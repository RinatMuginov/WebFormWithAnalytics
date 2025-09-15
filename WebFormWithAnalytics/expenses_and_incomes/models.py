from django.db import models
from decimal import Decimal
from django.conf import settings

class Category(models.Model):
    categoryName = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=[('income', 'Доход'), ('expense', 'Расход')])  # Тип: доход/расход

    def __str__(self):
        return self.categoryName
    
class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    comment = models.CharField(max_length=255, blank=True)
    transaction_type = models.CharField(max_length=10, choices=[('income','Доход'),('expense','Расход')])
    total_balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} {self.amount} — {self.category}"