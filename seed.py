"""
seed.py
-------
This script handles the initial mock seeding of the database.
Key Responsibilities:
1. Formulates 200,000 distinct mock products with randomized names, categories, and prices.
2. Spacers creation dates chronologically so they represent a continuous historical feed.
3. Wipes out any existing catalog items to allow fresh, clean runs.
4. Performs batch inserts in chunks of 2,000 using the Supabase client SDK over HTTP REST APIs.
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

def generate_products(count=200000):
    print(f"Generating {count} products in memory...")
    products = []
    base_time = datetime.utcnow()
    
    for i in range(count):
        adj = random.choice(PRODUCT_ADJECTIVES)
        noun = random.choice(PRODUCT_NOUNS)
        cat = random.choice(CATEGORIES)
        name = f"{adj} {noun} #{i+1}"
        price = round(random.uniform(5.0, 999.0), 2)
        created_at = base_time - timedelta(seconds=i * 5)
        
        products.append({
            "name": name,
            "category": cat,
            "price": price,
            "created_at": created_at.isoformat(),
            "updated_at": created_at.isoformat()
        })
    return products

def seed_db(count=200000):
    products = generate_products(count)
    
    print(f"Inserting {count} products into the Supabase database...")
    start_time = time.time()
    
    # Clear existing products
    print("Clearing existing products from Supabase...")
    try:
        supabase.table("products").delete().gt("id", 0).execute()
    except Exception as e:
        print(f"Warning during delete: {e}. Attempting to proceed...")
    
    batch_size = 2000
    total_batches = count // batch_size
    
    for i in range(0, count, batch_size):
        batch = products[i:i+batch_size]
        supabase.table("products").insert(batch).execute()
        if (i // batch_size + 1) % 5 == 0 or i // batch_size + 1 == total_batches:
            print(f"Inserted batch {i // batch_size + 1}/{total_batches}...")
            
    end_time = time.time()
    print(f"Successfully seeded {count} products in {end_time - start_time:.2f} seconds!")

if __name__ == "__main__":
    seed_db()
