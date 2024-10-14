from django.db import models
from connect_to_db import db
from bson import json_util, ObjectId

# Create your models here.


class PlaneInfo:
    def __init__(self, plane_name, source, destination, status):
        self.plane_name = plane_name
        self.source = source
        self.destination = destination
        self.status = status

    Objects = db['planes']
    
    def save(self):
        plane_id = self.Objects.insert_one(self.__dict__).inserted_id
        return plane_id
    
    @classmethod
    def get_all_planes(cls):
        return json_util.dumps(cls.Objects.find())
    
    @classmethod
    def get_plane_by_source(cls, source):
        return json_util.dumps(cls.Objects.find({"source":source}))
    
    @classmethod
    def get_plane_by_destination(cls, destination):
        return json_util.dumps(cls.Objects.find({"destination":destination}))
    
    @classmethod
    def get_plane_by_id(cls, plane_id):
        return json_util.dumps(cls.Objects.find_one({"_id":ObjectId(plane_id)}))
    
    @classmethod
    def update_plane_status(cls, plane_id, status):
        cls.Objects.update_one({"_id":ObjectId(plane_id)},{"$set":{"status":status}})
        return True
    