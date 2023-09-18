from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=120)
    image = models.ImageField(upload_to='product')
    price = models.FloatField()
    flag = models.CharField(max_length=10, choices=FLAG_CHOICES)
    brand = models.ForeignKey('Brand', on_delete= SET_NULL, related_name=product_brand, null=True, blank=True)
    sku = models.CharField(max_length=50)
    subtitle = models.CharField(max_length=200)
    description = models.TextField(max_length=50000)
    tags = TaggableManager()
    video_url = models.URLField(null=True,blank=True)






