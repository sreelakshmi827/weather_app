from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

# class CustomUser(models.Model):
#     username = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     password= models.CharField(max_length=100)
    
class CustomUser(AbstractUser):  
    def _str_(self):
      return self.username

