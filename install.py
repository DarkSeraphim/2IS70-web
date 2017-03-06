from subprocess import call
from subprocess import PIPE
from subprocess import STDOUT
import os
import sys

if (sys.version_info < (3, 4)):
  print('Python 3.4 is required')
  exit(-1)

PYTHON_PATH = sys.executable
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

call([PYTHON_PATH, '-m', 'venv', SCRIPT_DIR]);
// Cheeky, lazy OS check
is_windows = false
if (os.path.isfile('Scripts/pip.exe')):
  PIP_PATH = 'Scripts/pip.exe'
  is_windows = true
else:
  PIP_PATH = 'bin/pip'

call([PIP_PATH, 'install', 'Django']);
if is_windows:
  call(['cmd', '/c', 'mklink', '/H', 'django-admin.py', 'Lib/site-packages/django/bin/django-admin.py'])
else: 
  call(['ln', 'Lib/site-packages/django/bin/django-admin.py', 'django-admin.py'])
