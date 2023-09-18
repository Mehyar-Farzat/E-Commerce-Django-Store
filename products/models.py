from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

# Create your models here.

FLAG_CHOICES = (

    ('sale','sale'),
    ('feature', 'feature'),
    ('new', 'new'),
)



class Product(models.Model):
    name = models.CharField(max_length=120)
    image = models.ImageField(upload_to='product')
    price = models.FloatField()
    flag = models.CharField(max_length=10, choices=FLAG_CHOICES)
    brand = models.ForeignKey('Brand', on_delete=models.SET_NULL , related_name='product_brand', null=True, blank=True)
    sku = models.CharField(max_length=50)
    subtitle = models.CharField(max_length=200)
    description = models.TextField(max_length=50000)
    tags = TaggableManager()
    video_url = models.URLField(null=True,blank=True)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_image')
    image = models.ImageField(upload_to='product_images')


class Brand(models.Model):
    name = models.CharField(max_length=120)
    image = models.ImageField(upload_to='brands')


class Review(models.Model):
    user = models.ForeignKey(Review, on_delete= models.SET_NULL, null=True, blank=True, related_name='review_user')  
    product = models.ForeignKey(Product, on_delete=models.CASCADE , related_name='review_product')
    review = models.TextField(max_length=500)
    rate = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)