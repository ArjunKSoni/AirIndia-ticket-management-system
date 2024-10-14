import pymongo

url="mongodb+srv://ArjunKSoni:Arjun6261@cluster0.zmp7n.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client =pymongo.MongoClient(url)

db=client['test_airindia']
