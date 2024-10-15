import pymongo
from bson import ObjectId

# url="mongodb+srv://ArjunKSoni:Arjun6261@cluster0.zmp7n.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# db=client['airindia']

class MongoHelper:
    def __init__(self):
        self.client = pymongo.MongoClient(host="127.0.0.1", port=27017, authSource="airindia")
        self.connection = self.client["airindia"]
        
    def getCollection(self, coll_name):
        self.db_coll_name = self.connection.get_collection(coll_name)
        if self.db_coll_name == None:
            self.db_coll_name= self.connection[coll_name]
            
    def serialiseObject(self, data):
        data['_id']=str(data['_id'])
        return data
            
    def insertSingle(self,doc):
        _id=self.db_coll_name.insert_one(doc).inserted_id
        return _id
    
    def findAll(self):
        data=[ self.serialiseObject(document) for document in self.db_coll_name.find()]
        return data
    
    def findByFilter(self, filter):
        data=[ self.serialiseObject(document) for document in self.db_coll_name.find(filter)]
        return data
    
    def findById(self, id):
        data= self.db_coll_name.find_one({"_id":ObjectId(id)})
        return self.serialiseObject(data)
    
    def updateOneById(self, id, updatedData):
        data= self.db_coll_name.update_one({"_id":ObjectId(id)},{"$set":updatedData})
        return data 
    
    def deleteOneById(self, id):
        print("id", id)
        data =self.db_coll_name.delete_one({"_id":ObjectId(id)})
        return data.acknowledged
        