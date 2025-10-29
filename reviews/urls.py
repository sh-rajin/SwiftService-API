from django.urls import path, include
from .views import ReviewDetailAPIView, ReviewListAPIView, ServiceReviewCreateAPIView

urlpatterns = [
    path('', ReviewListAPIView.as_view(), name='review-list'),
    path('service/<int:service_id>', ServiceReviewCreateAPIView.as_view(), name='review-list'),
    path('<int:pk>/', ReviewDetailAPIView.as_view(), name='review-detail')
]