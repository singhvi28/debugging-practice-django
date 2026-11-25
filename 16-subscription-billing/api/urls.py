from django.urls import path

from api import views

urlpatterns = [
    path("plans", views.plans_collection),
    path("plans/<str:plan_id>", views.get_plan),
    path("plans/<str:plan_id>/price", views.update_plan_price),
    path("subscriptions", views.subscribe),
    path("subscriptions/<str:subscription_id>", views.get_subscription),
    path("subscriptions/<str:subscription_id>/cancelled", views.cancel_subscription),
]
