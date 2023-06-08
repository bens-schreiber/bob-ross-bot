from typing import Tuple
from pymongo import MongoClient
from pymongo.collection import Collection

from no_sql.entities import *

# Connect to MongoDB
client = MongoClient('mongodb://root:example@localhost:27017/')

# Grab the bob-ross-db database
db = client['bob-ross-db']


def colors_collection() -> Collection[UserColor]:
    """Reference to the colors collection in the bob-ross-db database"""
    return db["colors"]


def coordinates_x_collection() -> Collection[UserCoordinateX]:
    """Reference to the coordinates_x collection in the bob-ross-db database"""
    return db["coordinates_x"]


def coordinates_y_collection() -> Collection[UserCoordinateY]:
    """Reference to the coordinates_y collection in the bob-ross-db database"""
    return db["coordinates_y"]


def find_user_color(user: int) -> UserColor | None:
    """Find a user's color in the database."""
    return colors_collection().find_one(UserColor(user=user))


def set_user_color(user: int, color: int) -> None:
    colors_collection().update_one(
        {"user": user},
        {"$set": {"color": color}},
        upsert=True
    )


def find_user_coordinates(user: int) -> Tuple[int, int] | None:
    """Find a user's coordinates in the database."""
    x = coordinates_x_collection().find_one(UserCoordinateX(user=user))
    y = coordinates_y_collection().find_one(UserCoordinateY(user=user))
    if x is None or y is None:
        return None
    return x["x"], y["y"]


def set_user_coordinates(user: int, coordinates: Tuple[int, int]) -> None:
    """Set a user's coordinates in the database."""
    coordinates_x_collection().update_one(
        {"user": user},
        {"$set": {"x": coordinates[0]}},
        upsert=True
    )
    coordinates_y_collection().update_one(
        {"user": user},
        {"$set": {"y": coordinates[1]}},
        upsert=True
    )
