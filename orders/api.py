from rest_framework import generics
from rest_framework.response import Response
from .serializers import CartSerializer, CartDetailSerializer, OrderSerializer, OrderDetailSerializer
from django.contrib.auth.models import User
from products.models import Product, Brand
from .models import Cart, CartDetail, Order, OrderDetail, Coupon


