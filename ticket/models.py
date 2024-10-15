from django.db import models
from connect_to_db import MongoHelper
from bson import json_util, ObjectId
# Create your models here.

Ticket= MongoHelper()
Ticket.getCollection("tickets")
