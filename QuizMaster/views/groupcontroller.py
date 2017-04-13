from django.http import (HttpResponse, 
                         HttpResponseBadRequest, 
                         HttpResponseForbidden,
                         HttpResponseNotFound,
                         JsonResponse)

from QuizMaster.models.models import Group, GroupMeta, UserType
import uuid

def getAll(request):
  groups = []
  if request.user.type.type == UserType.STUDENT:
    rels = request.user.groups
  else:
    rels = request.user.own_groups
  for group in rels.all():
    if type(group) is GroupMeta:
      group = group.group
    groups.append({
      "id": group.pk,
      "name": group.name,
      "access_code": group.meta.access_code
    })
  return JsonResponse(groups, safe=False)

def manageGroup(request):
  if request.method == 'POST':
    return createGroup(request)
  elif request.method == 'PUT':
    return updateGroup(request)
  else: # request.method == 'DELETE'
    return deleteGroup(request)

def createGroup(request):
  name = request.POST['name']
  if not name:
    return HttpResponseBadRequest()
  try:
    group = Group.objects.get(name=name)
    return HttpResponse(status=409)
  except Group.DoesNotExist:
    pass
  group = Group()
  group.name = name
  group.save()

  meta = GroupMeta()
  meta.access_code = str(uuid.uuid4())[:6]
  meta.group = group
  meta.creator = request.user
  meta.save()
  
  return JsonResponse({
    "id": group.pk,
    "name": group.name,
    "access_code": meta.access_code
  })

def updateGroup(request):
  pk = request.GET['group_id']
  name = request.POST['name']
  
  if not pk or not name:
    return HttpResponseBadRequest()

  try:
    group = Group.objects.get(pk=pk)
  except Group.DoesNotExist:
    return HttpResponseNotFound()

  if group.meta.creator.pk != request.user.pk:
    return HttpResponseForbidden()

  try:
    group = Group.objects.get(name=name)
    return HttpResponse(status=409)
  except Group.DoesNotExist:
    pass
  
  group.name = name
  group.save()
  return JsonResponse({
    "id": group.pk,
    "name": group.name  
  })

def deleteGroup(request):
  pk = request.GET['group_id']
  if not pk:
    return HttpResponseBadRequest()

  try:
    group = Group.objects.get(pk=pk)
  except Group.DoesNotExist:
    return HttpResponseNotFound()

  if group.meta.creator.pk != request.user.pk:
    return HttpResponseForbidden()

  group.delete()
  return JsonResponse({
    "id": pk, # group.pk == null
    "name": group.name  
  })

def subscription(request):
  if request.method == 'POST':
    return joinGroup(request)
  else: # request.method == 'DELETE'
    return leaveGroup(request)

def joinGroup(request):
  code = request.POST['access_code']
  if not code:
    return HttpResponseBadRequest()

  try:
    meta = GroupMeta.objects.get(access_code=code)
    group = meta.group
  except:
    return HttpResponseNotFound()

  user = request.user
  if group.user_set.filter(pk=user.pk).exists():
  # if user in group.users: # Actually fix this, rofl
    return HttpResponse(status=409)
  
  group.user_set.add(user)
  return HttpResponse()

def leaveGroup(request):
  pk = request.GET['group_id'];
  try:
    group = Group.objects.get(pk=pk)
  except Group.DoesNotExist:
    return HttpResponseNotFound()

  user = request.user
  if not group.user_set.filter(pk=user.pk).exists():
  # if user not in group.users: # Actually fix this, rofl
    return HttpResponse(status=409)

  group.user_set.remove(user)
  return HttpResponse()