from django.shortcuts import render
from .models import Order, OrderDetail, Cart, CartDetail
from sittings.models import Deliveryfee

# Create your views here.


def order_list(request):
    orders = Order.objects.all()
    return render(request, 'orders/orders.html', {'orders' : orders})



def checkout(request):
    cart = Cart.objects.get(user=request.user, status='inprogress')
    cart_detail = CartDetail.objects.filter(cart=cart)
    delivery_fee = Deliveryfee.objects.last().fee

    return render(request, 'orders/checkout.html', {

        'cart' : cart,
        'cart_detail' : cart_detail,
        'delivery_fee' : delivery_fee


    })
