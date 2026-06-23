"""
database.py
-----------
This file handles the database connection and configuration layer.
Key Responsibilities:
1. Configures the database engine to support SQLite (for local development) and PostgreSQL (for production/Neon) dynamically.
2. Defines the SQLAlchemy 'Product' model schema representing items in the directory.
3. Configures composite indexes on (created_at DESC, id DESC) and (category, created_at DESC, id DESC) to optimize the Keysets / Tuple queries for sub-millisecond execution.
4. Manages the database session life cycle ('get_db').
"""

import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Index
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./products.db")

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False, index=True)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

Index("ix_products_created_id", Product.created_at.desc(), Product.id.desc())
Index("ix_products_category_created_id", Product.category, Product.created_at.desc(), Product.id.desc())

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)
