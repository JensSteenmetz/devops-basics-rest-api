from swagger_server.service.student_service import *

import connexion
import six

from swagger_server.models.student import Student  # noqa: E501
from swagger_server import util


def add_student(body=None):  # noqa: E501
    """Add a new student

    Adds an item to the system # noqa: E501

    :param body: Student item to add
    :type body: dict | bytes

    :rtype: str
    """
    if connexion.request.is_json:
        body = Student.from_dict(connexion.request.get_json())  # noqa: E501
        return add(body)
    return 500,'error'


def delete_student(student_id):  # noqa: E501
    """Deletes a student

    Delete a single student by ID  # noqa: E501

    :param student_id: the uid
    :type student_id: 

    :rtype: object
    """
    return delete(student_id)


def get_student_by_id(student_id):  # noqa: E501
    """gets student

    Returns a single student # noqa: E501

    :param student_id: the uid
    :type student_id: 

    :rtype: Student
    """
    return get_by_id(student_id)


def get_student_average(student_id):
    """Gets average grade of student

    Returns the average grade of a given student.

    :param student_id: the uid
    :type student_id:

    :rtype: float
    """
    return get_average_grade(student_id)


def get_student_grade(student_id, subject):
    """Gets grade of student for subject

    Returns the grade of a given student and subject.

    :param student_id: the uid
    :type student_id:

    :param subject: the subject name
    :type subject:

    :rtype: float
    """
    return get_subject_grade(student_id, subject)
