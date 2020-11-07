from django.db import models


class Address(models.Model):
    street_1 = models.CharField(max_length=255)
    street_2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class User(models.Model):
    id = models.CharField(max_length=255, default='')
    auth0_id = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, default='')
    password = models.CharField(max_length=255, default="")
    address = models.OneToOneField(
        Address,
        on_delete=models.CASCADE,
        primary_key=True,
        default=''
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)