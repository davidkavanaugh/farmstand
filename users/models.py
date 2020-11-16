from django.db import models
from django_s3_storage.storage import S3Storage
import re
from django.conf import settings
from PIL import Image


class UserManager(models.Manager):
    def signup_validator(self, postData, files):
        errors = {}
        FIRST_NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
        LAST_NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
        FARM_NAME_REGEX = re.compile(r'^[0-9a-zA-Z\'\s]+$')
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        PASSWORD_REGEX = re.compile(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&/])[A-Za-z\d$@$!%*?&]{8,}")
        STREET_REGEX = re.compile(r'^[0-9a-zA-Z.\'\s]+$')
        CITY_REGEX = re.compile(r'^[a-zA-Z.\'\s]+$')
        STATE_REGEX = re.compile(r'[A-Z]{2}')
        ZIP_REGEX = re.compile(r'^\d{5}$')
        if not FIRST_NAME_REGEX.match(postData['first_name']):
            errors['first_name'] = "Valid first name required"
        if not LAST_NAME_REGEX.match(postData['last_name']):
            errors['last_name'] = "Valid last name required"
        if not FARM_NAME_REGEX.match(postData['farm_name']):
            errors['farm_name'] = "Valid farm name required"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Valid email required"
        if not PASSWORD_REGEX.match(postData["password_1"]):
            errors['password'] = "Password too weak"
        if not STREET_REGEX.match(postData['street_1']):
            errors['street'] = "Valid address required"
        if not CITY_REGEX.match(postData['city']):
            errors['city'] = "Valid city/town required"
        if not STATE_REGEX.match(postData['state']):
            errors['state'] = "Valid state required"
        if not ZIP_REGEX.match(postData['zip_code']):
            errors['zip_code'] = "Valid 5 digit zip code required"
        if postData['password_1'] != postData['password_2']:
            errors['password'] = "Passwords must match"
        if len(User.objects.filter(email=postData['email'])) > 0:
            errors['email'] = "User already exists"
        if len(User.objects.filter(farm_name=postData['farm_name'])) > 0:
            errors['farm_name'] = "Farm name already taken"
        if 'image' in files:
            try:
                Image.open(files['image']).verify
                print('Valid image')
            except Exception:
                errors['image'] = "Profile image must be jpeg or png"
                print('Invalid image')
        return errors

    def update_validator(self, postData, files, user_id):
        errors = {}
        FIRST_NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
        LAST_NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
        FARM_NAME_REGEX = re.compile(r'^[0-9a-zA-Z\'\s]+$')
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        PASSWORD_REGEX = re.compile(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&/])[A-Za-z\d$@$!%*?&]{8,}")
        STREET_REGEX = re.compile(r'^[0-9a-zA-Z.\'\s]+$')
        CITY_REGEX = re.compile(r'^[a-zA-Z.\'\s]+$')
        STATE_REGEX = re.compile(r'[A-Z]{2}')
        ZIP_REGEX = re.compile(r'^\d{5}$')   
        if not FIRST_NAME_REGEX.match(postData['first_name']):
            errors['first_name'] = "Valid first name required"
        if not LAST_NAME_REGEX.match(postData['last_name']):
            errors['last_name'] = "Valid last name required"
        if not FARM_NAME_REGEX.match(postData['farm_name']):
            errors['farm_name'] = "Valid farm name required"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Valid email required"       
        if not STREET_REGEX.match(postData['street_1']):
            errors['street'] = "Valid address required"
        if not CITY_REGEX.match(postData['city']):
            errors['city'] = "Valid city/town required"
        if not STATE_REGEX.match(postData['state']):
            errors['state'] = "Valid state required"
        if not ZIP_REGEX.match(postData['zip_code']):
            errors['zip_code'] = "Valid 5 digit zip code required"
        if not postData['email'] == User.objects.get(_id=user_id).email:
            print('attempt change')
            if len(User.objects.filter(email=postData['email'])) > 0:
                errors['email'] = "User already exists"
        if not postData['farm_name'] == User.objects.get(_id=user_id).farm_name:
            if len(User.objects.filter(farm_name=postData['farm_name'])) > 0:
                errors['farm_name'] = "Farm name already taken" 
        if len(postData['password_1']) > 0:
            if not PASSWORD_REGEX.match(postData["password_1"]):
                errors['password'] = "Password too weak"
            if postData['password_1'] != postData['password_2']:
                errors['password'] = "Passwords must match"
        if 'image' in files:
            try:
                Image.open(files['image']).verify
                print('Valid image')
            except Exception:
                errors['image'] = "Profile image must be jpeg or png"
                print('Invalid image')
        return errors

class Address(models.Model):
    street_1 = models.CharField(max_length=255)
    street_2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


aws_storage = S3Storage(aws_s3_bucket_name=settings.AWS_S3_BUCKET_NAME)


class User(models.Model):
    _id = models.CharField(max_length=255, primary_key=True, default='')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    farm_name = models.CharField(max_length=255, default="")
    email = models.CharField(max_length=255, default='')
    password = models.CharField(max_length=255, default="")
    address = models.OneToOneField(
        Address,
        on_delete=models.CASCADE,
        default='',
        related_name="user"
    )
    image = models.ImageField(storage=aws_storage, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
