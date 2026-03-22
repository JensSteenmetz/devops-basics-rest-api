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
    return str(result.inserted_id), 200


def get_by_id(student_id=None, subject=None):
    student = student_db.find_one({
        "_id": ObjectId(student_id)
    })
    if not student:
        return 'not found', 404

    student['student_id'] = str(student['_id'])
    student.pop('_id', None)
    return student, 200


def delete(student_id=None):
    student = student_db.find_one({
        "_id": ObjectId(student_id)
    })
    if not student:
        return 'not found', 404

    student_db.delete_one({
        "_id": ObjectId(student_id)
    })
    return student_id, 200


def get_average_grade(student_id=None):
    student = student_db.find_one({
        "_id": ObjectId(student_id)
    })
    if not student:
        return "Student not found", 404

    grade_records = student.get("grade_records", [])

    total = 0
    count = 0

    for record in grade_records:
        grade = record.get("grade")
        if grade is not None:
            total += grade
            count += 1

    if count == 0:
        return 0, 200

    average = total / count

    return average, 200

def get_subject_grade(student_id=None, subject=None):
    if not student_id or not subject:
        return "student_id and subject are required", 400

    student = student_db.find_one({
        "_id": ObjectId(student_id)
    })
    if not student:
        return "Student not found", 404

    grade_records = student.get("grade_records", [])

    for record in grade_records:
        if record.get("subject_name") == subject:
            return record.get("grade"), 200

    return {"message": f"Grade for subject '{subject}' not found"}, 404