from django.shortcuts import render
from products.models import Product,Brand,Review

# Create your views here.

def home(request):
    
    brands = Brand.objects.all()[:10]
    sale_products =  Product.objects.filter(flag='Sale')[:10]
    return render(request, 'sittings/home.html', {
        'brands':brands,
        'sale_products':sale_products,

    })
