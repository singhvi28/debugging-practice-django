from django.urls import path

from views import call_upstream, get_budget

urlpatterns = [
    path("call/<str:caller_id>", call_upstream),
    path("budget", get_budget),
]
