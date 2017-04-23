import json, sys
from django.http import (HttpResponse, 
                         HttpResponseBadRequest, 
                         HttpResponseForbidden,
                         HttpResponseNotFound,
                         JsonResponse)

class RequestHandler:
    def __init__(self, methods, callback):
        if not methods:
            raise ValueError('Methods need to be defined')
        if type(methods) is str:
            methods = [methods]
        self.methods = methods
        self.callback = callback
        self.needs_auth = False
        self.user_types = []

    def of(methods, callback):
        return RequestHandler(methods, callback)

    def forUserTypes(self, user_types):
        if user_types:
            self.needs_auth = True
            self.user_types = user_types
        return self

    def handle(self, request):
        if request.method not in self.methods:
            print ("Method does not exist")
            return HttpResponseBadRequest()

        #print ("DEBUG")
        #print (request.content_type, request.META['CONTENT_LENGTH'], request.body.decode('utf8'))

        if request.path == '/quiz' and request.method == 'POST':
            print ("Got POST to /quiz!")
            print ("Content-Type:", request.content_type)
            for key in request.POST:
                print ("Found POST key:", key)
            for key in request.FILES:
                print ("Found file:", key)
        if request.content_type == 'multipart/form-data' and 'data' in request.POST:
            data = request.POST['data']
            if len(data) > 0:
                try:
                    request.POST = json.loads(request.POST['data'])
                except:
                    return HttpResponse(status=422) 
        elif (request.method != 'GET' 
            and request.content_type == 'application/json'
            and 'CONTENT_LENGTH' in request.META
            and int(request.META['CONTENT_LENGTH']) > 0):
            try:
                request.POST = json.loads(request.body.decode('utf8'))
            except:
                return HttpResponse(status=422)

        
        if self.needs_auth:
            #print ("User type was {}".format(request.user.type.type))
            #print ("Types accepted were {}".format(self.user_types))
            if not request.user or not request.user.is_authenticated:
                return HttpResponse(status=401)
            if request.user.type.type not in self.user_types:
                return HttpResponseForbidden()
        return self.callback(request)


    def build(self):
        return lambda req : self.handle(req)
