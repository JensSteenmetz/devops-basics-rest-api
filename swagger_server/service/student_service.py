import os
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.errors import InvalidId

mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(mongo_uri)
db = client["student_db"]
student_db = db["students"]


def add(student=None):
    if student is None:
        return "invalid input", 400

    # Handle both dict input and model objects
    if hasattr(student, "to_dict"):
        student = student.to_dict()

    first_name = student.get("first_name")
    last_name = student.get("last_name")

    if not first_name or not last_name:
        return "invalid input", 400

    # grade_records is optional in the tests
    if "grade_records" not in student or student["grade_records"] is None:
        student["grade_records"] = []

    existing = student_db.find_one({
        "first_name": first_name,
        "last_name": last_name
    })
    if existing:
        return "already exists", 409

    result = student_db.insert_one(student)
    return str(result.inserted_id), 200


def get_by_id(student_id=None, subject=None):
    if not student_id:
        return "Invalid ID supplied", 400

    try:
        obj_id = ObjectId(student_id)
    except InvalidId:
        return "Invalid ID supplied", 400

    student = student_db.find_one({"_id": obj_id})
    if not student:
        return "not found", 404

    student["student_id"] = str(student["_id"])
    student.pop("_id", None)
    return student, 200


def delete(student_id=None):
    if not student_id:
        return "Invalid ID supplied", 400

    try:
        obj_id = ObjectId(student_id)
    except InvalidId:
        return "Invalid ID supplied", 400

    student = student_db.find_one({"_id": obj_id})
    if not student:
        return "not found", 404

    student_db.delete_one({"_id": obj_id})

    student["student_id"] = str(student["_id"])
    student.pop("_id", None)
    return student, 200


def get_average_grade(student_id=None):
    if not student_id:
        return "Invalid ID supplied", 400

    try:
        obj_id = ObjectId(student_id)
    except InvalidId:
        return "Invalid ID supplied", 400

    student = student_db.find_one({"_id": obj_id})
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
        return "No valid grades found for this student", 404

    average = total / count
    return average, 200


def get_subject_grade(student_id=None, subject=None):
    if not student_id or not subject:
        return "student_id and subject are required", 400

    try:
        obj_id = ObjectId(student_id)
    except InvalidId:
        return "Invalid ID supplied", 400

    student = student_db.find_one({"_id": obj_id})
    if not student:
        return "Student not found", 404

    grade_records = student.get("grade_records", [])

    for record in grade_records:
        if record.get("subject_name") == subject:
            return record.get("grade"), 200

    return f"Grade for subject '{subject}' not found", 404