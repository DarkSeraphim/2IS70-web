

def getAll(request):
  return JsonResponse()

def manageGroup(request):
  if request.method == 'POST':
    return createGroup(request)
  elif request.method == 'PUT'
    return updateGroup(request)
  else # request.method == 'DELETE'
    return deleteGroup(request)

def createGroup(request):
  group = True # load group by name
  if group:
    return HttpResponse(status=409)
  return JsonResponse()

def updateGroup(request):
  group = False # Load group
  if not group:
    return HttpResponseNotFound()
  return JsonResponse()

def deleteGroup(request):
  return JsonResponse()

def subscription(request):
  group = False # Load group
  if not group:
    return HttpResponseNotFound()
  if request.method == 'POST'
    return joinGroup(group, request)
  else # request.method == 'DELETE'
    return leaveGroup(group, request)

def joinGroup(group, request):
  user = request.session['user_id']
  if user in group.users(): # Actually fix this, rofl
    return HttpResponse(status=409)
  
  group.users().add(user)
  return JsonResponse()

def leaveGroup(group, request):
  user = request.session['user_id']
  if user not in group.users(): # Actually fix this, rofl
    return HttpResponse(status=409)

  group.users().remove(user)
  return JsonResponse()