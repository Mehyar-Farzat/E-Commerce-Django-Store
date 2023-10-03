from rest_framework import serializers
from .models import Product, Brand , Review



class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, source='review_product')   # get reviews of product
    reviews_count = serializers.SerializerMethodField()              # get count of reviews
    avg_rate = serializers.SerializerMethodField()                   # get Avg
    class Meta:
        model = Product
        fields = '__all__'


    def get_reviews_count(self,object):                         # get count reviews of exiting product
        reviews_count = object.review_product.all().count()
        return reviews_count


    def get_avg_rate(self,object):                              # get avarge of rate
        total = 0
        reviews = object.review_product.all()
        for review in reviews:                                  # loop to get all reviews
            total += review.rate                                # add(+) all reviews

        return total/len(reviews)                               # get total and divid on length to get avg











class BrandSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True,source='product_brand') # show products in brand detail
    class Meta:
        model = Brand
        fields = '__all__'



        






