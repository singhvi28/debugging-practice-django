from django.db import models


class Course(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    title = models.CharField(max_length=255)
    instructor = models.CharField(max_length=255)
    max_students = models.IntegerField(default=30)

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    student_email = models.EmailField()
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_email} in {self.course.title}"
