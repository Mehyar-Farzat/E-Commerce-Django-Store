from django.shortcuts import render
from products.models import Product, Brand, Review
#from django.views.decorators.cache import cache_page

# Create your views here.
#@cache_page(60 * 60 * 24)
def home(request):
    
    brands = Brand.objects.all()[:10]
    sale_products =  Product.objects.filter(flag='Sale')[:10]
    feature_products =  Product.objects.filter(flag='Feature')[:6]
    new_products =  Product.objects.filter(flag='New')[:10]
    reviews = Review.objects.all()[:2]

    return render(request, 'settings/home.html', {

        'brands':brands,
        'sale_products':sale_products,
        'feature_products':feature_products,
        'new_products':new_products,
        'reviews':reviews,

    })
