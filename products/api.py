from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .serializers import ProductListSerializer, ProductDetailSerializer #BrandListSerializer, BrandDetailSerializer
from .models import Product, Brand
from .mypagination import CustomPagination
from .myfilters import ProductFilter


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

class ProductListAPI(generics.ListAPIView):        # list and create(adding like Editor)
    serializer_class = ProductListSerializer       # return as json
    queryset = Product.objects.all()               # return as list
    pagination_class = CustomPagination            # custom pagination
    #filter_backends = [DjangoFilterBackend]       # filter
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]   # filter and search and ordering filters
    search_fields = ['name', 'tags']               # search 
    filterset_fields = ['brand', 'flag']           # filter by brand and flag 
    ordering_fields = ['price']                    # ordering by price 
    filterset_class = ProductFilter                # custom filter class 


class ProductDetailAPI(generics.RetrieveAPIView):   # update and edite date 
    serializer_class = ProductDetailSerializer      
    queryset = Product.objects.all()                


# class BrandListAPI(generics.ListAPIView):
#     serializer_class = BrandListSerializer
#     queryset = Brand.objects.all()


# class BrandDetailAPI(generics.RetrieveAPIView):
#     serializer_class = BrandDetailSerializer
#     queryset = Brand.objects.all()

# class ProductDetailAPI(generics.RetrieveUpdateAPIView):   # update and edite date
#     serializer_class = ProductSerializer
#     queryset = Product.objects.all()


# class ProductListAPI(generics.ListCreateAPIView):   # list and create(adding like Editor)
#     serializer_class = ProductListSerializer
#     queryset = Product.objects.all()


# class ProductDetailAPI(generics.RetrieveUpdateDestroyAPIView):   # update and edite and delete data
#     serializer_class = ProductListSerializer
#     queryset = Product.objects.all()