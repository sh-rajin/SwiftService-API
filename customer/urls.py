from django.urls import path, include
from .views import CustomerListAPIView

urlpatterns = [
    path('', CustomerListAPIView.as_view(), name='customer-list'),
]