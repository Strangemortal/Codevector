"""
seed_2.py
---------
This script appends additional products to the database without wiping existing data.
Key Responsibilities:
1. Generates 50 new items with custom names, categories, and prices.
2. Formulates timestamps newer than the baseline to simulate new product entries.
3. Appends the items directly into the existing database tables.
4. Helps verify pagination state transitions and data-drift resistance (verifying that no duplicates are generated on deep pages).
"""

import os
import random
import time
from datetime import datetime, timedelta
from database import supabase

CATEGORIES = [
    "Electronics", "Clothing", "Home & Kitchen", "Books", 
    "Beauty & Health", "Sports & Outdoors", "Toys & Games", "Automotive"
]

PRODUCT_ADJECTIVES = [
    "Premium", "Super", "Eco", "Smart", "Ultra", "Mega", 
    "Pocket", "Classic", "Deluxe", "Pro", "Wireless", "Portable"
]

PRODUCT_NOUNS = [
    "Gadget", "Widget", "Device", "Apparel", "Tool", "Book", 
    "Cream", "Gear", "Toy", "Charger", "Bottle", "Organizer"
]

def generate_new_products(count=50):
    print(f"Generating {count} new products in memory...")
    products = []
    base_time = datetime.utcnow()
    
    for i in range(count):
        adj = random.choice(PRODUCT_ADJECTIVES)
        noun = random.choice(PRODUCT_NOUNS)
        cat = random.choice(CATEGORIES)
        name = f"Injected Batch Item #{i+1} ({adj} {noun})"
        price = round(random.uniform(10.0, 500.0), 2)
        created_at = base_time + timedelta(seconds=i * 2)
        
        products.append({
            "name": name,
            "category": cat,
            "price": price,
            "created_at": created_at.isoformat(),
            "updated_at": created_at.isoformat()
        })
    return products

def append_db(count=50):
    products = generate_new_products(count)
    
    print(f"Appending {count} products to the database...")
    start_time = time.time()
    
    supabase.table("products").insert(products).execute()
            
    end_time = time.time()
    print(f"Successfully appended {count} products in {end_time - start_time:.4f} seconds!")

if __name__ == "__main__":
    append_db()
