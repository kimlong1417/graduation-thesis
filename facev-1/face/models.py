from email.policy import default
from socket import INADDR_UNSPEC_GROUP
from django.db import models
import uuid

# Create your models here.

class AccountUser(models.Model):
    id_user = models.UUIDField(primary_key=True, default= uuid.uuid4 ,auto_created=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=200)
    email = models.EmailField(max_length=100)
    
    def __str__(self):
        return self.name

class ImageUser(models.Model):
    id_image = models.UUIDField(primary_key=True, default=uuid.uuid1, auto_created=True, serialize=False, verbose_name='ID')
    id_user = models.ForeignKey(AccountUser, on_delete=models.CASCADE)
    image = models.CharField(max_length=200)