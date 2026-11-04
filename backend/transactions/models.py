from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.db.models import Q
from decimal import Decimal

class TransactionType(models.TextChoices):
    INCOME = "INCOME", "Ingreso"
    EXPENSE = "EXPENSE", "Gasto"


class Category(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name = "finance_categories",
    )
    name = models.CharField(max_length = 100)
    category_type = models.CharField(
        max_length = 7,
        choices = TransactionType.choices,
    )
    color = models.CharField(
        max_length = 7,
        default = "#64748b",
        validators = [
            RegexValidator(
                regex = r"^#[0-9A-Fa-f]{6}$",
                message = "Usa un color hexadecimal, ejemplo: #1d4ed8",
            )
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["category_type", "name"]
        constraints = [
            models.UniqueConstraint(
                fields = ["user", "category_type", "name"],
                name = "unique_user_category_type_name",
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.get_category_type_display()})"

class Transaction(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name = "finance_transactions",
    )
    category = models.ForeignKey(
            Category,
            on_delete = models.SET_NULL,
            related_name = "transactions",
            null = True,
            blank = True,
    )
    transactions_type = models.CharField(
        max_length = 7,
        choices = TransactionType.choices,
    )
    amount = models.DecimalField(
        max_digits = 12,
        decimal_places = 2,
        validators = [MinValueValidator(Decimal("0.01"))],
    )
    description = models.CharField(max_length = 255, blank = True)
    transaction_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        ordering = ["-transaction_date", "-created_at"]
        constraints = [
            models.CheckConstraint(
                condition = Q(amount__gt = 0),
                name = "transaction_amount_positive",
            )
        ]
        indexes = [
            models.Index(
                fields = ["user", "transaction_date"],
                name = "txn_user_date_idx",
            )
        ]
    
    def __str__(self):
        return (
            f"{self-get_transaction_type_display()} - "
            f"{self.amount} - {self.transaction_date}"
        )