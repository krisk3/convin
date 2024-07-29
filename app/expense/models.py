from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from . import validators

User = get_user_model()

# Create your models here.
class Expense(models.Model):
    """

    """
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(1.0)])
    split_type = models.CharField(max_length=10, choices=validators.SPLIT_CHOICES, default='equal')
    title = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Expense"
        verbose_name_plural = "Expenses"

    def __str__(self):
        return f"{self.title} - {self.amount}"


class UserExpense(models.Model):
    """

    """
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='userexpenses')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userexpenses')
    amount_owed = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0.01)])
    percentage_owed = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])

    class Meta:
        verbose_name = "User Expense"
        verbose_name_plural = "User Expenses"

    def __str__(self):
        return f"{self.user.name} - {self.amount_owed}"