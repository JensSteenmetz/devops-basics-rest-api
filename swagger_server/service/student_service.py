import os
from pymongo import MongoClient
from bson.objectid import ObjectId

mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(mongo_uri)
db = client["student_db"]
student_db = db["students"]


def add(student=None):
    res = student_db.find_one({
        "first_name": student.first_name,
        "last_name": student.last_name
    })
    if res:
        return 'already exists', 409

    result = student_db.insert_one(student.to_dict())
    return str(result.inserted_id)


def get_by_id(student_id=None, subject=None):
    student = student_db.find_one({
        "_id": ObjectId(student_id)
    })
    if not student:
        return 'not found', 404

    student['student_id'] = str(student['_id'])
    student.pop('_id', None)
    return student


def delete(student_id=None):
    student = student_db.find_one({
        "_id": ObjectId(student_id)
    })
    if not student:
        return 'not found', 404

    student_db.delete_one({
        "_id": ObjectId(student_id)
    })
    return student_id