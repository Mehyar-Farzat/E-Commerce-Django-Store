from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer
from .models import Product



@api_view(['GET'])
def product_list_api(request):
    products = Product.objects.all() # return as list
    data = ProductSerializer(products, many=True).data # return as json
    return Response({'products': data})

