from django.urls import path
from .views import order_list, checkout, add_to_cart, payment_success, payment_failed, process_payment
from .api import CartDetailCreateDeleteAPI, OrderListAPI,OrderDetailAPI, ApplyCouponAPI, OrderCreateAPI




urlpatterns = [

    path('', order_list),
    path('add-to-cart', add_to_cart),
    path('checkout' , checkout),
    path('checkout/payment', process_payment),
    path('checkout/payment/success', payment_success),
    path('checkout/payment/failed', payment_failed),
    


    # api

    path('api/<str:username>/list', OrderListAPI.as_view()),
    path('api/<str:username>/order/create',OrderCreateAPI.as_view()),
    path('api/<str:username>/list/<int:pk>', OrderDetailAPI.as_view()),
    path('api/<str:username>/cart', CartDetailCreateDeleteAPI.as_view()),
    path('api/<str:username>/cart/applycoupon', ApplyCouponAPI.as_view()),

    
]