from django.shortcuts import render
from .models import Ticket
from plane.models import PlaneInfo
from django.http import JsonResponse
import json
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from permission_decorators import is_ticket_counter_staff, is_customer
# Create your views here.


@csrf_exempt
@is_ticket_counter_staff
def book_ticket(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print("data",data)
        try:
            ticket_number = Ticket.insertSingle({
                            "passenger_id":data['passenger_id'], 
                            "plane_id":data['plane_id'], 
                            "source":data['source'], 
                            "destination":data['destination'], 
                            "date_of_journey":data['date_of_journey'], 
                            "time_of_journey":data['time_of_journey'], 
                            "status":data['status']
                            })
            return JsonResponse({"ticket_url":"http://127.0.0.1:8000/ticket/"+str(ticket_number)})

        except Exception as e:
            print(e)
            return JsonResponse({"error":"internal server error"})
        
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            resp=Ticket.updateOneById(data['ticket_id'],data['ticket'])
            return JsonResponse({"status":resp.acknowledged})
        except Exception as e:
            print(e)
            return JsonResponse({"error":"internal server error"})
        
    elif request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            acknowledge=Ticket.deleteOneById(data['ticket_id'])
            if acknowledge:
                return JsonResponse({"status":acknowledge})
            else:
                return JsonResponse({"status":False})
        except Exception as e:
            print(e)
            return JsonResponse({"error":"internal server error"})

    return JsonResponse({"error":"method not supported"})

@is_customer
def get_ticket_details(request, id):
    if request.method == "GET":
        try:
            ticket = Ticket.findById(id)
            plane = PlaneInfo.findById(ticket['plane_id'])
            user = User.objects.get(id=ticket['passenger_id'])
            
            return JsonResponse({"ticket":ticket,
                                "plane":plane,
                                "user":{
                                    "username":user.username,
                                    "email":user.email,
                                    "first_name":user.first_name,
                                    "last_name":user.last_name
                                    }
                                })
        except Exception as e:
            print(e)
            return JsonResponse({"error":"Internal server error"})
    
    return JsonResponse({"error":"method not supported"})