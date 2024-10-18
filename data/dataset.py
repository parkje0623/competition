import pandas as pd
import numpy as np
from faker import Faker
import random

# Initialize Faker to generate realistic customer data
fake = Faker()

# Set random seed for reproducibility
random.seed(42)
Faker.seed(42)

# 1. Define Product Types and Price Range
products = {
    'Smartphone': [
        { 'sku': 'SP001', 'price': 1299, 'rating': 5 },
        { 'sku': 'SP002', 'price': 299, 'rating': 2 },
        { 'sku': 'SP003', 'price': 399, 'rating': 4 },
        { 'sku': 'SP004', 'price': 399, 'rating': 3 },
        { 'sku': 'SP005', 'price': 899, 'rating': 5 }
    ],
    'Laptop': [
        { 'sku': 'LP001', 'price': 2599, 'rating': 5 },
        { 'sku': 'LP002', 'price': 799, 'rating': 2 },
        { 'sku': 'LP003', 'price': 1799, 'rating': 4 },
        { 'sku': 'LP004', 'price': 1099, 'rating': 4 },
        { 'sku': 'LP005', 'price': 1399, 'rating': 4 }
    ],
    'Tablet': [
        { 'sku': 'TB001', 'price': 1599, 'rating': 5 },
        { 'sku': 'TB002', 'price': 299, 'rating': 2 },
        { 'sku': 'TB003', 'price': 399, 'rating': 2 },
        { 'sku': 'TB004', 'price': 349, 'rating': 3 },
        { 'sku': 'TB005', 'price': 599, 'rating': 3 }
    ],
    'Smartwatch': [
        { 'sku': 'SW001', 'price': 799, 'rating': 5 },
        { 'sku': 'SW002', 'price': 199, 'rating': 3 },
        { 'sku': 'SW003', 'price': 99, 'rating': 4 },
        { 'sku': 'SW004', 'price': 399, 'rating': 5 },
        { 'sku': 'SW005', 'price': 199, 'rating': 5 }
    ]
}

# 2. Shipping Options and Payment Methods
shipping_types = ['Standard', 'Express']

# 3. Addons and Addon Prices
addons = [
    {'name': 'Accessory', 'price': 29},
    {'name': 'Extended Warranty', 'price': 199},
    {'name': 'Screen Protector', 'price': 19},
    {'name': 'Charger', 'price': 35},
    {'name': 'Headphone', 'price': 99}    
]

# Function: Calculate Total Price and Addon Price
def calculate_prices(unit_price, selected_addons):
    addon_price = sum(addon['price'] for addon in selected_addons)
    total_price = unit_price + addon_price
    return total_price, addon_price

# 4. Generate Dataset
data = []
customer_info = {}
# Generate 100000 unique customer IDs
customer_pool = [fake.uuid4() for _ in range(100000)]
for _ in range(50000):
    # User Information
    customer_id = random.choices(customer_pool, k=1)[0]

    if customer_id in customer_info:
        # If existing Customer, keep the same info
        customer_data = customer_info[customer_id]
        age = customer_data['age']
        gender = customer_data['gender']
        if customer_data['loyalty_member'] == 'No':
            # 50% chance of being a member if repeated customer
            loyalty_member = 'Yes' if random.random() < 0.9 else 'No'
        else:
            loyalty_member = 'Yes'
    else:
        # If non-existing customer, create a new info
        age = int(random.triangular(18, 80, 35))
        gender = random.choice(['Male', 'Female'])
        loyalty_member = random.choice(['Yes', 'No'])

        # Store customer for repeated customers
        customer_info[customer_id] = {
            'age': age,
            'gender': gender,
            'loyalty_member': loyalty_member
        }

    # Select Random Product Category to Purchase
    product_type = random.choice(list(products.keys()))
    selected_product_list = products[product_type]
    # Define weights for biased random towards better rating products
    ratings = [product['rating'] for product in selected_product_list]
    weights = [rating / sum(ratings) for rating in ratings]

    # Choose Product
    selected_product = random.choices(selected_product_list, weights=weights, k=1)[0]
    unit_price = selected_product['price']
    sku = selected_product['sku']
    rating = selected_product['rating']

    # Select random add-ons, but the possibility of a customer buying add-on is 10%
    selected_addons = random.choices(addons, k=random.randint(1, 3)) if random.random() < 0.1 else ''
    addon_item = ', '.join([addon['name'] for addon in selected_addons])
    total_price, addon_price = calculate_prices(unit_price, selected_addons)

    # Assign random date and shipping info
    purchase_date = fake.date_between(start_date='-7y', end_date='today')
    shipping_type = random.choice(shipping_types)

    # Save the data into an array
    data.append([
        customer_id, age, gender, loyalty_member,
        product_type, sku, rating, unit_price, purchase_date, 
        shipping_type, addon_item, addon_price, total_price
    ])

# 5. Save into a DataFrame and Export into CSV
columns = [
    'Customer ID', 'Age', 'Gender', 'Loyalty Member',
    'Product Type', 'SKU', 'Rating', 'Unit Price', 'Purchase Date', 
    'Shipping Type', 'Addon Item', 'Addon Price', 'Total Price'
]
customer_data = pd.DataFrame(data, columns=columns)
customer_data.to_csv('../sales-dashboard/public/data/customer_sales_data.csv', index=False)