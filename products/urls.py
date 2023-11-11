from django.urls import path
from .views import ProductList,ProductDetail,BrandList,BrandDetail,mydebug
#from .api import product_list_api, product_detail_api                                  #  (for functions)
from .api import ProductListAPI, ProductDetailAPI #BrandListAPI, BrandDetailAPI         #  (for CBV)




urlpatterns = [

    path('debug', mydebug),
    path('', ProductList.as_view()),
    path('brands/', BrandList.as_view()),
    path('brands/<slug:slug>', BrandDetail.as_view()),
    path('<slug:slug>', ProductDetail.as_view()),
    path('api/list', ProductListAPI.as_view()),                   # path for CBV
    path('api/list/<int:pk>', ProductDetailAPI.as_view()),        # path for CBV
    
    #path('api/list/brands', BrandListAPI.as_view()),                   
    #path('api/list/brands/<int:pk>', BrandDetailAPI.as_view()),


    # path('api/list', product_list_api),                         # path for fuction(def)
    # path('api/list/<int:product_id>', product_detail_api),      # path for function(def)

]



