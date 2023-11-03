import datetime
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Order, OrderDetail, Cart, CartDetail, Coupon
from sittings.models import Deliveryfee

# Create your views here.


def order_list(request):
    orders = Order.objects.all()
    return render(request, 'orders/orders.html', {'orders' : orders})



def checkout(request):
    cart = Cart.objects.get(user=request.user, status='inprogress')
    cart_detail = CartDetail.objects.filter(cart=cart)
    delivery_fee = Deliveryfee.objects.last().fee
    sub_total = cart.cart_total()
    total = sub_total + delivery_fee
    discount = 0

    if request.method== 'POST':
        code = request.POST['coupon_code']
        #code = request.POST.get('coupon_code')  another way to get coupon
        #coupon = Coupon.objects.get(code=code)  # to get a code of coupon, but if there is no coupon, the site will be down
        coupon = get_object_or_404(Coupon, code=code) # to return error 404 if there is no coupon

        if coupon and coupon.quantity > 0 :  # if there is a coupon and enough quantity
            today_date = datetime.datetime.today().date()
            if today_date >= coupon.start_date and today_date <= coupon.valid_date: # check if the coupon is up to date
                coupon_value = sub_total / 100*coupon.discount # get the value of this coupon
                sub_total = sub_total - coupon_value # the new sub total after discount
                total = sub_total + delivery_fee     # the new total after discount


                # save coupon

                cart.coupon = coupon
                cart.cart_total_discount = sub_total
                cart.save()




                
    return render(request, 'orders/checkout.html', {

        'cart' : cart,
        'cart_detail' : cart_detail,
        'delivery_fee' : delivery_fee,
        'sub_total' : sub_total,
        'total' : total,
        'discount' : discount


    })
