from django.db import models
from django.contrib.auth.models import User

from BuyNow.models import Product


# Create your models here.
class Comments(models.Model):
    product = models.ForeignKey(Product, related_name='comment', on_delete=models.CASCADE, null=True, blank=True)
    comment = models.TextField(max_length=512)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.product.name , self.user)
    