from django.shortcuts import render, redirect  # render
from django.views.generic import ListView, DetailView  # generic views
from .models import Product, ProductImage, Review, Brand  # models
from django.db.models import Q , F , Value   # Q , F , Value
from django.db.models.aggregates import Avg, Max, Min, Sum, Count  # aggregate
from django.views.decorators.cache import cache_page  # cache

from .tasks import send_email_task # celery task

#@cache_page(60 * 1)
def mydebug(request):  # debug

    data = Product.objects.all()  # select * from product

    # data = Product.objects.filter(price__gt=9000)   # gt = greater than 9000 
    # data = Product.objects.filter(price__gte=9000)  # gte = greater than or equal 9000
    # data = Product.objects.filter(price__lt=300)   # lt = less than 300
    # data = Product.objects.filter(price__lte=200)  # lte = less than or equal 200
    # data = Product.objects.filter(price__range=[100, 150])  # range = between 100 and 150
    
    # data = Product.objects.filter(name__contains='Smith')  # contains = contains 'Smith'
    # data = Product.objects.filter(name__icontains='Smith')  # icontains = contains 'Smith' (case insensitive)
    
    # data = Product.objects.filter(name__startswith='Smith')  # startswith = starts with 'Smith'
    # data = Product.objects.filter(name__endswith='Smith')  # endswith = ends with 'Smith'
    
    # data = Product.objects.filter(name__isnull=True)  # isnull = is null
    # data = Product.objects.filter(price__lt=300, name__contains='Smith')  # multiple filters
    
    # data = Product.objects.filter(Q(price__lt=300) | Q(name__contains='Smith'))  # OR
    # data = Product.objects.filter(Q(price__lt=300) & Q(name__contains='Smith'))  # AND
    # data = Product.objects.filter(~Q(name__contains='Smith'))  # NOT
    # data = Product.objects.filter(Q(price__lt=300) & ~Q(name__contains='Smith')) # AND NOT
    
    # data = Product.objects.filter(quantity=F('price'))  # F() expressions
    # data = Product.objects.filter(price__gt=F('quantity') * 5)  # F() expressions
    
    # data = Product.objects.order_by('price')  # order by
    # data = Product.objects.order_by('-price')  # order by descending
    # data = Product.objects.order_by('price', '-name')  # order by multiple fields
    # data = Product.objects.order_by('price').reverse()  # reverse order
    
    # data = Product.objects.order_by('?')  # random order
    
    # data = Product.objects.all()[:10]  # limit
    # data = Product.objects.all()[10:20]  # offset
    # data = Product.objects.all()[10:20:2]  # offset and limit
    # data = Product.objects.all()[10:]  # offset
    # data = Product.objects.all()[:10:2]  # limit
    # data = Product.objects.all()[::2]  # limit
    # data = Product.objects.all()[10::2]  # offset
    
    # data = Product.objects.values('name', 'price')  # select
    # data = Product.objects.values_list('name', 'price')  # select
    # data = Product.objects.only('name', 'price')  # select
    
    # data = Product.objects.select_related('brand')  # join  # select_related() is for ForeignKey and OneToOneField
    # data = Product.objects.prefetch_related('brand').all()  # join # prefetch_related() is for ManyToManyField
   
    # #data = Product.objects.aggregate(sum('price'))  # aggregate
    # data = Product.objects.aggregate(Avg('price'), Max('price'), Min('price'), Sum('price'), Count('price'))  # aggregate
   
    # data = Product.objects.annotate(New=Value('True')) # annotate
    # data = Product.objects.annotate(average_price=Avg('price'))  # annotate
    # data = Product.objects.annotate(average_price=Avg('price')).filter(average_price__gt=100)  # annotate
    # data = Product.objects.annotate(price_with_tax=F('price') * 1.1)  # annotate
    
    send_email_task.delay()   # celery task

    return render(request, 'products/debug.html', {'data': data})   # render
    


# Create your views here.

class ProductList(ListView):  # this class to show all products
    model = Product           
    paginate_by = 10          # this to show 10 products per page
    

class ProductDetail(DetailView):     # this class to show product details
    model = Product
    
    

    def get_context_data(self, **kwargs):  # this function to return more details for product such as images,review
        context = super().get_context_data(**kwargs)
        context["product_images"] = ProductImage.objects.filter(product=self.get_object())
        context['reviews'] = Review.objects.filter(product=self.get_object())
        return context



class BrandList(ListView):    # this class to show all brands
    model = Brand
    paginate_by = 10
    

#class BrandDetail(DetailView):
    #model = Brand

    

class BrandDetail(ListView):     # this class to show all products for specific brand
    model = Product
    template_name = 'products/brand_detail.html'
    paginate_by = 10

    def get_queryset(self):      # this function to filter products for specific brand
        queryset = super(BrandDetail,self).get_queryset()
        brand = Brand.objects.get(slug=self.kwargs['slug'])
        queryset= queryset.filter(brand=brand)
        return queryset


    def get_context_data(self, **kwargs):      # this function to return more details for brand such as brand name
        context = super().get_context_data(**kwargs)
        context["brand"] = Brand.objects.get(slug=self.kwargs['slug'])
        return context


    
def add_review(request,slug):
    product = Product.objects.get(slug=slug)
    review = request.POST['review']     # OR ---> request.POST.get('review')
    rate = request.POST['rating']


    Review.objects.create(

        user= request.user ,
        product= product ,
        review= review ,
        rate= rate
    )

    return redirect(f'/products/{slug}')


