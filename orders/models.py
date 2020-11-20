from django.db import models
from users.models import User
from products.models import Product
from cart.models import CartItem

class Order(models.Model):
    user = models.ForeignKey(User, related_name="orders", on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem, related_name="orders")
    total = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)