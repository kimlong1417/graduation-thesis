from django.db import models

# Create your models here.

class Account(models.Model):
    id_user = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, default=True)

class Image(models.Model):
    image = models.ImageField()
    # image_base64 = models.CharField(max_length=10000)

class Upload_Image(models.Model):
    # id_user = models.ForeignKey(Account, on_delete=models.CASCADE)
    image = models.ImageField()

class ObjectMatching_Image(models.Model):
    # id_user = models.ForeignKey(Account, on_delete=models.CASCADE)
    image = models.ImageField()

class Compare_Image(models.Model):
    # id_user = models.ForeignKey(Account, on_delete=models.CASCADE)
    image = models.ImageField()

class Compare_Image2(models.Model):
    # id_user = models.ForeignKey(Account, on_delete=models.CASCADE)
    image = models.ImageField()

class FileUpload(models.Model):
    file = models.FileField(upload_to='fileUpload/%Y/%m/%d')
    description = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)