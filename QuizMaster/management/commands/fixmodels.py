from QuizMaster.models.models import (GroupMeta,
                                        Membership,
                                        Question,
                                        QuestionAnswer,
                                        QuestionAudio,
                                        QuestionImage,
                                        Quiz,
                                        QuizComment,
                                        SubmittedQuiz,
                                        SubmittedQuizAnswer,
                                        UserType)
from collections import namedtuple

from django.conf import settings
from django.db import migrations, models, connection

from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Fixes relations (sets the ON DELETE to CASCADE)'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self._fix_tables()


    def _namedtuplefetchall(self, cursor):
        "Return all rows from a cursor as a namedtuple"
        desc = cursor.description
        nt_result = namedtuple('Result', [col[0] for col in desc])
        rows = cursor.fetchall()
        return [nt_result(*row) for row in rows]

    def _qm_join(self, l):
        if type(l) != list:
            l = [l]
        return ','.join(list(map(lambda entry: '`{}`'.format(entry), l)))

    def _change_referential_constraint(self, table, fk_name, fk_columns, other_table, pk_columns):
        ADD = """ALTER TABLE {} ADD FOREIGN KEY `{}`({})
                                    REFERENCES `{}`({}) ON DELETE CASCADE"""
        fk_columns = self._qm_join(fk_columns)
        pk_columns = self._qm_join(pk_columns)
        with connection.cursor() as cursor:
            cursor.execute('ALTER TABLE {} DROP FOREIGN KEY `{}`;'.format(table, fk_name))
            cursor.execute(ADD.format(table, fk_name, fk_columns, other_table, pk_columns))

    def _fix_tables(self):
      FETCH = """SELECT r.CONSTRAINT_NAME AS `fk_name`, r.DELETE_RULE, r.TABLE_NAME,
                        GROUP_CONCAT(k.COLUMN_NAME SEPARATOR ', ') AS `fk_columns`,
                        r.REFERENCED_TABLE_NAME as `other_table`,
                        k.REFERENCED_COLUMN_NAME as `pk_columns`
                FROM information_schema.REFERENTIAL_CONSTRAINTS r
                  JOIN information_schema.KEY_COLUMN_USAGE k
                  USING (CONSTRAINT_CATALOG, CONSTRAINT_SCHEMA, CONSTRAINT_NAME)
                WHERE r.CONSTRAINT_SCHEMA = %s AND r.TABLE_NAME=%s
                GROUP BY r.CONSTRAINT_CATALOG,
                         r.CONSTRAINT_SCHEMA,
                         r.CONSTRAINT_NAME"""
      # Fetch constraint
      # Fix it
      models = [
        GroupMeta,
        Membership,
        Question,
        QuestionAnswer,
        QuestionAudio,
        QuestionImage,
        Quiz,
        QuizComment,
        SubmittedQuiz,
        SubmittedQuizAnswer,
        UserType
      ]

      schema = settings.DATABASES['default']['NAME']
      for model in models:
        table = model.objects.model._meta.db_table
        print ("Fixing ", table)
        with connection.cursor() as cursor:
          cursor.execute(FETCH, [schema, table])
          for row in self._namedtuplefetchall(cursor):
            print ("Replacing ",row.fk_name)
            self._change_referential_constraint(table, row.fk_name, row.fk_columns, row.other_table, row.pk_columns)