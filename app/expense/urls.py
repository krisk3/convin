"""
URL configuration for app project.
"""
from django.urls import path, include
from . import views

urlpatterns = [
    path("create/expense/", views.ExpenseCreateView.as_view(), name="create-expense"),
]