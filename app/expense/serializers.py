"""
Serialzers for the expense app.
"""

from rest_framework import serializers
from . import models
from . import validators

class UserExpenseSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=50, required=False, allow_blank=True)
    mobile = serializers.CharField(max_length=10, required=False, allow_blank=True)
    class Meta:
        model = models.UserExpense
        fields = ['expense',
                  'user',
                  'email',
                  'mobile',
                  'amount_owed',
                  'percentage_owed']
        read_only_fields = ['expense', 'user']


class ExpenseSerializer(serializers.ModelSerializer):
    user_expense = UserExpenseSerializer(many=True)
    class Meta:
        model = models.Expense
        fields = ['amount',
                  'split_type',
                  'title',
                  'creator',
                  'user_expense',]
        read_only_fields = ['creator']


class ExpenseSerializer2(serializers.ModelSerializer):
    class Meta:
        model = models.Expense
        fields = ['title',
                  'creator']

class IndividualExpenseSerializer(serializers.ModelSerializer):
    expense = ExpenseSerializer2()
    class Meta:
        model = models.UserExpense
        fields = ['expense',
                  'user',
                  'amount_owed',
                  'percentage_owed']

