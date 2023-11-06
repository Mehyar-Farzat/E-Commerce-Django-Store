from rest_framework import generics
from rest_framework.response import Response
from .serializers import CartSerializer, OrderSerializer
from django.contrib.auth.models import User
from products.models import Product, Brand
from .models import Cart, CartDetail, Order, OrderDetail, Coupon


class CartDetailCreateDeleteAPI(generics.GenericAPIView):

    def get(self,request,*args, **kwargs):
        user = User.objects.get(username=self.kwargs['username']) # use username url to get a user
        cart , created = Cart.objects.get_or_create(user=user, status='inprogress') # checking if this user has a cart, if not, create one
        data = CartSerializer(cart).data
        return Response({'Cart' : data})


   # delete an item in a cart
    def delete(self,request,*args, **kwargs):
        user = User.objects.get(username=self.kwargs['username'])
        product = Product.objects.get(id=request.POST['product_id']) # get the id of a product
        cart = Cart.objects.get(user=user, status='inprogress') # get a cart

        cart_detail = CartDetail.objects.get(cart=cart,product=product)  # get a product of exiting cart
        
        