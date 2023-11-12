from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product, ProductImage, Review, Brand
from django.db.models import Q



def mydebug(request):
    #data = Product.objects.all()
    data = Product.objects.filter(price__gt=9000)   # gt = greater than 9000 
    data = Product.objects.filter(price__gte=9000)  # gte = greater than or equal 9000
    data = Product.objects.filter(price__lt=300)   # lt = less than 300
    data = Product.objects.filter(price__lte=200)  # lte = less than or equal 200
    data = Product.objects.filter(price__range=[100, 150])  # range = between 100 and 150
    data = Product.objects.filter(name__contains='Smith')  # contains = contains 'Smith'
    data = Product.objects.filter(name__icontains='Smith')  # icontains = contains 'Smith' (case insensitive)
    data = Product.objects.filter(name__startswith='Smith')  # startswith = starts with 'Smith'
    data = Product.objects.filter(name__endswith='Smith')  # endswith = ends with 'Smith'
    data = Product.objects.filter(name__isnull=True)  # isnull = is null
    data = Product.objects.filter(price__lt=300, name__contains='Smith')  # multiple filters
         
    



    return render(request, 'products/debug.html', {'data': data})
    


# Create your views here.

class ProductList(ListView):
    model = Product
    paginate_by = 10
    

class ProductDetail(DetailView):
    model = Product
    
    

    def get_context_data(self, **kwargs):  # this function to return more details for product such as images,review
        context = super().get_context_data(**kwargs)
        context["product_images"] = ProductImage.objects.filter(product=self.get_object())
        context['reviews'] = Review.objects.filter(product=self.get_object())
        return context



class BrandList(ListView):
    model = Brand
    paginate_by = 10
    

#class BrandDetail(DetailView):
    #model = Brand

    

class BrandDetail(ListView):
    model = Product
    template_name = 'products/brand_detail.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super(BrandDetail,self).get_queryset()
        brand = Brand.objects.get(slug=self.kwargs['slug'])
        queryset= queryset.filter(brand=brand)
        return queryset


    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context["brand"] = Brand.objects.get(slug=self.kwargs['slug'])
        return context
    
        


