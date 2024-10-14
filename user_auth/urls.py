from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.register),
    path("login/", views.user_login),
    path("verify/", views.verify),
    path("<id>", views.get_user),
    path("tickets/", views.get_ticket_by_userid),
]
