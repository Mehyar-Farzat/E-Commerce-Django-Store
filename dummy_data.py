import os , django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

django.setup()


from products.models import Product, Brand, Review
from django.contrib.auth.models import User
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
           # price = random.randint(100,500),
            price = round(random.uniform(99.99,599.99),2),
            flag = flags[random.randint(0,2)],
            brand = Brand.objects.get(id=random.randint(1,50)),
            sku = random.randint(1000,10000000),
            subtitle = fake.text(max_nb_chars=50),
            description = fake.text(max_nb_chars=200),
            
            quantity = random.randint(5,35),
        )

    print(f'{n} Brands added successfully') 




def add_reviews(n):
    fake = Faker()
    for x in range(n):
        Review.objects.create(
            product = Product.objects.get(id=random.randint(1,100)),
            user = User.objects.get(id=random.randint(1,5)),
            review = fake.text(max_nb_chars=500),
            rate = random.randint(1,5),
        )

    print(f'{n} Reviews added successfully')
        
    

add_products(300)
