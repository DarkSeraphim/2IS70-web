from django.http import (HttpResponse, 
                         HttpResponseBadRequest, 
                         HttpResponseForbidden,
                         HttpResponseNotFound,
                         JsonResponse)

from django.contrib.auth.models import User
from QuizMaster.models.models import (Group, 
                                      Quiz,
                                      Question,
                                      QuestionImage,
                                      QuestionAudio,
                                      QuestionAnswer,
                                      SubmittedQuiz, 
                                      SubmittedQuizAnswer,
                                      Membership,
                                      UserType)
from random import shuffle
from django.conf import settings
import os

def getAll(request):
  user = request.user
  if user.type.type == UserType.STUDENT:
    quizes = Quiz.objects.filter(groups__user=user)
  else: # Teacher
    quizes = Quiz.objects.filter(creator=user)
  res_quizes = []
  for quiz in quizes:
    res_groups = []
    for group in quiz.groups.all():
      res_groups.append({
        "id": group.pk,
        "name": group.name
      })
      
    res_questions = []
    for question in quiz.questions.all():
      res_answers = []
      for answer in question.answers.all():
        res_answers.append({
          "id": answer.pk,
          "text": answer.text  
        })
      if request.user.type.type == UserType.STUDENT:
        shuffle(res_answers)
      res_question = {
        "id": question.pk,
        "text": question.text,
        "weight": question.weight,
        "is_open": question.is_open,
        "correct_answer": {
          "id": question.correct_answer.pk,
          "text": question.correct_answer.text
        },
        "answers": res_answers
      }
      if request.user.type.type == UserType.STUDENT:
        del res_question['correct_answer']
        if question.is_open:
          res_question['answers'] = []
      res_questions.append(res_question)
    res_quiz = {
      "id": quiz.pk,
      "creator": {
        "id": quiz.creator.pk,
        "name": quiz.creator.first_name,
        "email": quiz.creator.email
      },
      "name": quiz.name,
      "start_at": quiz.start_at,
      "close_at": quiz.close_at,
      "time_limit": quiz.time_limit,
      "pass_threshold": quiz.pass_threshold,
      "groups": res_groups,
      "questions": res_questions
    }
    res_quizes.append(res_quiz)
  # Find all tests and serialise as JSON array
  return JsonResponse(res_quizes, safe=False)

def manage(request):
  if request.method == 'POST':
    return createTest(request)
  else: # request.method == 'DELETE'
    return deleteTest(request)

def validate(data, *fields):
  for field in fields:
    if field not in data:
      return False
  return True

def writeUserFile(file, path):
  filepath = settings.BASE_DIR + '/files/' + path
  dir = os.path.dirname(filepath)
  if not os.path.exists(dir):
    os.makedirs(dir)
  with open(filepath, 'wb+') as destination:
    for chunk in file.chunks():
      destination.write(chunk)

def createTest(request):
  data = request.POST
  quizData = ('name', 'start_at', 'close_at', 'time_limit', 'pass_threshold', 'questions')
  questionData = ('text', 'is_open', 'weight', 'answers')
  answerData = ['text']

  # Validate quiz data
  if not validate(data, *quizData):
    print ("Quiz data invalid")
    return HttpResponseBadRequest()

  # Validate question data
  qdatas = data['questions']
  if type(qdatas) != list or len(qdatas) == 0:
    print ("no questions")
    return HttpResponseBadRequest()

  for qdata in qdatas:
    if not validate(qdata, *questionData):
      print ("question data not valid")
      return HttpResponseBadRequest()
    # Validate answers

    adatas = qdata['answers']
    if type(adatas) != list or len(adatas) == 0:
      print ("no answers")
      return HttpResponseBadRequest()

    for adata in adatas:
      print ("answer ", adata)
      if not validate(adata, *answerData):
        print ("answer data not valid: ", adata)
        return HttpResponseBadRequest()    

  # Validate groups

  if type(data['groups']) != list or len(data['groups']) == 0:
    print ("No groups given")
    return HttpResponseBadRequest()

  groups = []
  res_groups = []
  for groupId in data['groups']:
    try:
      group = Group.objects.get(pk=groupId['id'])
      groups.append(group)
      res_groups.append({
        "id": group.pk,
        "name":  group.name  
      })
    except Group.DoesNotExist:
      print ("No group found")
      return HttpResponseBadRequest()

  quiz = Quiz()
  quiz.name = data['name']
  quiz.creator = request.user
  quiz.start_at = data['start_at']
  quiz.close_at = data['close_at']
  quiz.time_limit = data['time_limit']
  quiz.pass_threshold = data['pass_threshold']
  quiz.save()

  for group in groups:
    Membership.objects.create(group=group, quiz=quiz)

  tid = 0
  res_questions = []
  for qdata in data['questions']:
    question = Question()
    question.text = qdata['text']
    question.is_open = qdata['is_open']
    question.weight = qdata['weight']
    question.quiz = quiz
    question.save()
    res_question = {
      "id": question.pk,
      "text": question.text,
      "is_open": question.is_open,
      "weight": question.weight,
    }

    res_answers = []
    first = True;
    for adata in qdata['answers']:
      atext = adata['text']
      answer = QuestionAnswer()
      answer.question = question
      answer.text = atext
      answer.save()
      res_answers.append({
        "id": answer.pk,
        "text": answer.text
      })
      question.answers.add(answer)
      if first:
        question.correct_answer = answer
        question.save()
        first = False
        res_question['correct_answer'] = {
          "id": answer.pk,
          "text": answer.text
        }

    res_question['answers'] = res_answers

    audiofilekey = 'question-' + str(tid) + '-audio'
    if audiofilekey in request.FILES:
      audiofile = request.FILES[audiofilekey]
      qa = QuestionAudio()
      path = str(quiz.pk) + '/' + str(question.id) + '/audio.mp3'
      qa.path = path
      qa.question = question
      qa.save()
      writeUserFile(audiofile, path)
      res_question['audio'] = {
        "id": qa.pk,
        "path": path
      }
    imagefilekey = 'question-' + str(tid) + '-image'
    if imagefilekey in request.FILES:
      imagefile = request.FILES[imagefilekey]
      qi = QuestionImage()
      path = str(quiz.pk) + '/' + str(question.id) + '/image.jpg'
      qi.path = path
      qi.question = question
      qi.save()
      writeUserFile(imagefile, path)
      res_question['image'] = {
        "id": qi.pk,
        "path": path
      }

    tid += 1
    res_questions.append(res_question)

  return JsonResponse({
    "name": quiz.name,
    "creator": {
      "id": quiz.creator.id,
      "name": quiz.creator.first_name,
      "email": quiz.creator.email
    },
    "start_at": quiz.start_at,
    "close_at": quiz.close_at,
    "time_limit": quiz.time_limit,
    "pass_threshold": quiz.pass_threshold,
    "groups": res_groups,
    "questions": res_questions
  })  

def deleteTest(request):
  pk = request.GET['quiz_id']
  if not pk:
    return HttpResponseBadRequest()
  try:
    quiz = Quiz.objects.get(pk=pk)
  except Quiz.DoesNotExist:
    return HttpResponseNotFound()

  if quiz.creator.id != request.user.id:
    return HttpResponseForbidden()

  quiz.delete()
  return JsonResponse({"id": pk, "name": quiz.name})

def submit(request):
  data = request.POST
  if not validate(data, 'quiz', 'submitted_at', 'answers'):
    print("Invalid data")
    return HttpResponseBadRequest()
  
  try:
    quiz = Quiz.objects.get(pk=data['quiz']['id'])
  except Quiz.DoesNotExist:
    return HttpResponseNotFound()

  # check if the intersection of the user's groups and the groups for which this quiz was published
  # is not empty (which means the user has access)
  mygroups = set(request.user.groups.all())
  quizgroups = set(quiz.groups.all())
  if len(mygroups.intersection(quizgroups)) == 0:
    return HttpResponseForbidden()

  answerdata = data['answers']
  answers = []

  if type(answerdata) != list or len(answerdata) == 0:
    return HttpResponseBadRequest()

  for adata in answerdata:
    if not validate(adata, 'question', 'answer', 'answer_text'):
      return HttpResponseBadRequest()
    
    text = adata['answer_text']
    try:
      question = Question.objects.get(pk=adata['question']['id'], quiz=quiz)
    except Question.DoesNotExist:
      return HttpResponseBadRequest()

    if question.is_open:
      try:
        answer = QuestionAnswer.objects.get(text=text, question=question)
      except QuestionAnswer.DoesNotExist:
        pass # Wrong answer, sucks to suck
    else:
      try:
        answer = QuestionAnswer.objects.get(pk=adata['answer']['id'], question=question)
      except QuestionAnswer.DoesNotExist:
        return HttpResponseBadRequest()

    answers.append({
      "question": question,
      "answer": answer,
      "text": text
    })
  
  submission = SubmittedQuiz()
  submission.quiz = quiz
  submission.user = request.user
  submission.submitted_at = data['submitted_at']
  submission.save()

  for answer in answers:
    subans = SubmittedQuizAnswer()
    subans.question = answer['question']
    subans.answer = answer['answer']
    subans.text = answer['text']
    subans.quiz = submission
    subans.save()

  submission.save() # Do we need this?
  
  return HttpResponse()

def reviewAsStudent(request):
  user = request.user
  try:
    quiz = Quiz.objects.get(pk=request.GET['quiz_id'])
  except Quiz.DoesNotExist:
    return HttpResponseNotFound()
  try:
    mine = SubmittedQuiz.objects.get(quiz=quiz, user=user)
  except SubmittedQuiz.DoesNotExist:
    return HttpResponseNotFound()

  # Load answers, serialise, and throw it back to the user
  res_answers = []
  for answer in mine.answers.all():
  
    res_question = {
      "id": answer.question.pk,
      "text": answer.question.text,
      "weight": answer.question.weight,
      "is_open": answer.question.is_open,
      "correct_answer": {
        "id": answer.question.correct_answer.pk,
        "text": answer.question.correct_answer.text
      }
    }

    my_answer = {}
    if answer.answer:
      my_answer = {
        "id": answer.answer.pk,
        "text": answer.answer.text,
      }

    res_answers.append({
      "id": answer.pk,
      "question": res_question,
      "answer": my_answer,
      "answer_text": answer.answer_text
    })

  return JsonResponse({
    "id": mine.pk,
    "submitted_at": mine.submitted_at,
    "answers": res_answers
  })

def reviewAsTeacher(request):
  if not validate(request.GET, 'quiz_id'):
    return HttpResponseBadRequest()

  pk = request.GET['quiz_id']
  if not pk:
    return HttpResponseBadRequest()
  user = request.user

  try:
    quiz = Quiz.objects.get(pk=pk, creator=request.user)
  except Quiz.DoesNotExist:
    return HttpResponseNotFound()
  
  stats = {}
  for question in quiz.questions.all():
    stats[question.pk] = {
      "qiestion": question,
      "answers": 0,
      "points": 0
    }

  # Find submitted tests, crunch data, serialise, throw back
  submissions = SubmittedQuiz.objects.filter(quiz=quiz).all()
  minimum = None
  maximum = None
  average = 0
  weight = 0

  for submission in submissions:
    score = 0
    for answer in submission.answers.all():
      # Correct!
      stat = stats[answer.question.pk]
      if answer.answer != None and answer.answer.pk == answer.question.correct_answer.pk:
        score += answer.question.weight
        stat['points'] += answer.question.weight
      stat['answers'] += 1

    if minimum == None or minimum > score:
      minimum = score
    if maximum == None or maximum < score:
      maximum = score

    if weight == 0:
      average = score
    else:
      average = average * (n / (n + 1)) + score * (1 / (n + 1))
    weight += 1

  res_stats = []
  for question in quiz.questions.all():
    stat = stats[question.pk]
    res_question = {
      "id": question.pk,
      "text": question.text,
      "is_open": question.is_open,
      "weight": question.weight
    }
    res_stats.append({
      "question": res_question,
      "answers": stat['answers'],
      "points": stat['points']
    })

  users = set()
  for group in quiz.groups.all():
    for u in group.user_set.all():
      users.add(u)

  return JsonResponse({
    "statistics": res_stats,
    "total_students": len(users),
    "submissions": len(submissions),
    "min_score": minimum,
    "average_score": average,
    "max_score": maximum,
  })
