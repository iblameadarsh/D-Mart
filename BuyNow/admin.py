from django.contrib import admin
from .models import Product

# Register your models here.


class ProductAdmin(admin.ModelAdmin):

    list_display = ("id", "name", "user", "category")
    list_filter = ("category", "user")


admin.site.register(Product, ProductAdmin)


