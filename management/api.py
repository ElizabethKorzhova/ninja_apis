"""This module contains API routes for management application."""
from typing import List, Tuple

from django.db.models import Avg, QuerySet
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import Router

from .models import Course, Enrollment, ExamResult, Student
from .schemas import (
    CourseAverageOut,
    CourseIn,
    CourseOut,
    CourseUpdate,
    EnrollmentIn,
    EnrollmentOut,
    ExamResultIn,
    StudentIn,
    StudentOut,
    StudentUpdate,
)

router = Router(tags=["Student Course Management"])


@router.get("/students/", response=List[StudentOut])
def get_students(request: HttpRequest) -> QuerySet[Student]:
    """Gets authenticated user's students."""
    return Student.objects.filter(owner=request.user).order_by("last_name", "first_name")


@router.get("/students/{student_id}", response={200: StudentOut})
def get_student(request: HttpRequest, student_id: int) -> Student:
    """Gets one student by id."""
    return get_object_or_404(Student, id=student_id, owner=request.user)


@router.post("/students/", response={201: StudentOut})
def create_student(request: HttpRequest, payload: StudentIn) -> Tuple[int, Student]:
    """Creates a new student."""
    student = Student.objects.create(owner=request.user, **payload.dict())
    return 201, student


@router.patch("/students/{student_id}", response={200: StudentOut})
def update_student(
    request: HttpRequest,
    student_id: int,
    payload: StudentUpdate,
) -> Student:
    """Partially updates student by id."""
    student = get_object_or_404(Student, id=student_id, owner=request.user)

    for field, value in payload.dict(exclude_unset=True).items():
        setattr(student, field, value)

    student.save()
    return student


@router.delete("/students/{student_id}", response={204: None})
def delete_student(request: HttpRequest, student_id: int) -> Tuple[int, None]:
    """Deletes student by id."""
    student = get_object_or_404(Student, id=student_id, owner=request.user)
    student.delete()
    return 204, None


@router.get("/courses/", response=List[CourseOut])
def get_courses(request: HttpRequest) -> QuerySet[Course]:
    """Gets authenticated user's courses."""
    return Course.objects.filter(owner=request.user).order_by("title")


@router.get("/courses/{course_id}", response={200: CourseOut})
def get_course(request: HttpRequest, course_id: int) -> Course:
    """Gets one course by id."""
    return get_object_or_404(Course, id=course_id, owner=request.user)


@router.post("/courses/", response={201: CourseOut})
def create_course(request: HttpRequest, payload: CourseIn) -> Tuple[int, Course]:
    """Creates a new course."""
    course = Course.objects.create(owner=request.user, **payload.dict())
    return 201, course


@router.patch("/courses/{course_id}", response={200: CourseOut})
def update_course(
    request: HttpRequest,
    course_id: int,
    payload: CourseUpdate,
) -> Course:
    """Partially updates course by id."""
    course = get_object_or_404(Course, id=course_id, owner=request.user)

    for field, value in payload.dict(exclude_unset=True).items():
        setattr(course, field, value)

    course.save()
    return course


@router.delete("/courses/{course_id}", response={204: None})
def delete_course(request: HttpRequest, course_id: int) -> Tuple[int, None]:
    """Deletes course by id."""
    course = get_object_or_404(Course, id=course_id, owner=request.user)
    course.delete()
    return 204, None


@router.post("/enrollments/", response={201: EnrollmentOut})
def enroll_student(
    request: HttpRequest,
    payload: EnrollmentIn,
) -> Tuple[int, Enrollment]:
    """Enrolls student to course."""
    student = get_object_or_404(Student, id=payload.student_id, owner=request.user)
    course = get_object_or_404(Course, id=payload.course_id, owner=request.user)
    enrollment, _ = Enrollment.objects.get_or_create(student=student, course=course)
    return 201, enrollment


@router.get("/enrollments/", response=List[EnrollmentOut])
def get_enrollments(request: HttpRequest) -> QuerySet[Enrollment]:
    """Gets authenticated user's enrollments."""
    return Enrollment.objects.select_related(
        "student",
        "course",
        "exam_result",
    ).filter(
        student__owner=request.user,
        course__owner=request.user,
    )


@router.post("/enrollments/{enrollment_id}/grade/", response={200: EnrollmentOut})
def grade_student(
    request: HttpRequest,
    enrollment_id: int,
    payload: ExamResultIn,
) -> Enrollment:
    """Creates or updates exam result for enrollment."""
    enrollment = get_object_or_404(
        Enrollment.objects.select_related("student", "course"),
        id=enrollment_id,
        student__owner=request.user,
        course__owner=request.user,
    )
    ExamResult.objects.update_or_create(
        enrollment=enrollment,
        defaults={"grade": payload.grade},
    )
    enrollment.refresh_from_db()
    return enrollment


@router.get("/courses/{course_id}/average-grade/", response={200: CourseAverageOut})
def get_course_average(request: HttpRequest, course_id: int) -> CourseAverageOut:
    """Calculates average grade for course."""
    course = get_object_or_404(Course, id=course_id, owner=request.user)
    average_grade = course.enrollments.aggregate(
        average=Avg("exam_result__grade"),
    )["average"]
    return CourseAverageOut(course_id=course.id, average_grade=average_grade)
