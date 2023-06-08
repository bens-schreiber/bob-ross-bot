from pymongo import MongoClient
from pymongo.collection import Collection

from no_sql.entities import *

# Connect to MongoDB
client = MongoClient('mongodb://root:example@localhost:27017/')

# Grab the bob-ross-db database
db = client['bob-ross-db']

def colors_collection()-> Collection[UserColor]:
    """Reference to the colors collection in the bob-ross-db database"""
    return db["colors"]

def coordinates_x_collection() -> Collection[UserCoordinateX]:
    """Reference to the coordinates_x collection in the bob-ross-db database"""
    return db["coordinates_x"]

def coordinates_y_collection() -> Collection[UserCoordinateY]:
    """Reference to the coordinates_y collection in the bob-ross-db database"""
    return db["coordinates_y"]