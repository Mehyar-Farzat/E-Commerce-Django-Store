from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductListSerializer, ProductDetailSerializer, BrandListSerializer, BrandDetailSerializer
from .models import Product, Brand
from .mypagination import CustomPagination


# Functions:

# @api_view(['GET'])
# def product_list_api(request):
#     products = Product.objects.all() # return as list
#     data = ProductSerializer(products, many=True, context= {'request': request}).data # return as json
#     return Response({'products': data})


# @api_view(['GET'])
# def product_detail_api(request, product_id):
#     product = Product.objects.get(id=product_id)
#     data = ProductSerializer(product, context= {'request': request}).data
#     return Response({'product': data})

#------------------------------------------------------------------------------------#


# Class Based View:

class ProductListAPI(generics.ListAPIView):
    serializer_class = ProductListSerializer
    queryset = Product.objects.all()
    pagination_class = CustomPagination


class ProductDetailAPI(generics.RetrieveAPIView):
    serializer_class = ProductDetailSerializer
    queryset = Product.objects.all()


class BrandListAPI(generics.ListAPIView):
    serializer_class = BrandListSerializer
    queryset = Brand.objects.all()


class BrandDetailAPI(generics.RetrieveAPIView):
    serializer_class = BrandDetailSerializer
    queryset = Brand.objects.all()

# class ProductDetailAPI(generics.RetrieveUpdateAPIView):   # update and edite date
#     serializer_class = ProductSerializer
#     queryset = Product.objects.all()


# class ProductListAPI(generics.ListCreateAPIView):   # list and create(adding like Editor)
#     serializer_class = ProductSerializer
#     queryset = Product.objects.all()


# class ProductDetailAPI(generics.RetrieveUpdateDestroyAPIView):   # update and edite and delete data
#     serializer_class = ProductSerializer
#     queryset = Product.objects.all()