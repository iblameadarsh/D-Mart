from django.db import models
from django.contrib.auth.models import User
from D_Mart.utils import CAT_CHOICES


# from django.contrib.auth import get_user_model
# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(max_length=512)
    price = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    # listed_at= models.DateField()
    image = models.ImageField(default='default.jpg', upload_to='images')
    category = models.CharField(max_length=12, choices=CAT_CHOICES, default='Others')

    def __str__(self):
        return self.name
