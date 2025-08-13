import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_graphql_crm.settings')
django.setup()

from crm.models import Customer, Product, Order

def seed_db():
    # Create customers
    customer1 = Customer.objects.create(name="Alice", email="alice@example.com", phone="+1234567890")
    customer2 = Customer.objects.create(name="Bob", email="bob@example.com")

    # Create products
    product1 = Product.objects.create(name="Laptop", price=999.99, stock=10)
    product2 = Product.objects.create(name="Phone", price=499.99, stock=20)

    # Create an order
    order = Order.objects.create(customer=customer1)
    order.products.add(product1, product2)
    order.total_amount = product1.price + product2.price
    order.save()

if __name__ == '__main__':
    seed_db()
    print("Database seeded")
