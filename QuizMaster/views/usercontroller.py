

def login(request):
  email = request.body['email']
  password = request.body['password']
  # TODO: do login
  # RETURN: 400 if parameters missing, 404 if email / pass not found, 200 if successfull
  #
  return JsonResponse()

def register(request):
  email = request.body['email']
  password = request.body['password']
  account_type = request.body['account_type'];
  # Other data
  # TODO: do register 
  # RETURN: 409 if email exists, 400 if parameters are missing, 200 if successfull
  return JsonResponse()