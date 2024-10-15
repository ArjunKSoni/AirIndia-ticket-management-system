from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth.models import Group
from ticket.models import Ticket
from permission_decorators import is_staff, is_customer, is_ticket_counter_staff
import jwt
import json
# Create your views here.

@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data= json.loads(request.body)
            username = data["username"]
            password = data["password"]
            email = data["email"]
            first_name = data["first_name"]
            last_name = data["last_name"]
            
            if User.objects.filter(username=username).exists():
                return JsonResponse({"error":"username already exists"})
            
            if data["group"] not in ["admin", "staff", "customer", "ticket_counter"]:
                return JsonResponse({"error":"invalid group"})
            
            group, created = Group.objects.get_or_create(name=data["group"])
            user=User.objects.create_user(
                username=username,
                email=email
                )

            user.first_name = first_name
            user.last_name = last_name
            
            print("first name",user.first_name)
            user.set_password(password)
            
            user.groups.set([group])
            print(user.groups.all())
            user.save()
            
            jwt_token= jwt.encode({"id":user.id,"username":user.username},
                                  key=settings.SECRET_KEY, 
                                  algorithm=settings.JWT_ALGORITHM
                                  )
            
            return JsonResponse({"Token": jwt_token})
        
        except Exception as e:
            print(e)
            return JsonResponse({"error":"internal server error"})
    return JsonResponse({"error":"method not supported"})


@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data["username"]
        password = data["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            jwt_token= jwt.encode({"id":user.id,"username":user.username},
                                  key=settings.SECRET_KEY, 
                                  algorithm=settings.JWT_ALGORITHM
                                  )
            return JsonResponse({"Token": jwt_token})
    return JsonResponse({"error":"method not supported"})


@csrf_exempt
@is_staff
def verify(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        token = data["token"]
        print(token)
        try:
            data = jwt.decode(token, key=settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            return JsonResponse({"user":data})
        except Exception as e:
            print(e)
            return JsonResponse({"error":"invalid token"})
    return JsonResponse({"error":"method not supported"})

@is_ticket_counter_staff
def get_user(request, id):
    if request.method == 'GET':
        try:
            user = User.objects.get(id=id)
            return JsonResponse({"user":{
                "username":user.username,
                "email":user.email,
                "first_name":user.first_name,
                "last_name":user.last_name
                }})
        except Exception as e:
            print(e)
            return JsonResponse({"error":"internal server error"})
    return JsonResponse({"error":"method not supported"})


@is_customer
def get_ticket_by_userid(request):
    if request.method == 'GET':
        try:
            tickets = Ticket.findByFilter({"passenger_id":request.user['id']})
            return JsonResponse({"tickets":tickets})
        except Exception as e:
            return JsonResponse({"error":"internal server error"})
    return JsonResponse({"error":"method not supported"})