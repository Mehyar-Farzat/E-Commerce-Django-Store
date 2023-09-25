import os , django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

django.setup()


from products.models import Product, Brand, Review
import random
from faker import Faker



def add_brands(n):
    fake = Faker()
    images = ['1.jpg','2.jpg','3.jpg','4.jpg','5.jpg','6.jpg','7.jpg']
    for x in range(n):
        Brand.objects.create(
            name = fake.name(),
            image = f"brands/{images[random.randint(0,5)]}"

            
        )

    print(f'{n} Brands added successfully')    


def add_products(n):
    pass


def add_reviews(n):
    pass


add_brands(50)