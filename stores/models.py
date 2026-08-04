from django.db import models
from django.contrib.auth.models import User


class Store(models.Model):
    owner=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="stores"
    )
    
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    
    
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

# Create your models here.
