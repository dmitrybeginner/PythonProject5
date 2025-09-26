from django.urls import path
from rest_framework.routers import DefaultRouter

from .apps import UsersConfig
from .views import (PaymentCreateAPIView, PaymentListView, SubscriptionAPIView,
                    UserViewSet)

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"", UserViewSet, basename="users")

urlpatterns = [
    path("payments/", PaymentListView.as_view(), name="payment_list"),
    path("payments/create/", PaymentCreateAPIView.as_view(), name="payment_create"),
    path("subscriptions/", SubscriptionAPIView.as_view(), name="subscriptions"),
] + router.urls
