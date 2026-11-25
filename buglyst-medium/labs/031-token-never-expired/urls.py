from django.urls import path

from views import issue_session, me

urlpatterns = [
    path("sessions", issue_session),
    path("me", me),
]
