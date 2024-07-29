"""
URL configuration for app project.
"""
from django.urls import path, include
from . import views

urlpatterns = [
    path("create/expense/", views.ExpenseCreateView.as_view(), name="create-expense"),
    path('user/expenses/', views.IndividualExpenseView.as_view(), name='user-expenses'),
    path('user/overall-expenses/', views.ExpenseDetailView.as_view(), name='user-overall-expenses'),
]