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
    fake = Faker()
    images = ['1.jpg','2.jpg','3.jpg','4.jpg','5.jpg','6.jpg','7.jpg']
    flags = ['sale', 'new' , 'feature']
    for x in range(n):
        Product.objects.create(
            name = fake.name(),
            image = f"product/{images[random.randint(0,5)]}",
            price = random.randint(100,9999),
            #price = round(random.uniform(50.99,199.99),2),
            flag = flags[random.randint(0,2)],
            brand = Brand.objects.get(id=random.randint(1,50)),
            sku = random.randint(1000,10000000),
            subtitle = fake.text(max_nb_chars=200),
            description = fake.text(max_nb_chars=10000),
            
            quantity = random.randint(5,35),
        )

    print(f'{n} Brands added successfully') 




def add_reviews(n):
    fake = Faker()
    for x in range(n):
        pass
    

add_products(100)
