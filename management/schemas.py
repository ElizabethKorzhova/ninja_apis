"""This module contains schemas for management API."""
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from ninja import Schema


class StudentIn(Schema):
    """Represents schema for student creation."""
    first_name: str
    last_name: str
    email: str
    enrolled_at: date


class StudentUpdate(Schema):
    """Represents schema for student update."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    enrolled_at: Optional[date] = None


class StudentOut(Schema):
    """Represents schema for student response."""
    id: int
    first_name: str
    last_name: str
    email: str
    enrolled_at: date


class CourseIn(Schema):
    """Represents schema for course creation."""
    title: str
    code: str
    description: str = ""


class CourseUpdate(Schema):
    """Represents schema for course update."""
    title: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None


class CourseOut(Schema):
    """Represents schema for course response."""
    id: int
    title: str
    code: str
    description: str
    created_at: datetime


class EnrollmentIn(Schema):
    """Represents schema for student enrollment."""
    student_id: int
    course_id: int


class ExamResultIn(Schema):
    """Represents schema for grading student."""
    grade: Decimal


class ExamResultOut(Schema):
    """Represents schema for exam result response."""
    id: int
    grade: Decimal
    graded_at: datetime


class EnrollmentOut(Schema):
    """Represents schema for enrollment response."""
    id: int
    student: StudentOut
    course: CourseOut
    enrolled_at: datetime
    exam_result: Optional[ExamResultOut] = None


class CourseAverageOut(Schema):
    """Represents schema for course average grade response."""
    course_id: int
    average_grade: Optional[Decimal] = None
