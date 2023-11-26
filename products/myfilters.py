from django_filters import rest_framework as filters
from .models import Product
import django_filters



class ProductFilter(filters.FilterSet):    # create filter class 
    class Meta:  
        model = Product    
        fields = { 
            
            'name' : ['contains'],
            'price': ['range'],
            'flag' : ['exact'],
            'brand': ['exact'],

        }