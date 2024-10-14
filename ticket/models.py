from django.db import models
from connect_to_db import db
from bson import json_util, ObjectId
# Create your models here.

class Ticket:
    def __init__(self, passenger_id, plane_id, source, destination, date_of_journey, time_of_journey, status):
        self.passenger_id = passenger_id
        self.plane_id = plane_id
        self.source = source
        self.destination = destination
        self.date_of_journey = date_of_journey
        self.time_of_journey = time_of_journey
        self.status = status

    Objects = db['tickets']
    
    def save(self):
        ticket_id = self.Objects.insert_one(self.__dict__).inserted_id
        return ticket_id
    
    @classmethod
    def get_all_tickets(cls):
        return json_util.dumps(cls.Objects.find())
    
    @classmethod
    def get_ticket_by_passenger_id(cls, passenger_id):
        return json_util.dumps(cls.Objects.find({"passenger_id":passenger_id}))
    
    @classmethod
    def get_ticket_by_plane_id(cls, plane_id):
        return json_util.dumps(cls.Objects.find({"plane_id":plane_id}))
    
    @classmethod
    def get_ticket_by_id(cls, ticket_id):
        data=cls.Objects.find_one({"_id":ObjectId(ticket_id)})
        return json_util.dumps(data)
    