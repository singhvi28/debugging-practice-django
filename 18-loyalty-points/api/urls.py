from django.urls import path

from api import views

urlpatterns = [
    path("accounts", views.list_accounts),
    path("accounts/<str:account_id>", views.get_account),
    path("accounts/<str:account_id>/balance", views.get_balance),
    path("accounts/<str:account_id>/earn", views.earn_points),
    path("points/redeem", views.redeem_points),
    path("accounts/<str:account_id>/ledger", views.get_ledger),
]
