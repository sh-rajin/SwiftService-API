from django.urls import path, include
from .views import CategoryListCreateAPIView, CategoryDetailAPIView

urlpatterns = [
    path('', CategoryListCreateAPIView.as_view(), name='category-list'),
    path('<int:pk>/', CategoryDetailAPIView.as_view(), name='category-detail')
]