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
    creator_name = serializers.SerializerMethodField()
    class Meta:
        model = models.Expense
        fields = ['title',
                  'creator_name']

    def get_creator_name(self, obj):
        return obj.creator.name

class IndividualExpenseSerializer(serializers.ModelSerializer):
    expense = ExpenseSerializer2()
    user_name = serializers.SerializerMethodField()
    class Meta:
        model = models.UserExpense
        fields = ['expense',
                  'user_name',
                  'amount_owed',
                  'percentage_owed']

    def get_user_name(self, obj):
        return obj.user.name


class UserExpenseSerializer2(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    class Meta:
        model = models.UserExpense
        fields = ['user_name', 'amount_owed', 'percentage_owed']

    def get_user_name(self, obj):
        return obj.user.name


class ExpenseDetailSerializer(serializers.ModelSerializer):
    user_expenses = UserExpenseSerializer2(source='userexpenses', many=True)
    creator_name = serializers.SerializerMethodField()

    class Meta:
        model = models.Expense
        fields = ['title', 'creator_name', 'amount', 'split_type', 'date_created', 'user_expenses']

    def get_creator_name(self, obj):
        return obj.creator.name