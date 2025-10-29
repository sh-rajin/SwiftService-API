from django.urls import path, include
from .views import ServiceListCreateAPIView, ServiceDetailAPIView, TopRatedServiceAPIView, ServiceReviewAPIView, ServiceReviewDetailAPIView

urlpatterns = [
    path('', ServiceListCreateAPIView.as_view(), name='service-list'),
    path('<int:pk>/', ServiceDetailAPIView.as_view(), name='service-detail'),
    path('top-rated/', TopRatedServiceAPIView.as_view(), name='top-service'),
    # path('<int:pk>/reviews/', ServiceReviewAPIView.as_view(), name='service_review'),
    # path('<int:pk>/reviews/<int:review_id>/', ServiceReviewDetailAPIView.as_view(), name='review_details')
]