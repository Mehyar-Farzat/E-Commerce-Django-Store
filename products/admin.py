from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Product, ProductImage, Brand, Review




class ProductImagesInline(admin.TabularInline):   # add images in product admin page 
    model = ProductImage 


class ProductAdmin(SummernoteModelAdmin):        # add summernote in product admin page
    summernote_fields = '__all__'                # add summernote in all fields
    inlines = [ProductImagesInline,]     






# Register your models here.

admin.site.register(Product,ProductAdmin)   
admin.site.register(ProductImage)
admin.site.register(Brand)
admin.site.register(Review)
