from django.db import models
from django.db.models.deletion import CASCADE


# Create your models here.

class Account(models.Model):
    user_id = models.CharField(primary_key=True, max_length=50, default=False)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, default=True)

class Images(models.Model):
    image_id = models.AutoField(primary_key=True)
    # user = models.ForeignKey(Account, on_delete=models.CASCADE)
    images = models.CharField(max_length=100)