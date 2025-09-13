from django.urls import path
from .apps import UsersConfig
from .views import PaymentListView

app_name = UsersConfig.name

urlpatterns = [
    path('payments/', PaymentListView.as_view(), name='payment_list'),
]
