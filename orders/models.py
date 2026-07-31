from django.db import models
from django.contrib.auth.models import User
from products.models import Product

# Create your models here.

class Order(models.Model):
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders"
    )
    
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Order #{self.id}"