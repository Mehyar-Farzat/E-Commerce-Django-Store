from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from products.models import Product
from utils.generate_code import generate_code
import datetime



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
    coupon = models.ForeignKey('Coupon', related_name='order_coupon', on_delete=models.SET_NULL, null=True,blank=True)
    cart_total_discount = models.FloatField(null=True, blank=True)



class OrderDetail(models.Model):
    order = models.ForeignKey(Order, related_name='order_detail', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='orderdetail_product', on_delete= models.SET_NULL, null=True,blank=True)
    quantity = models.IntegerField()
    price = models.FloatField()
    total = models.FloatField()


CART_STATUS = (

    ('Inprogress' , 'Inprogress'),
    ('Completed' , 'Completed'),
    
)

class Cart(models.Model):
    user = models.ForeignKey(User, related_name='cart_owner', on_delete=models.SET_NULL,null=True,blank=True)
    status = models.CharField(max_length=15, choices=CART_STATUS, default='Inprogress')
    coupon = models.ForeignKey('Coupon', related_name='cart_coupon', on_delete=models.SET_NULL, null=True,blank=True)
    cart_total_discount = models.FloatField(null=True, blank=True)


    def cart_total(self):
        total = 0
        for object in self.cart_detail.all():
            total += object.total
        return total

class CartDetail(models.Model):
    cart = models.ForeignKey(Cart, related_name='cart_detail', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cartdetail_product', on_delete= models.SET_NULL, null=True,blank=True)
    quantity = models.IntegerField()
    total = models.FloatField(null=True, blank=True)


    # use save function to calculate the total price
    def save(self, *args, **kwargs):
        self.total = round(self.quantity*self.product.price,2)
        super(CartDetail, self).save(*args, **kwargs)







class Coupon(models.Model):
    code = models.CharField(max_length=15)
    start_date = models.DateField(default=timezone.now)
    #valid_date = models.DateField(default=timezone.now) # the user will be choise the date of expierd manually
    valid_date = models.DateField(null=True,blank=True) # change valid_date to use it below in a save function
    quantity = models.IntegerField()
    discount = models.FloatField()



    def save(self, *args, **kwargs ):
        week = datetime.timedelta(days=7)            # using timedelta to create a spicific time (ex: 7 dayes)
        self.valid_date = self.start_date + week
        super(Coupon, self).save(*args, **kwargs)




