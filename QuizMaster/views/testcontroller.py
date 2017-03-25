

def getAll(request):
  user = request.session['user_id']
  # Find all tests and serialise as JSON array
  return JsonResponse()

def manage(request):
  if request.method == 'POST':
    return createTest(request)
  elif request.method == 'PUT':
    return updateTest(request)
  else: # request.method == 'DELETE'
    return deleteTest(request)

def createTest(test, request):
  # Check if all fields are there!
  # Take care not to override an existing ID!
  return JsonResponse()

def updateTest(test, request):
  user = request.session['user_id']
  test = False # Load test
  if not test:
    return HttpResponseNotFound()
  if test.creator != user:
    return HttpResponseForbidden()
  # Set test fields
  # save to DB
  return JsonResponse()

def deleteTest(test, request):
  user = request.session['user_id']
  test = False # Load test
  if not test:
    return HttpResponseNotFound()
  if test.creator != user:
    return HttpResponseForbidden()

  # Delete it!!!!@

  return JsonResponse()

def submit(request):
  test = False # Load test
  if not test:
    return HttpResponseNotFound()
  user = False
  if not user:
    return HttpResponseNotFound() # Wtf did just happen

  # check if the intersection of the user's groups and the groups for which this quiz was published
  # is not empty (which means the user has access)

  # Create new SubmittedQuiz object, and related models of course

  return JsonResponse()

def reviewAsStudent(request):
  user = request.session['user_id']
  test = False # Load submitted test
  if not test:
    return HttpResponseNotFound()
  if test.user != user: # Was it our quiz?
    return HttpResponseForbidden()

  # Load answers, serialise, and throw it back to the user

  return JsonResponse()

def reviewAsTeacher(request):
  user = request.session['user_id']
  test = False # Load test
  if not test:
    return HttpResponseNotFound()
  if test.creator != user: # Are we the creator
    return HttpResponseForbidden()

  # Find submitted tests, crunch data, serialise, throw back

  return JsonResponse()