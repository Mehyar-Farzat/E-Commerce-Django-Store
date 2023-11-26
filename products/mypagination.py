from rest_framework.pagination import PageNumberPagination




class CustomPagination(PageNumberPagination):  # custom pagination class 
    page_size = 30 