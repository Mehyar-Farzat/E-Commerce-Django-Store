from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.utils.text import slugify

# Create your models here.

FLAG_CHOICES = (

    ('Sale','Sale'),
    ('Feature', 'Feature'),
    ('New', 'New'),
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
    quantity = models.IntegerField()
    tags = TaggableManager()
    video_url = models.URLField(null=True,blank=True)
    slug = models.SlugField(null=True,blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs ):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_image')
    image = models.ImageField(upload_to='product_images')


class Brand(models.Model):
    name = models.CharField(max_length=120)
    image = models.ImageField(upload_to='brands')
    slug = models.SlugField(null=True,blank=True)

    def __str__(self):
        return self.name


    def save(self, *args, **kwargs ):
        self.slug = slugify(self.name)
        super(Brand, self).save(*args, **kwargs)
        


class Review(models.Model):
    user = models.ForeignKey(User, on_delete= models.SET_NULL, null=True, blank=True, related_name='review_user')  
    product = models.ForeignKey(Product, on_delete=models.CASCADE , related_name='review_product')
    review = models.TextField(max_length=500)
    rate = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)

   
    def __str__(self):
        return str(self.product) + ": " + str(self.review)

    # def __str__(self):    another way to return str for both ( product & review ) 
        #return f"{self.product }  {self.review}"