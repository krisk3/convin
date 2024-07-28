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
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("create/user/", views.UserCreateView.as_view(), name="create-user"),
    path("list/user/", views.UserListView.as_view(), name="list-user"),
]