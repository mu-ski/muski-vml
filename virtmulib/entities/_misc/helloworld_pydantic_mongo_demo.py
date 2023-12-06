import pymongo
from pydantic import BaseModel, Field
from typing import Optional

from virtmulib.entities.py_object_id import PyObjectId


class Sandwich(BaseModel):
    # The primary key for the StudentModel, stored as a `str` on the instance.
    # This will be aliased to `_id` when sent to MongoDB,
    # but provided as `id` in the API requests and responses.
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str


def demo_pydantic_mongo() -> None:
    client = pymongo.MongoClient("localhost", 27017)

    db = client.test
    db.name  # => test
    mycoll = db.my_collection_2

    s1 = Sandwich(name="Magnoona!")
    s2 = Sandwich(name="Cheese Sandwich")
    s3 = Sandwich(name="Super spicy chicken")

    db.my_collection_2.insert_one(s1.model_dump(by_alias=True, exclude=["id"]))
    db.my_collection.insert_one(s2.model_dump(by_alias=True, exclude=["id"]))
    db.my_collection.insert_one(s3.model_dump(by_alias=True, exclude=["id"]))

    db.my_collection_2.find_one()

    for i in db.my_collection_2.find():
        print(i["name"])

    db.my_collection_2.create_index("name")

    for i in db.my_collection_2.find().sort("name", pymongo.ASCENDING):
        print(i["name"])
