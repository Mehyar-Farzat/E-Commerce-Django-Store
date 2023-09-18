from django.contrib import admin
from .models import Product, ProductImage, Brand, Review

# Register your models here.

admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Brand)
admin.site.register(Review)
