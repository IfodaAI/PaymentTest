# models.py
from django.db import models
from django.utils import timezone

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Kutilmoqda'),
        ('paid', 'To\'langan'),
        ('cancelled', 'Bekor qilingan'),
        ('delivered', 'Yetkazilgan'),
    )

    product_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.id} - {self.product_name} ({self.amount})-{self.status}"