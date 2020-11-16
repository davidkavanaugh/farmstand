from django.db import models
from users.models import User
from django_s3_storage.storage import S3Storage
from django.conf import settings


aws_storage = S3Storage(aws_s3_bucket_name=settings.AWS_S3_BUCKET_NAME)


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default="")
    price = models.FloatField(default="0.00")
    unit = models.CharField(max_length=255, default="ea")
    quantity = models.IntegerField()
    farmer = models.ForeignKey(
        User, related_name="products", on_delete=models.CASCADE)
    image = models.ImageField(storage=aws_storage, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
