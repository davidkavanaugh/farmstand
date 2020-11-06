from django.db import models
from sign_up.models import User


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    unit = models.CharField(max_length=255)
    farmer = models.OneToOneField(
        User, related_name="farmer", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
