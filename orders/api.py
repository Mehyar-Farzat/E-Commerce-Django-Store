from rest_framework import generics
from rest_framework.response import Response
from .serializers import CartSerializer, OrderListSerializer, OrderDetailSerializer
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from products.models import Product, Brand
from .models import Cart, CartDetail, Order, OrderDetail, Coupon
import datetime
from settings.models import DeliveryFee


class CartDetailCreateDeleteAPI(generics.GenericAPIView):  # add and delete an item in a cart 
    serializer_class = CartSerializer                       # return as json

    def get(self,request,*args, **kwargs):                 # get a cart of exiting user 
        user = User.objects.get(username=self.kwargs['username'])   # get a user by username 
        cart , created = Cart.objects.get_or_create(user=user, status='inprogress') # checking if this user has a cart, if not, create one
        data = CartSerializer(cart).data                           # return as json 
        return Response({'Cart' : data})  

    
    def post(self,request,*args, **kwargs):                      # add an item in a cart 
        user= User.objects.get(username=self.kwargs['username'])  # get a user by username 
        product = Product.objects.get(id=request.POST['product_id'])  # get the id of a product to get a spicific product 
        quantity = int(request.POST['quantity'])                     # get quantity of a product 

        cart = Cart.objects.get(user=user, status='inprogress')    # get a cart 
        cart_detail, created = CartDetail.objects.get_or_create(cart=cart, product=product)  # checking if this product is in the cart, if not, create one
        cart_detail.price = product.price                         # get price of a product 
        cart_detail.quantity = quantity                           # get quantity of a product 
        cart_detail.total = round(quantity*product.price,2)       # get total of a product 
        cart_detail.save()                                        # save a product in a cart 

        return Response({'message' : 'product was added successfully'})



   # delete an item in a cart
    def delete(self,request,*args, **kwargs):                    #  delete an item in a cart
        user = User.objects.get(username=self.kwargs['username'])   # get a user by username 
        product = Product.objects.get(id=request.POST['product_id']) # get the id of a product to get a spicific product
        cart = Cart.objects.get(user=user, status='inprogress') # get a cart

        cart_detail = CartDetail.objects.get(cart=cart,product=product)  # get a product of exiting cart
        cart_detail.delete()
        return Response ({'message':'product was deleted successfully'})

        

class OrderListAPI(generics.ListAPIView):      # return all orders that belong to the exiting user 
    queryset= Order.objects.all()              # return as list
    serializer_class = OrderListSerializer     # return as json

# return all orders that belong to the exiting user
    def list(self,request,*args, **kwargs):      
        user = User.objects.get(username=self.kwargs['username'])  # get a user by username 
        queryset = self.get_queryset().filter(user=user)           # get all orders that belong to the exiting user
        data = OrderListSerializer(queryset,many=True).data        # return as json
        return Response(data)                                      # return as json

class OrderDetailAPI(generics.RetrieveAPIView):                  # return a spicific order that belong to the exiting user
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer


class ApplyCouponAPI(generics.GenericAPIView):              # apply a coupon to a cart 

    def post(self,request,*args, **kwargs): 
        user = User.objects.get(username=self.kwargs['username']) 
        coupon = get_object_or_404(Coupon, code=request.data['coupon_code'])   # get a coupon by code
        cart = Cart.objects.get(user=user, status='inprogress')                # get a cart
        if coupon and coupon.quantity > 0:                                     # check if coupon is valid and quantity is more than 0 
            today_date = datetime.datetime.today().date()                      # get today date 
            if today_date >= coupon.start_date and today_date <= coupon.valid_date: # check if today date is between start date and valid date 
                coupon_value = sub_total() / 100*coupon.discount               # get coupon value 
                sub_total = sub_total() - coupon_value                         # get sub total 
                cart.coupon = coupon                                          # get coupon 
                cart.order_total_discount = sub_total                         # get order total discount 
                coupon.quantity -= 1                                          # decrease quantity of coupon by 1 
                cart.save()                                                   # save a cart 
                coupon.save()                                                 # save a coupon
                return Response({'message' : 'coupon was applied successfully'})       
            return Response({'message' : 'coupon was not applied successfully'})
        #return Response({'message' : 'coupon is not valid'})


class OrderCreateAPI(generics.GenericAPIView):   # create an order 
    
        def get(self,request,*args, **kwargs):   
            user = User.objects.get(username=self.kwargs['username']) # get a user by username
            cart = Cart.objects.get(user=user, status='inprogress')   # get a cart 
            cart_detail = CartDetail.objects.filter(cart=cart)        # get all products of a cart 

            # create a new order ( from cart to order)

            new_order = Order.objects.create( 
                
                user=user, 
                coupon= cart.coupon,
                order_total_discount =cart.order_total_discount,
                
                )

            # create order detail ( from cart detail to order detail)

            for object in cart_detail():                            # loop to get all products of a cart 
                OrderDetail.objects.create(                         # create order detail 
 
                    order= new_order, 
                    product= object.product, 
                    quantity= object.quantity, 
                    price= object.product.price, 
                    total= object.total

                    )
            cart.status = 'completed'                              # change status of a cart to completed
            cart.save()                                            # save a cart
            return Response({'message' : 'order was created successfully'})