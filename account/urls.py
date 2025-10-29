from django.urls import path, include
from .views import *

urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name="register"),
    path('login/', LoginAPIView.as_view(), name="login"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
    path('activate/<uidb64>/<token>/', activate, name="activate"),
    path('users/', UsersListAPIView.as_view(), name='users-list'),
    path('users/<int:pk>/', UserDetailsAPIView.as_view(), name='user-details'),
    path('change-password/', ChangePassword.as_view(), name='change-password'),
]