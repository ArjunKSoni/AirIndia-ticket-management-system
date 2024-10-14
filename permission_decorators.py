from django.http import HttpResponse
from django.contrib.auth.models import User

def is_admin(func):
    def wrapper(request, *args, **kwargs):
        if not request.headers.get('AUTHORIZATION',None):
            return HttpResponse("Invalid Token")
        try:
            user=User.objects.get(id=request.user.get('id'))
            if user.groups.filter(name='admin').exists():
                return func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not authorized to view this page")
        except Exception as e:
            return HttpResponse("Internal server error")
    return wrapper

def is_customer(func):
    def wrapper(request, *args, **kwargs):
        if not request.headers.get('AUTHORIZATION',None):
            return HttpResponse("Invalid Token")
        try:
            user=User.objects.get(id=request.user.get('id'))
            if user.groups.filter(name='customer').exists() or user.groups.filter(name='admin').exists():
                return func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not authorized to view this page")
        except Exception as e:
            return HttpResponse("Internal server error")
    return wrapper

def is_staff(func):
    def wrapper(request, *args, **kwargs):
        if not request.headers.get('AUTHORIZATION',None):
            return HttpResponse("Invalid Token")
        try:
            user=User.objects.get(id=request.user.get('id'))
            print("user",user)
            if user.groups.filter(name='staff').exists() or user.groups.filter(name='admin').exists():
                return func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not authorized to view this page")
        except Exception as e:
            print(e)
            return HttpResponse("Internal server error")
    return wrapper

def is_ticket_counter_staff(func):
    def wrapper(request, *args, **kwargs):
        if not request.headers.get('AUTHORIZATION',None):
            return HttpResponse("Invalid Token")
        try:
            user=User.objects.get(id=request.user.get('id'))
            print(user)
            if user.groups.filter(name='ticket_counter').exists() or user.groups.filter(name='admin').exists():
                return func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not authorized to view this page")
        except Exception as e:
            print(e)
            return HttpResponse("Internal server error")
    return wrapper