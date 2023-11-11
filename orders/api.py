from rest_framework import generics
from rest_framework.response import Response
from .serializers import CartSerializer, OrderListSerializer, OrderDetailSerializer
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from products.models import Product, Brand
from .models import Cart, CartDetail, Order, OrderDetail, Coupon
import datetime


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

        

class OrderListAPI(generics.ListAPIView):
    queryset= Order.objects.all()
    serializer_class = OrderListSerializer

# return all orders that belong to the exiting user
    def list(self,request,*args, **kwargs):
        user = User.objects.get(username=self.kwargs['username'])
        queryset = self.get_queryset().filter(user=user)
        data = OrderListSerializer(queryset,many=True).data
        return Response(data)

class OrderDetailAPI(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer


class ApplyCouponAPI(generics.GenericAPIView):

    def post(self,request,*args, **kwargs):
        user = User.objects.get(username=self.kwargs['username'])
        coupon = get_object_or_404(Coupon, code=request.data['coupon_code'])
        cart = Cart.objects.get(user=user, status='inprogress')
        if coupon and coupon.quantity > 0:
            today_date = datetime.datetime.today().date()
            if today_date >= coupon.start_date and today_date <= coupon.valid_date:
                coupon_value = sub_total() / 100*coupon.discount
                sub_total = sub_total() - coupon_value
                cart.coupon = coupon
                cart.order_total_discount = sub_total
                coupon.quantity -= 1
                cart.save()
                coupon.save()
                return Response({'message' : 'coupon was applied successfully'})
            return Response({'message' : 'coupon was not applied successfully'})
        #return Response({'message' : 'coupon is not valid'})


class OrderCreateAPI(generics.GenericAPIView):
    
        def post(self,request,*args, **kwargs):
            user = User.objects.get(username=self.kwargs['username'])
            cart = Cart.objects.get(user=user, status='inprogress')
            cart_detail = CartDetail.objects.filter(cart=cart)

            # create a new order ( from cart to order)

            new_order = Order.objects.create(
                
                user=user, 
                coupon= cart.coupon,
                order_total_discount =cart.order_total_discount,
                
                )

            # create order detail ( from cart detail to order detail)

            for object in cart_detail():
                OrderDetail.objects.create(

                    order= new_order, 
                    product= object.product, 
                    quantity= object.quantity, 
                    price= object.product.price, 
                    total= object.total

                    )
            cart.status = 'completed'
            cart.save()
            return Response({'message' : 'order was created successfully'})