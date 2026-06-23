"""
main.py
-------
This is the main application server file built with FastAPI.
Key Responsibilities:
1. Mounts the static directory to serve modular styles and script assets.
2. Implements the paginated catalog endpoint 'GET /api/products' using optimized tuple comparison logic.
3. Implements base64 encoding and decoding functions for direction-aware (next/prev) cursors.
4. Implements endpoint 'GET /api/categories' to list distinct categories.
5. Implements endpoint 'POST /api/products' to simulate a single live creation.
6. Serves the root 'index.html' file on the landing route.
"""

import os
import base64
from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, Depends, Query, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, tuple_
from database import get_db, Product, init_db

app = FastAPI(title="CodeVector High-Performance Product Directory")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

def encode_cursor(direction: str, dt: datetime, item_id: int) -> str:
    cursor_str = f"{direction}:{dt.isoformat()},{item_id}"
    return base64.urlsafe_b64encode(cursor_str.encode()).decode()

def decode_cursor(cursor_str: str) -> tuple[str, datetime, int]:
    try:
        decoded = base64.urlsafe_b64decode(cursor_str.encode()).decode()
        direction, val_str = decoded.split(":", 1)
        dt_str, item_id_str = val_str.split(",")
        return direction, datetime.fromisoformat(dt_str), int(item_id_str)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid cursor format")

@app.get("/api/products")
def get_products(
    limit: int = Query(20, ge=1, le=100),
    category: Optional[str] = Query(None),
    cursor: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Product)
    
    if category:
        query = query.filter(Product.category == category)
        
    if cursor:
        direction, cursor_dt, cursor_id = decode_cursor(cursor)
        
        if direction == "next":
            query = query.filter(
                tuple_(Product.created_at, Product.id) < (cursor_dt, cursor_id)
            ).order_by(desc(Product.created_at), desc(Product.id))
        elif direction == "prev":
            query = query.filter(
                tuple_(Product.created_at, Product.id) > (cursor_dt, cursor_id)
            ).order_by(asc(Product.created_at), asc(Product.id))
        else:
            raise HTTPException(status_code=400, detail="Invalid cursor direction")
    else:
        direction = "next"
        query = query.order_by(desc(Product.created_at), desc(Product.id))

    items = query.limit(limit + 1).all()
    
    has_more = len(items) > limit
    if has_more:
        items = items[:limit]
        
    if direction == "prev":
        items.reverse()
        
    next_cursor = None
    prev_cursor = None
    
    if items:
        if (direction == "next" and has_more) or (direction == "prev"):
            next_cursor = encode_cursor("next", items[-1].created_at, items[-1].id)
            
        if (direction == "prev" and has_more) or (direction == "next" and cursor is not None):
            prev_cursor = encode_cursor("prev", items[0].created_at, items[0].id)
            
    return {
        "items": [
            {
                "id": p.id,
                "name": p.name,
                "category": p.category,
                "price": p.price,
                "created_at": p.created_at.isoformat(),
                "updated_at": p.updated_at.isoformat()
            } for p in items
        ],
        "next_cursor": next_cursor,
        "prev_cursor": prev_cursor
    }

@app.get("/api/categories")
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Product.category).distinct().all()
    return [c[0] for c in categories]

@app.post("/api/products")
def create_product(
    name: str, 
    category: str, 
    price: float, 
    db: Session = Depends(get_db)
):
    new_product = Product(
        name=name,
        category=category,
        price=price,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {
        "id": new_product.id,
        "name": new_product.name,
        "category": new_product.category,
        "price": new_product.price,
        "created_at": new_product.created_at.isoformat(),
        "updated_at": new_product.updated_at.isoformat()
    }

@app.get("/", response_class=HTMLResponse)
def get_index():
    index_path = os.path.join(os.path.dirname(__file__), "index.html")
    if not os.path.exists(index_path):
        raise HTTPException(status_code=404, detail="Frontend file not found")
    with open(index_path, "r", encoding="utf-8") as f:
        return f.read()

@app.on_event("startup")
def startup_event():
    init_db()
