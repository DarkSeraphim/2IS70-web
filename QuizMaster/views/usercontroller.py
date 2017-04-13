from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from QuizMaster.models.models import UserType
from time import time
from django.http import (HttpResponse, 
                         HttpResponseBadRequest, 
                         HttpResponseForbidden,
                         HttpResponseNotFound,
                         JsonResponse)
from django.core import serializers

EMAIL_BODY = """Hello {0},
             You seem to have requested a password reset. 
             If this was not you, feel free to ignore this email.

             If this was you, please enter the following code in the app (the code expires in 15 minutes):
             {1}

             (In the login view, tap 'Forgot password', then tap 'Enter code')

             Sincerely,

             QuizMaster team"""

#def user_can_authenticate(user):
#  """
#  Reject users with is_active=False. Custom user models that don't have
#  that attribute are allowed.
#  """
#  is_active = getattr(user, 'is_active', None)
#  return is_active or is_active is None

# Copied from ModelBackend
"""def authenticate(email, password):
  try:
    user = User.objects.get(email=email)
  except UserModel.DoesNotExist:
    # Run the default password hasher once to reduce the timing
    # difference between an existing and a non-existing user (#20760).
    User().set_password(password)
  else:
    if user.check_password(password) and user_can_authenticate(user):
      return user
"""
def validate(data, *fields):
  for field in fields:
    if field not in data:
      return False
  return True

def do_login(request):
  if not validate(request.POST, 'email', 'password'):
    return HttpResponseBadRequest()

  email = request.POST['email']
  password = request.POST['password']
  if not email or not password:
    return HttpResponseBadRequest()

  user = authenticate(username=email, password=password)
  if user:
    try:
      logout(request)
    except:
      pass
    login(request, user)
    # request.session['user_type'] = user.type
    return JsonResponse({
      "id": user.pk,
      "name": user.first_name,
      "email": user.email,
      "type": user.type.type
    })
  return HttpResponseNotFound()

def register(request):
  if not validate(request.POST, 'name', 'email', 'password', 'type'):
    return HttpResponseBadRequest()
  name = request.POST['name']
  email = request.POST['email']
  password = request.POST['password']
  account_type = request.POST['type'].lower()
  if not name or not email or not password or not account_type:
    return HttpResponseBadRequest()

  if account_type not in [UserType.STUDENT, UserType.TEACHER]:
    return HttpResponseBadRequest()

  try:
    user = User.objects.get(email=email)
    # Already exists
    return HttpResponse(status=409)
  except User.DoesNotExist:
    pass

  user = User.objects.create_user(username=email, first_name=name, email=email, password=password)
  user.save()
  utype = UserType()
  utype.type = account_type
  utype.user = user
  utype.save()
  login(request, user) # Auto login

  # Other data
  # TODO: do register 
  # RETURN: 409 if email exists, 400 if parameters are missing, 200 if successfull
  return JsonResponse({
    "id": user.id,
    "name": user.first_name,
    "email": user.email,
    "type": user.type.type  
  })

def password_request_reset(request):
  email = request.POST['email']
  user = False # Find user by email
  if not user:
    return HttpResponseNotFound()

  rand_str = lambda n: ''.join([random.choice(string.lowercase) for i in xrange(n)])
  code = rand_str(16)
  request.session['reset_email'] = email
  request.session['reset_code'] = code
  request.session['reset_expire'] = time() + 15 * 60
  message = EMAIL_BODY.format(user.name, code)
  user.email_user(subject='QuizMaster password reset', message=message)

  return HttpResponse(status=200)

def password_reset(request):
  session_code = request.session['reset_code']
  expire = request.session['reset_expire']
  email = request.session['reset_email']
  if not session_code or not expire or not email or time() < expire:
    return HttpResponseNotFound()
  
  code = request.POST['code']
  password = request.POST['password']
  if not code or not password or code != session_code:
    return HttpResponseNotFound()
  
  user = False # Load by email
  if not user:
    return HttpResponseNotFound()

  user.set_password(password)
  del request.session['reset_email']
  del request.session['reset_code']
  del request.session['reset_expire']
  return HttpResponse(status=200)

def do_logout(request):
  if request.user and request.user.is_authenticated:
    logout(request)
    return HttpResponse(status=200)
  return HttpResponse(status=401)