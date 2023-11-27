from django.db import models  
from django.contrib.auth.models import User    
from utils.generate_code import generate_code 

from django.db.models.signals import post_save       # import post_save signal from django 
from django.dispatch import receiver                 # import receiver from django 

# Create your models here.

class Profile(models.Model):      # create profile model    
    user = models.OneToOneField(User,related_name='user_profile', on_delete=models.CASCADE)   # create one to one relationship with user model 
    image = models.ImageField(upload_to='accounts')                                         # add image field 
    code = models.CharField(max_length=10, default=generate_code)                           # add code field 

@receiver(post_save, sender=User)                                               # receiver decorator to receive post_save signal from user model
def create_profile(sender, instance, created, **kwargs):                        # create profile function 
    if created:                                                                 # check if user is created 
        Profile.objects.create(                                                 # create profile for user
            
            user=instance                
            
        )                                   



NUMBER_TYPES = (             

    ('Primary','Primary'),
    ('Secondary','Secondary'),
)

class ContactNumbers(models.Model):        
    user = models.ForeignKey(User,related_name='user_phones', on_delete=models.CASCADE)      
    number = models.CharField(max_length=20)
    type = models.CharField(max_length=20, choices=NUMBER_TYPES)    


ADDRESS_TYPES = (

    ('Home','Home'),
    ('Office','Office'),
    ('Bussines','Bussines'),
    ('Academy','Academy'),
    ('Other','Other'),
)


class Address(models.Model):
    user = models.ForeignKey(User,related_name='user_address', on_delete=models.CASCADE) 
    type = models.CharField(max_length=20, choices=ADDRESS_TYPES)
    address = models.CharField(max_length=150)     
    