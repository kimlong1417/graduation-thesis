from django.db import models

# Create your models here.
class member(models.Model):
    firstname = models.CharField(max_length=50, null=False, blank=False)
    lastname = models.CharField(max_length=50, null=False, blank=False)
    username = models.CharField(max_length=50, null=False, blank=False)
    password = models.UUIDField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=50, null=False, blank=False)
    phone = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.firstname
    