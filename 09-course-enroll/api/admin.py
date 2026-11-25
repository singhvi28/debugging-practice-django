from django.contrib import admin
from .models import Course, Enrollment


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "instructor", "max_students")
    search_fields = ("title", "instructor")


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("id", "course", "student_email", "enrolled_at")
    search_fields = ("student_email",)
