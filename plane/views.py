from django.shortcuts import render
from .models import PlaneInfo
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ticket.models import Ticket
from permission_decorators import is_staff, is_ticket_counter_staff, is_admin
import json
# Create your views here.

@csrf_exempt
@is_admin
def register_plain(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            plane_number = PlaneInfo.insertSingle({
                            "plane_name":data['plane_name'], 
                            "source":data['source'], 
                            "destination":data['destination'], 
                            "status":data['status']
                            } )
            return JsonResponse({"plane_id":str(plane_number)})
        except Exception as e:
            print(e)
            return JsonResponse({"error":"internal server error"})
    
    elif request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            acknowledge=PlaneInfo.deleteOneById(data['plane_id'])
            if acknowledge:
                return JsonResponse({"status":acknowledge})
            else:
                return JsonResponse({"status":False})
        except Exception as e:
            print(e)
            return JsonResponse({"error":"internal server error"})
            
    return JsonResponse({"error":"method not supported"})



@is_ticket_counter_staff
def get_all_planes(request):
    planes = PlaneInfo.findAll()
    print(planes)
    return JsonResponse({"planes":planes})


@is_staff
def get_ticket_by_plane_id(request, id):
    if request.method == 'GET':
        tickets = Ticket.findByFilter({"plane_id":id})
        return JsonResponse({"tickets":tickets})
    return JsonResponse({"error":"method not supported"})

@csrf_exempt
@is_admin
def update_plane_status(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        resp = PlaneInfo.updateOneById(data['plane_id'],{"status":data['status']}) 
        if resp.acknowledged:
            return JsonResponse({"message":"status updated"})
        return JsonResponse({"error":"internal server error"})
    return JsonResponse({"error":"method not supported"})
