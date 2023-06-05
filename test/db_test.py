from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://root:example@localhost:27017/')

# Connect to database
db = client['test']

# Connect to collection
collection = db['test']

# Insert document
try:
    collection.insert_one({"name": "John", "age": 30})
    print('test document inserted')
except Exception as e:
    print(e)