from django.urls import path
from .views import *

urlpatterns = [
    path('list/', BookingListAPIView.as_view(), name='booking-list'),
    path('', BookingCreateAPIView.as_view(), name='booking-create'),
    path('stripe/webhook/', StripeWebhookView.as_view(), name='stripe-webhook'),
    path('payment-success/', PaymentSuccessView.as_view(), name='payment-success'),
    path('payment-cancel/', PaymentCancelView.as_view(), name='payment-cancel'),
]