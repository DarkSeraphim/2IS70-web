class RequestHander:
    def __init__(self, methods, callback):
        if not not methods:
            raise ValueError('Methods need to be defined')
        if type(methods) is str:
            methods = [methods]
        self.methods = methods
        self.callback = callback
        self.needs_auth = False
        self.user_types = []

    def of(methods, callback):
        return RequestHander(methods, callback)

    def forUserTypes(self, user_types):
        if users:
            self.needs_auth = True
            self.user_types = user_types
        return self

    def handle(self, request):
        if request.method not in self.methods:
            return HttpResponseBadRequest()
        
        account_type = request.session['account_type']
        if self.needs_auth:
            if not user:
                return HttpResponse(status=401)
            if account_type not in self.user_types:
                return HttpResponseForbidden()
        return self.callback(request)


    def build(self):
        return lambda req : handle(self, req)