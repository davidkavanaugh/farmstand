from django.db import models
from users.models import User
from django_s3_storage.storage import S3Storage
from django.conf import settings
import re
from PIL import Image

aws_storage = S3Storage(aws_s3_bucket_name=settings.AWS_S3_BUCKET_NAME)

class ProductManager(models.Manager):
    def product_validator(self, postData, files):
        errors = {}
        NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
        DESCRIPTION_REGEX = re.compile(r'^[0-9a-zA-Z\!\-\$\/\\,\'\s]+$')
        UNIT_REGEX = re.compile(r'^[a-zA-Z]+$')
        PRICE_REGEX = re.compile(r'(0\.((0[1-9]{1})|([1-9]{1}([0-9]{1})?)))|(([1-9]+[0-9]*)(\.([0-9]{1,2}))?)')
        QUANTITY_REGEX = re.compile(r'^[0-9]+$')
        if not NAME_REGEX.match(postData['product_name']):
            errors['product_name'] = "please enter a valid name"
        if not DESCRIPTION_REGEX.match(postData['product_description']):
            errors['product_description'] = "Please enter a valid description"
        if not UNIT_REGEX.match(postData['product_unit']):
            errors['product_unit'] = "Please enter a unit of measurement"
        if not PRICE_REGEX.match(postData['product_price']):
            errors['product_price'] = "Please enter a valid price"
        if not QUANTITY_REGEX.match(postData['product_quantity']):
            errors['product_quantity'] = "Please enter a quanitty"
        if 'image' in files:
            try:
                Image.open(files['image']).verify
                print('Valid image')
            except Exception:
                errors['image'] = "Image must be jpeg or png"
                print('Invalid image')
        else:
            errors['product_image'] = "Please include an image"
        return errors

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
    objects = ProductManager()
