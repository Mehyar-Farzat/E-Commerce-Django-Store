from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from products.models import Product
from utils.generate_code import generate_code


ORDER_STATUS = (

    ('Recieved' , 'Recieved'),
    ('Processed' , 'Processed'),
    ('shipped' , 'Shipped'),
    ('Deliverd' , 'Deliverd'),

)


class Order(models.Model):
    user = models.ForeignKey(User, related_name='order_owner', on_delete=models.SET_NULL,null=True,blank=True)
    status = models.CharField(max_length=15, choices=ORDER_STATUS, default='Recieved')
    code = models.CharField(max_length=8, default=generate_code)
    order_time = models.DateTimeField(default=timezone.now)
    delivery_time = models.DateTimeField(null=True, blank=True)



class OrderDetail(models.Model):
    order = models.ForeignKey(Order, related_name='order_detail', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='orderdetail_product', on_delete= models.SET_NULL, null=True,blank=True)
    quantity = models.IntegerField()
    price = models.FloatField()
    total = models.FloatField()

