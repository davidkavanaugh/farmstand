from django.db import models
from cart.models import CartItem

class Order(models.Model):
    items = models.ManyToManyField(Product, related_name="orders", on_delete=models.CASCADE)
    total = 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)