from django.db import models  
from django.contrib.auth.models import User    
from utils import generate_code    

# Create your models here.

class Profile(models.Model):      # create profile model    
    user = models.OneToOneField(User,related_name=user_profile, on_delete=models.CASCADE)   # create one to one relationship with user model 
    image = models.ImageField(upload_to='accounts')                                         # add image field 
    code = models.CharField(max_length=10, default=generate_code)                           # add code field 
