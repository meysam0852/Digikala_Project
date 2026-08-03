from django.db import models
from django.contrib.auth.models import User
from products.models import Product

# Create your models here.

class CartItem(models.Model):
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )
    Product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )
    
    quantity = models.PositiveBigIntegerField(default=1)
    
    def __str__(self):
        return f"{self.customer.username} - {self.product.name}"
