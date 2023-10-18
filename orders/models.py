from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from utils.generate_code import generate_code


ORDER_STATUS = (

    ('Recieved') , ('Recieved'),
    ('Processed') , ('Processed'),
    ('shipped') , ('Shipped'),
    ('Deliverd') , ('Deliverd'),

)


class Order(models.Model):
    user = models.ForeignKey(User, related_name='order_owner', on_delete=models.SET_NULL,null=True,blank=True)
    status = models.CharField(max_length=15, choices=ORDER_STATUS, default='Recieved')
    code = models.CharField(max_length=8, default=generate_code)
    order_time = models.DateTimeField(default=timezone.now)
    delivery_time = models.DateTimeField(null=True, blank=True)
