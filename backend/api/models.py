from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal

class UserDetails(models.Model):
    user_id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    profile_img = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    age = models.IntegerField()
    bank_account_name = models.CharField(max_length=100)
    token = models.CharField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        verbose_name = 'User Detail'
        verbose_name_plural = 'User Details'

    def __str__(self):
        return self.name

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('INCOME', 'Income'),
        ('EXPENSE', 'Expense'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPES)
    description = models.CharField(max_length=255)
    source = models.CharField(max_length=100)  # e.g., 'Upwork', 'Paypal', 'Youtube', etc.
    source_icon = models.URLField(null=True, blank=True)  # URL to the source's icon
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.source} - {self.amount} ({self.transaction_type})"

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

class Statistics(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='statistics')
    date = models.DateField()
    total_income = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_expense = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Statistics'

    def __str__(self):
        return f"Stats for {self.user.username} on {self.date}"

class TopSpending(models.Model):
    statistics = models.ForeignKey(Statistics, on_delete=models.CASCADE, related_name='top_spending')
    merchant = models.CharField(max_length=100)  # e.g., 'Starbucks'
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()
    merchant_icon = models.URLField(null=True, blank=True)  # URL to the merchant's icon

    class Meta:
        ordering = ['-amount']

    def __str__(self):
        return f"{self.merchant} - {self.amount}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.URLField(null=True, blank=True)
    total_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default='USD')  # e.g., USD, EUR, etc.
    frequently_sent_to = models.ManyToManyField(
        User,
        related_name='sent_to_by',
        blank=True,
        limit_choices_to={'is_active': True}
    )

    def __str__(self):
        return f"Profile for {self.user.username}"

    def update_balance(self):
        """Update total balance based on all transactions"""
        income = self.user.transactions.filter(
            transaction_type='INCOME'
        ).aggregate(total=models.Sum('amount'))['total'] or 0

        expenses = self.user.transactions.filter(
            transaction_type='EXPENSE'
        ).aggregate(total=models.Sum('amount'))['total'] or 0

        self.total_balance = income - expenses
        self.save() 