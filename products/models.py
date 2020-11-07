from django.db import models
from users.models import User


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default="")
    price = models.FloatField(default="0.00")
    unit = models.CharField(max_length=255, default="ea")
    quantity = models.IntegerField()
    farmer = models.ForeignKey(
        User, related_name="products", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
