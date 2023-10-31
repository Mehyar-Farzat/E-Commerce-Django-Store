from django.db import models

# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=100)
    subtitle = models.TextField()
    address = models.TextField(max_length=100)
    call_us = models.CharField(max_length=20)
    email_us = models.CharField(max_length=300)
    logo = models.ImageField(upload_to="logo/")
    emails = models.TextField(max_length=500)
    phones = models.TextField(max_length=100)
    fb_link = models.URLField(null=True,blank=True)
    tw_link = models.URLField(null=True,blank=True)
    yt_link = models.URLField(null=True,blank=True)
    app_description = models.CharField(max_length=300, null=True,blank=True)
    android_app = models.URLField(null=True,blank=True)
    ios_app = models.URLField(null=True,blank=True)
    
    

    def __str__(self):
        return self.name




class Deliveryfee(models.Model):
    fee = models.FloatField()

    def __str__(self):
        return str(self.fee)

    
        
    