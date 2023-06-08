from pymongo import MongoClient
from typing import TypedDict

# Connect to MongoDB
client = MongoClient('mongodb://root:example@localhost:27017/')

# Connect to database
db = client['test']

# Connect to collection
collection = db['test']

# Insert document
class TestDocument(TypedDict):
    user: int
    color: int

try:
    collection.insert_one(TestDocument(user=1, color=2))
    print('test document inserted')
except Exception as e:
    print(e)