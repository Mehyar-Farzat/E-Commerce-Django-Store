from rest_framework import generics
from rest_framework.response import Response
from .serializers import CartSerializer, OrderListSerializer, OrderDetailSerializer
from django.contrib.auth.models import User
from products.models import Product, Brand
from .models import Cart, CartDetail, Order, OrderDetail, Coupon


class CartDetailCreateDeleteAPI(generics.GenericAPIView):

    def get(self,request,*args, **kwargs):
        user = User.objects.get(username=self.kwargs['username']) # use username url to get a user
        cart , created = Cart.objects.get_or_create(user=user, status='inprogress') # checking if this user has a cart, if not, create one
        data = CartSerializer(cart).data
        return Response({'Cart' : data})

    
    def post(self,request,*args, **kwargs):
        user= User.objects.get(username=self.kwargs['username'])
        product = Product.objects.get(id=request.POST['product_id'])
        quantity = int(request.POST['quantity'])

        cart = Cart.objects.get(user=user, status='inprogress')
        cart_detail, created = CartDetail.objects.get_or_create(cart=cart, product=product)
        cart_detail.price = product.price
        cart_detail.quantity = quantityc
        cart_detail.total = round(quantity*product.price,2)
        cart_detail.save()

        return Response({'message' : 'product was added successfully'})



   # delete an item in a cart
    def delete(self,request,*args, **kwargs):
        user = User.objects.get(username=self.kwargs['username'])
        product = Product.objects.get(id=request.POST['product_id']) # get the id of a product to get a spicific product
        cart = Cart.objects.get(user=user, status='inprogress') # get a cart

        cart_detail = CartDetail.objects.get(cart=cart,product=product)  # get a product of exiting cart
        cart_detail.delete()
        return Response ({'message':'product was deleted successfully'})

class OrderListAPI(generics.RetrieveAPIView):
    queryset= Order.objects.all()
    serializer_class = OrderListSerializer
