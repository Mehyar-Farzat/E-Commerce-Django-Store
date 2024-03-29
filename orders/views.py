import datetime
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .models import Order, OrderDetail, Cart, CartDetail, Coupon
from settings.models import DeliveryFee
from products.models import Product
from django.contrib.auth.decorators import login_required
from utils.generate_code import generate_code
from django.http import JsonResponse
from django.template.loader import render_to_string

from django.conf import settings
import stripe
from dotenv import load_dotenv
import os

load_dotenv()

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
    total = round(sub_total + delivery_fee, 2)                                  # get total of a cart
    discount = 0                                                      # set discount to 0

    pub_key= os.environ.get('STRIPE_API_KEY_Publishable')

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

                 

                html = render_to_string('includes/checkout_table.html',{

                        'cart' : cart,
                        'cart_detail' : cart_detail,
                        'delivery_fee' : delivery_fee,
                        'sub_total' : round(sub_total, 2),
                        'total' : total,
                        'discount' : round(coupon_value, 2),
                        'pub_key' : pub_key
                })
                return JsonResponse({'result':html})



    return render(request, 'orders/checkout.html', {

        'cart' : cart,
        'cart_detail' : cart_detail,
        'delivery_fee' : delivery_fee,
        'sub_total' : sub_total,
        'total' : total,
        'discount' : discount,
        'pub_key' : pub_key
    })

@login_required
def add_to_cart(request):
    product = Product.objects.get(id=request.POST['product_id'])
    quantity = request.POST['quantity']

    cart = Cart.objects.get(user=request.user, status='inprogress')   # get a cart

    cart_detail, created = CartDetail.objects.get_or_create(cart=cart, product=product)

    # if not created:
    #     cart_detail.quantity = cart_detail.quantity + quantity

    cart_detail.price = product.price                         # get price of a product 
    cart_detail.quantity = quantity                           # get quantity of a product 
    cart_detail.total = round(int(quantity)*product.price,2)       # get total of a product 
    cart_detail.save()                                        # save a product in a cart 

    cart = Cart.objects.get(user=request.user, status='inprogress')    # get a cart one more  
    cart_detail= CartDetail.objects.filter(cart=cart)
    total = f"${cart.cart_total()}"   # show $ sign in total price
    cart_count = len(cart_detail)
    html = render_to_string('includes/cart_sidebar.html',{'cart_data' : cart , 'cart_detail_data' : cart_detail, request:request})
    return JsonResponse({'result':html, 'total':total, 'cart_count':cart_count})


def process_payment(request):
        cart = Cart.objects.get(user=request.user, status='inprogress')    # get a cart one more  
        delivery_fee = DeliveryFee.objects.last().fee

        if cart.order_total_discount:
            total = cart.order_total_discount() + delivery_fee

        else:
            total = cart.cart_total() + delivery_fee

        code = generate_code()

        # store code in session
        request.session['order_code'] = code
        request.session.save()

        stripe.api_key = os.environ.get('STRIPE_API_KEY_SECRET')

        checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        'price_data' : {
                            'currency' : 'usd',
                            'product_data' : {
                                'name' : code
                            },
                            'unit_amount' : int(total*100)
                        },

                        'quantity' : 1

                    },
                ],
                mode='payment',
                success_url='http://127.0.0.1:8000/orders/checkout/payment/success',
                cancel_url='http://127.0.0.1:8000/orders/checkout/payment/failed',
            )

        return JsonResponse({'session' : checkout_session})
    
@login_required
def payment_success(request):
    cart = Cart.objects.get(user=request.user, status='inprogress')
    cart_detail= CartDetail.objects.filter(cart=cart)
    
    # get a code from session
    order_code = request.session.get('order_code')
    
    # create a new order after payment
    new_order = Order.objects.create( 
                
                user=request.user, 
                coupon= cart.coupon,
                order_total_discount =cart.order_total_discount,
                code = order_code
                )

    # create order detail ( from cart detail to order detail)

    for object in cart_detail:                            # loop to get all products of a cart 
        OrderDetail.objects.create(                         # create order detail 

            order= new_order, 
            product= object.product, 
            quantity= object.quantity, 
            price= object.product.price, 
            total= object.total

            )
    cart.status = 'completed'                              # change status of a cart to completed
    cart.save()

    return render(request, 'orders/success.html',{'code': order_code})
    

def payment_failed(request):

    return render(request, 'orders/failed.html', {'code':'code'})
    pass