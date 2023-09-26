from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product, ProductImage, Review, Brand



# Create your views here.

class ProductList(ListView):
    model = Product
    paginate_by = 10
    

class ProductDetail(DetailView):
    model = Product
    
    

    def get_context_data(self, **kwargs):  # this function to return more details for product such as images,review
        context = super().get_context_data(**kwargs)
        context["product_images"] = ProductImage.objects.filter(product=self.get_object())
        context["product_review"] = Review.objects.filter(product=self.get_object())
        
        return context



class BrandList(ListView):
    model = Brand
    paginate_by = 10
    



    

class BrandDetail(DetailView):
    model = Brand

    #def get_context_data(self, **kwargs):  # this function to return more details for product such as images,review
        #context = super().get_context_data(**kwargs)
        #context["brand_products"] = Product.objects.filter(brand=self.get_object())
        #return context

    