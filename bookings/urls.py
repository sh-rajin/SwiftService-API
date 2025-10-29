from django.urls import path
from .views import BookingListAPIView, StripeWebhookView, BookingCreateAPIView

urlpatterns = [
    path('list/', BookingListAPIView.as_view(), name='booking-list'),
    path('', BookingCreateAPIView.as_view(), name='booking-create'),
    path('stripe/webhook/', StripeWebhookView.as_view(), name='stripe-webhook'),
]