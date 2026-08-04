from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    phone = models.CharField(max_length=11, blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.user.username} - Customer"



class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_profile')
    phone = models.CharField(max_length=11, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Seller"


@receiver(post_save, sender=User)
def create_user_profiles(sender, instance, created, **kwrags):
    if created:
        CustomerProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profiles(sender, instance, **kwargs):
    if hasattr(instance, 'customer_profile'):
        instance.customer_profile.save()