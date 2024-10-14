from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.register_plain),
    path("planes/", views.get_all_planes),
    path("plane/<id>", views.get_ticket_by_plane_id),
    path("plane/", views.update_plane_status),
    
]
