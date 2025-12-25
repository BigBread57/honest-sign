from django.urls import path
from order.views.order import (
    OrderListView,
    OrderDetailView, OrderCreateView
)
from order.views.user import RegistrationView, LoginView, LogoutView

urlpatterns = [

    path("registration/", RegistrationView.as_view(), name="registration"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("orders/", OrderListView.as_view(), name="order_list"),
    path("orders/create/", OrderCreateView.as_view(), name="order_create"),
    path("orders/<int:id>/", OrderDetailView.as_view(), name="order_detail"),
]