"""Module containing model definitions for management application."""
from django.contrib.auth.models import User
from django.db import models


class Student(models.Model):
    """Model definition for Student.

        Fields:
            first_name (CharField): required;
            last_name (CharField): required;
            email (EmailField): required;
            enrolled_at (DateField): required;
            owner (ForeignKey): required."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    enrolled_at = models.DateField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="students")

    def __str__(self) -> str:
        """Returns string representation of Student."""
        return f"{self.first_name} {self.last_name}"


class Course(models.Model):
    """Model definition for Course.

        Fields:
            title (CharField): required;
            code (CharField): required;
            description (TextField): optional;
            owner (ForeignKey): required;
            created_at (DateField): auto created date."""
    title = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="courses")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Returns string representation of Course."""
        return self.title


class Enrollment(models.Model):
    """Model definition for Enrollment.

        Fields:
            student (ForeignKey): required;
            course (ForeignKey): required;
            enrolled_at (DateField): auto created date."""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for Enrollment."""
        unique_together = ("student", "course")

    def __str__(self) -> str:
        """Returns string representation of Enrollment."""
        return f"{self.student} -> {self.course}"


class ExamResult(models.Model):
    """Model definition for ExamResult.

        Fields:
            enrollment (OneToOneField): required;
            grade (DecimalField): required;
            graded_at (DateField): auto created date."""
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, related_name="exam_result")
    grade = models.DecimalField(max_digits=4, decimal_places=2)
    graded_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """Returns string representation of ExamResult."""
        return f"{self.enrollment}: {self.grade}"
