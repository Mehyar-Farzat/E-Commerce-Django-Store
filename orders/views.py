import datetime
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .models import Order, OrderDetail, Cart, CartDetail, Coupon
from settings.models import DeliveryFee
from products.models import Product
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def order_list(request):          # return all orders that belong to the exiting user 
    orders = Order.objects.all()  # get all orders that belong to the exiting user 
    return render(request,'orders/orders.html', {'orders' : orders})  # return orders.html with orders data 


@login_required
def checkout(request):       # return checkout.html with cart data 
    cart = Cart.objects.get(user=request.user, status='inprogress')   # get a cart of exiting user 
    cart_detail = CartDetail.objects.filter(cart=cart)                # get all products of exiting cart 
    delivery_fee = DeliveryFee.objects.last().fee                     # get delivery fee 
    sub_total = cart.cart_total()                                     # get sub total of a cart 
    total = sub_total + delivery_fee                                  # get total of a cart
    discount = 0                                                      # set discount to 0

    if request.method== 'POST':                                       # if method is post 
        code = request.POST['coupon_code']                            # get coupon code from form 
        #code = request.POST.get('coupon_code')  another way to get coupon
        #coupon = Coupon.objects.get(code=code)  # to get a code of coupon, but if there is no coupon, the site will be down
        coupon = get_object_or_404(Coupon, code=code) # to return error 404 if there is no coupon

        if coupon and coupon.quantity > 0 :  # if there is a coupon and enough quantity
            today_date = datetime.datetime.today().date()
            if today_date >= coupon.start_date and today_date <= coupon.valid_date: # check if the coupon is up to date
                coupon_value = sub_total / 100*coupon.discount # get the value of this coupon
                sub_total = sub_total - coupon_value # the new sub total after discount
                total = sub_total + delivery_fee     # the new total after discount


                # save cart & coupon

                cart.coupon = coupon
                cart.order_total_discount = sub_total
                coupon.quantity -= 1
                cart.save()
                coupon.save()

                return render(request, 'orders/checkout.html', {

                        'cart' : cart,
                        'cart_detail' : cart_detail,
                        'delivery_fee' : delivery_fee,
                        'sub_total' : round(sub_total, 2),
                        'total' : total,
                        'discount' : round(coupon_value, 2)
                    })



    return render(request, 'orders/checkout.html', {

        'cart' : cart,
        'cart_detail' : cart_detail,
        'delivery_fee' : delivery_fee,
        'sub_total' : sub_total,
        'total' : total,
        'discount' : discount
    })

@login_required
def add_to_cart(request):
    product = Product.objects.get(id=request.POST['product_id'])
    quantity = request.POST['quantity']

    cart = Cart.objects.get(user=request.user, status='inprogress')

    cart_detail, created = CartDetail.objects.get_or_create(cart=cart, product=product)

    # if not created:
    #     cart_detail.quantity = cart_detail.quantity + quantity

    cart_detail.price = product.price                         # get price of a product 
    cart_detail.quantity = quantity                           # get quantity of a product 
    cart_detail.total = round(int(quantity)*product.price,2)       # get total of a product 
    cart_detail.save()                                        # save a product in a cart 

    return redirect(f'/products/{product.slug}')