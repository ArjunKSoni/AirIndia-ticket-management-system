from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.book_ticket),
    path("<id>", views.get_ticket_details),
]
