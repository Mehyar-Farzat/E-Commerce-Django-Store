from django.db import models  
from django.contrib.auth.models import User    
from utils import generate_code    

# Create your models here.

class Profile(models.Model):      # create profile model    
    user = models.OneToOneField(User,related_name='user_profile', on_delete=models.CASCADE)   # create one to one relationship with user model 
    image = models.ImageField(upload_to='accounts')                                         # add image field 
    code = models.CharField(max_length=10, default=generate_code)                           # add code field 


NUMBER_TYPES = (

    ('Primary','Primary'),
    ('Secondary','Secondary'),
)

class ContactNumbers(models.Model):
    user = models.ForeignKey(User,related_name='user_phones', on_delete=models.CASCADE)
    number = models.CharField(max_length=20)
    type = models.CharField(max_length=20, choices=NUMBER_TYPES)    