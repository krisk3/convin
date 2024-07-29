"""
Configure models to be managed via django admin panel.
"""
from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Expense)
admin.site.register(models.UserExpense)