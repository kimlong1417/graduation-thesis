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