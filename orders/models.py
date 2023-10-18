from django.db import models
from django.contrib.auth.models import User


ORDER_STATUS = (

    ('Recieved') , ('Recieved'),
    ('Processed') , ('Processed'),
    ('shipped') , ('Shipped'),
    ('Deliverd') , ('Deliverd'),

)


class Order(models.Model):
    user = models.ForeignKey(User, related_name='order_owner', on_delete=models.SET_NULL,null=True,blank=True)
    status = models.CharField(max_length=15, choices=ORDER_STATUS, default='Recieved')
    