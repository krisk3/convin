"""
URL configuration for app project.
"""
from django.urls import path, include
from . import views

urlpatterns = [
    path("create/expense/", views.ExpenseCreateView.as_view(), name="create-expense"), # Create a new expense
    path('user/expenses/', views.IndividualExpenseView.as_view(), name='user-expenses'),  # List all the expenses of a user
    path('user/overall-expenses/', views.ExpenseDetailView.as_view(), name='user-overall-expenses'), # List all the expenses by a user
    path('balance-sheet/', views.BalanceSheetPDFView.as_view(), name='balance-sheet-pdf'), # Downloaded balance sheet in PDF format
]