from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
import uuid
import secrets
from django.contrib.auth.hashers import make_password, check_password
from decimal import Decimal

# Create your models here.

class Item(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class UserDetails(models.Model):
    user_id = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ]
    )
    profile_img = models.URLField(null=True, blank=True)
    age = models.IntegerField(
        validators=[
            MinValueValidator(1, message="Age must be at least 1"),
            MaxValueValidator(150, message="Age cannot be more than 150")
        ]
    )
    bank_account_name = models.CharField(max_length=100)
    token = models.CharField(max_length=64, unique=True, null=True)
    password = models.CharField(max_length=128)  # Using 128 chars for hashed password

    def save(self, *args, **kwargs):
        if not self.user_id:
            self.user_id = uuid.uuid4().hex[:8].upper()
        if not self.token:
            self.token = secrets.token_hex(32)
        # Hash password if it's not already hashed
        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.name} ({self.user_id})"

    class Meta:
        verbose_name = 'User Detail'
        verbose_name_plural = 'User Details'

class TransactionDetails(models.Model):
    TRANSACTION_TYPES = [
        ('INCOME', 'Income'),
        ('EXPENSE', 'Expense'),
        ('TRANSFER', 'Transfer'),
        ('REFUND', 'Refund'),
    ]

    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='transaction_details', to_field='user_id')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    transaction_type = models.CharField(max_length=8, choices=TRANSACTION_TYPES)
    description = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)  # e.g., 'Food', 'Transport', 'Salary'
    date = models.DateTimeField(auto_now_add=True)
    is_recurring = models.BooleanField(default=False)
    recurring_frequency = models.CharField(max_length=20, blank=True, null=True)  # e.g., 'monthly', 'weekly'
    
    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Transaction Details'

    def __str__(self):
        return f"{self.user.name} - {self.amount} ({self.transaction_type})"
