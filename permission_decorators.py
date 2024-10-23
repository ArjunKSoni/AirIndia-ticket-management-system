from django.http import HttpResponse
from django.contrib.auth.models import User

def isAuthorized(group):
    def authDecorator(func):
        def wrapper(request, *args, **kwargs):
            if not request.headers.get('AUTHORIZATION',None):
                return HttpResponse("Invalid Token")
            try:
                user=User.objects.get(id=request.user.get('id'))
                print(user)
                if user.groups.filter(name=group).exists() or user.groups.filter(name='admin').exists():
                    return func(request, *args, **kwargs)
                else:
                    return HttpResponse("You are not authorized to view this page")
            except Exception as e:
                print(e)
                return HttpResponse("Internal server error")
        return wrapper
    return authDecorator