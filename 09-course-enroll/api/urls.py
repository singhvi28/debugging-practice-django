from django.urls import path

from api import views

urlpatterns = [
    path("courses", views.courses_collection),
    path("courses/<str:course_id>", views.get_course),
    path("courses/<str:course_id>/enrollments", views.list_enrollments),
    path("courses/<str:course_id>/enroll", views.enroll_student),
    path("enrollments/<str:enrollment_id>", views.delete_enrollment),
]
