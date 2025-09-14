from django.urls import path
from .apps import UsersConfig
from .views import PaymentListView, UserViewSet
from rest_framework.routers import DefaultRouter

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'', UserViewSet, basename='users')

urlpatterns = [
    path('payments/', PaymentListView.as_view(), name='payment_list'),
] + router.urls
