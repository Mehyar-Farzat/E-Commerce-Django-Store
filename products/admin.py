from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Product, ProductImage, Brand, Review




class ProductImagesInline(admin.TabularInline):
    model = ProductImage


class ProductAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'
    inlines = [ProductImagesInline,]    






# Register your models here.

admin.site.register(Product,ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(Brand)
admin.site.register(Review)
