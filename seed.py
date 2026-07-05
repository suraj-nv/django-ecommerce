import os
import django
import random
import string
from datetime import date, timedelta
from decimal import Decimal

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from store.models import (
    PromotionalOffer,
    Collection,
    Product,
    Customer,
    Address,
    Order,
    OrderItem,
    Cart,
    CartItem,
)

print("Starting database seeding...")

# =====================================
# Promotional Offers
# =====================================

offers = []

offer_data = [
    ("10% OFF", 10),
    ("15% OFF", 15),
    ("20% OFF", 20),
    ("25% OFF", 25),
    ("30% OFF", 30),
]

for desc, discount in offer_data:
    offer, created = PromotionalOffer.objects.get_or_create(
        description=desc,
        defaults={
            "discount": discount
        }
    )
    offers.append(offer)

print(f"{len(offers)} offers created.")

# =====================================
# Collections
# =====================================

collection_names = [
    "Mobiles",
    "Laptops",
    "Tablets",
    "Televisions",
    "Cameras",
    "Smart Watches",
    "Headphones",
    "Speakers",
    "Gaming",
    "Books",
    "Men Fashion",
    "Women Fashion",
    "Kids Fashion",
    "Footwear",
    "Beauty",
    "Furniture",
    "Kitchen",
    "Home Decor",
    "Groceries",
    "Sports",
    "Fitness",
    "Toys",
    "Baby Care",
    "Pet Supplies",
    "Office",
    "Stationery",
    "Automotive",
    "Health",
    "Jewellery",
    "Bags",
    "Travel",
    "Musical Instruments",
    "Garden",
    "Tools",
    "Lighting",
    "Air Conditioners",
    "Refrigerators",
    "Washing Machines",
    "Microwaves",
    "Water Purifiers",
    "Computer Accessories",
    "Networking",
    "Printers",
    "Monitors",
    "Storage Devices",
    "Software",
    "Gift Items",
    "Craft Supplies",
    "Party Supplies",
    "Accessories",
]

collections = {}

for name in collection_names:
    collection, created = Collection.objects.get_or_create(
        title=name
    )
    collections[name] = collection

print(f"{len(collections)} collections created.")
print("Part 1 Completed Successfully!")

# =====================================
# PART 2 - PRODUCTS
# =====================================

print("Creating products...")

product_catalog = {
    "Mobiles": {
        "brands": ["Apple", "Samsung", "OnePlus", "Xiaomi", "Realme", "Vivo", "Oppo", "Google"],
        "models": [
            "iPhone 16 Pro", "Galaxy S25 Ultra", "13", "Redmi Note 14",
            "Narzo 80", "V50", "Find X8", "Pixel 10"
        ],
        "variants": ["128GB", "256GB", "512GB"],
        "colors": ["Black", "Blue", "Silver", "Gold", "Green"]
    },

    "Laptops": {
        "brands": ["Dell", "HP", "Lenovo", "Asus", "Acer", "Apple"],
        "models": [
            "Inspiron", "Pavilion", "ThinkPad", "ZenBook",
            "Aspire", "MacBook Air M4"
        ],
        "variants": ['13"', '14"', '15.6"', '16"'],
        "colors": ["Silver", "Black", "Gray"]
    },

    "Televisions": {
        "brands": ["Samsung", "LG", "Sony", "TCL", "Mi"],
        "models": ["Smart TV", "OLED TV", "QLED TV"],
        "variants": ['43"', '50"', '55"', '65"'],
        "colors": ["Black"]
    },

    "Headphones": {
        "brands": ["Sony", "JBL", "Boat", "Noise", "Apple"],
        "models": [
            "WH-1000XM5",
            "Tune 770",
            "Rockerz",
            "AirPods Pro"
        ],
        "variants": ["Wireless", "Bluetooth"],
        "colors": ["Black", "White", "Blue"]
    },

    "Books": {
        "brands": [""],
        "models": [
            "Atomic Habits",
            "Clean Code",
            "Python Crash Course",
            "Rich Dad Poor Dad",
            "The Alchemist",
            "Deep Learning",
            "Django for APIs"
        ],
        "variants": [""],
        "colors": [""]
    },

    "Footwear": {
        "brands": ["Nike", "Adidas", "Puma", "Woodland"],
        "models": [
            "Air Max",
            "Ultraboost",
            "Running Shoes",
            "Casual Shoes"
        ],
        "variants": [
            "Size 7",
            "Size 8",
            "Size 9",
            "Size 10"
        ],
        "colors": ["Black", "Blue", "White"]
    },

    "Toys": {
        "brands": ["Barbie", "LEGO", "Hot Wheels", "Funskool"],
        "models": [
            "Doll",
            "City Set",
            "Racing Track",
            "Remote Car",
            "Puzzle"
        ],
        "variants": ["Standard"],
        "colors": ["Red", "Blue", "Pink"]
    },

    "Kitchen": {
        "brands": ["Prestige", "Philips", "Bajaj", "Havells"],
        "models": [
            "Mixer Grinder",
            "Air Fryer",
            "Pressure Cooker",
            "Electric Kettle"
        ],
        "variants": ["1L", "2L", "3L"],
        "colors": ["Black", "Silver"]
    }
}

created_products = 0

while created_products < 500:

    category = random.choice(list(product_catalog.keys()))

    data = product_catalog[category]

    brand = random.choice(data["brands"])
    model = random.choice(data["models"])
    variant = random.choice(data["variants"])
    color = random.choice(data["colors"])

    title = f"{brand} {model} {variant} {color}".strip()

    slug = (
        title.lower()
        .replace('"', "")
        .replace(" ", "-")
        .replace("--", "-")
    )

    product, created = Product.objects.get_or_create(
        slug=slug,
        defaults={
            "title": title,
            "description": f"{title} with premium quality.",
            "price": Decimal(random.randint(299, 150000)),
            "inventory": random.randint(5, 200),
            "collection": collections[category],
        }
    )

    if created:
        created_products += 1

        offer_count = random.randint(0, 2)

        if offer_count:
            product.promotional_offers.set(
                random.sample(
                    offers,
                    offer_count
                )
            )

print(f"{created_products} products created.")
products = list(Product.objects.all())

# =====================================
# PART 3 - CUSTOMERS
# =====================================

print("Creating customers...")

first_names = [
    "Aarav", "Vivaan", "Aditya", "Krishna", "Arjun",
    "Rohan", "Rahul", "Amit", "Karan", "Suraj",
    "Priya", "Ananya", "Sneha", "Pooja", "Neha",
    "Aisha", "Diya", "Kavya", "Riya", "Meera",
    "Raj", "Vikas", "Nikhil", "Manish", "Suresh",
    "Akash", "Deepak", "Varun", "Harsh", "Yash"
]

last_names = [
    "Sharma", "Verma", "Patel", "Singh", "Gupta",
    "Kumar", "Joshi", "Mehta", "Reddy", "Kapoor",
    "Das", "Mishra", "Choudhary", "Pandey", "Yadav",
    "Nair", "Iyer", "Roy", "Bose", "Jain"
]

customers = []

for i in range(1, 5001):

    first = random.choice(first_names)
    last = random.choice(last_names)

    customer = Customer.objects.create(
        first_name=first,
        last_name=last,
        email=f"{first.lower()}.{last.lower()}{i}@gmail.com",
        phone=f"9{random.randint(100000000,999999999)}",
        birth_date=date.today() - timedelta(days=random.randint(7000,22000)),
        membership=random.choice([
            Customer.MEMBERSHIP_BRONZE,
            Customer.MEMBERSHIP_SILVER,
            Customer.MEMBERSHIP_GOLD
        ])
    )

    customers.append(customer)

print(f"{len(customers)} customers created.")

# =====================================
# PART 4 - ADDRESSES
# =====================================

print("Creating addresses...")

streets = [
    "MG Road",
    "Brigade Road",
    "Park Street",
    "Anna Salai",
    "Ring Road",
    "Station Road",
    "Nehru Road",
    "Gandhi Road",
    "Lake View Road",
    "College Road",
    "Main Road",
    "Temple Road",
    "Airport Road",
    "Market Road",
    "Church Street",
]

cities = [
    "Mumbai",
    "Delhi",
    "Bengaluru",
    "Hyderabad",
    "Chennai",
    "Kolkata",
    "Pune",
    "Ahmedabad",
    "Jaipur",
    "Lucknow",
    "Surat",
    "Indore",
    "Bhopal",
    "Nagpur",
    "Patna",
    "Kanpur",
    "Chandigarh",
    "Noida",
    "Gurgaon",
    "Visakhapatnam",
]

for customer in customers:

    Address.objects.create(
        street=f"{random.randint(1,999)} {random.choice(streets)}",
        city=random.choice(cities),
        customer=customer,
    )

print(f"{len(customers)} addresses created.")
# =====================================
# PART 5 - ORDERS
# =====================================

print("Creating orders...")

orders = []

payment_statuses = [
    Order.PAYMENT_STATUS_PENDING,
    Order.PAYMENT_STATUS_COMPLETE,
    Order.PAYMENT_STATUS_FAILED,
]

for i in range(10000):

    order = Order.objects.create(
        customer=random.choice(customers),
        payment_status=random.choice(payment_statuses),
    )

    orders.append(order)

print(f"{len(orders)} orders created.")
# =====================================
# PART 6 - ORDER ITEMS
# =====================================

print("Creating order items...")

products = list(Product.objects.all())

order_items_created = 0

for order in orders:

    item_count = random.randint(1, 5)

    selected_products = random.sample(
        products,
        min(item_count, len(products))
    )

    for product in selected_products:

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=random.randint(1, 5),
            unit_price=product.price
        )

        order_items_created += 1

print(f"{order_items_created} order items created.")
# =====================================
# PART 7 - CARTS
# =====================================

print("Creating carts...")

carts = []

# Create a cart for approximately 70% of customers
selected_customers = random.sample(
    customers,
    int(len(customers) * 0.7)
)

for customer in selected_customers:
    cart = Cart.objects.create()
    carts.append(cart)

print(f"{len(carts)} carts created.")

# =====================================
# PART 8 - CART ITEMS
# =====================================

print("Creating cart items...") 

products = list(Product.objects.all())

cart_items_created = 0

for cart in carts:

    # Each cart gets 1-6 products
    item_count = random.randint(1, 6)

    selected_products = random.sample(
        products,
        min(item_count, len(products))
    )

    for product in selected_products:

        CartItem.objects.create(
            cart=cart,
            product=product,
            quantity=random.randint(1, 5)
        )

        cart_items_created += 1

print(f"{cart_items_created} cart items created.")

print("\n====================================")
print("DATABASE SEEDED SUCCESSFULLY!")
print("====================================")
print(f"Offers       : {PromotionalOffer.objects.count()}")
print(f"Collections  : {Collection.objects.count()}")
print(f"Products     : {Product.objects.count()}")
print(f"Customers    : {Customer.objects.count()}")
print(f"Addresses    : {Address.objects.count()}")
print(f"Orders       : {Order.objects.count()}")
print(f"Order Items  : {OrderItem.objects.count()}")
print(f"Carts        : {Cart.objects.count()}")
print(f"Cart Items   : {CartItem.objects.count()}")
print("====================================")