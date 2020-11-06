from django.db import models
from users.models import User


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    unit = models.CharField(max_length=255)
    quantity = models.IntegerField()
    farmer = models.ForeignKey(
        User, related_name="products", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
