"""
URL configuration for app project.
"""
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),   #Create access token and refresh token
    path('token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),  #Refresh access token
    path("create/user/", views.UserCreateView.as_view(), name="create-user"),  # Create a new user
    path("list/user/", views.UserListView.as_view(), name="list-user"),        #List users using their mobile number or email id
]