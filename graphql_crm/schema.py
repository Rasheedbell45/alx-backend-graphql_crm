import graphene
from graphene_django import DjangoObjectType
from .models import Customer, Product, Order
import re
from crm.schema import Query, Mutation

schema = graphene.Schema(query=Query, mutation=Mutation)

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer

class ProductType(DjangoObjectType):
    class Meta:
        model = Product

class OrderType(DjangoObjectType):
    class Meta:
        model = Order

class CreateCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String()

    customer = graphene.Field(CustomerType)
    message = graphene.String()

    def mutate(self, info, name, email, phone):
        if
          Customer.objects.filter(email=email).exists():
            raise Exception("Email already exists")
        if phone and not re.match(r'^\+?\d{1,3}?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$', phone):
            raise Exception("Invalid phone format")
        customer = Customer(name=name, email=email, phone=phone)
        customer.save()
        return CreateCustomer(customer=customer, message="Customer created")

class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        customers = graphene.List(graphene.InputObjectType(
            fields={
                'name': graphene.String(required=True),
                'email': graphene.String(required=True),
                'phone': graphene.String(),
            }
        ))

    customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)
  
  def mutate(self, info, customers):
        created_customers = []
        errors = []
        for customer_data in customers:
            try:
                if Customer.objects.filter(email=customer_data['email']).exists():
                    raise Exception("Email already exists")
                if 'phone' in customer_data and not re.match(r'^\+?\d{1,3}?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$', customer_data['phone']):
                    raise Exception("Invalid phone format")
                customer = Customer(**customer_data)
                customer.save()
                created_customers.append(customer)
            except Exception as e:
                errors.append(str(e))
        return BulkCreateCustomers(customers=created_customers, errors=errors)

class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Decimal(required=True)
        stock = graphene.Int()
        product = graphene.Field(ProductType)

    def mutate(self, info, name, price, stock=0):
        if price <= 0:
            raise Exception("Price must be positive")
        if stock < 0:
            raise Exception("Stock cannot be negative")
        product = Product(name=name, price=price, stock=stock)
        product.save()
        return CreateProduct(product=product)

class CreateOrder(graphene.Mutation):
    class Arguments:
        customer_id = graphene.ID(required=True)
        product_ids = graphene.List(graphene.ID, required=True)

    order = graphene.Field(OrderType)

    def mutate(self, info, customer_id, product_ids):
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            raise Exception("Invalid customer ID")
          
        if not product_ids:
            raise Exception("At least one product is required")
        products = Product.objects.filter(id__in=product_ids)
        if len(products) != len(product_ids):
            raise Exception("Invalid product ID")
        order = Order(customer=customer)
        order.save()
        order.products.set(products)
        total_amount = sum(product.price for product in products)
        order.total_amount = total_amount
        order.save()
        return CreateOrder(order=order)

class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_custom
