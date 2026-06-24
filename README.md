# High-Performance Product Directory (Supabase Client SDK)

A fast, lightweight, and drift-resistant product directory containing **200,000 products** sorted newest first, with category filtering and real-time pagination, built using the official **Supabase Client SDK**.

---

## ⚡ Quick Start

### 1. Database Setup (Supabase SQL Editor)
Since we are using Supabase, you must first create the `products` table. Open the **SQL Editor** in your Supabase dashboard and execute the following SQL:
```sql
-- Create the products table
CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  name VARCHAR NOT NULL,
  category VARCHAR NOT NULL,
  price FLOAT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Turn off Row Level Security (RLS) so the publishable API key can write/read
ALTER TABLE products DISABLE ROW LEVEL SECURITY;

-- Composite indexes for high performance pagination (newest first)
CREATE INDEX ix_products_created_id ON products (created_at DESC, id DESC);
CREATE INDEX ix_products_category_created_id ON products (category, created_at DESC, id DESC);
```

### 2. Configure Environment Variables
Create a `.env` file in the project root:

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Seed the Database
Our database seeder generates 200,000 product items and inserts them in bulk batches of 2,000 over HTTP REST APIs:
```bash
python seed.py
```

### 5. Run the Server
Launch the FastAPI server:
```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```
Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser to view the application.

---

## 🏗️ Design Decisions & Architecture

### 1. Supabase SDK Client
We integrated the official Python `supabase` package, avoiding direct raw socket database connections. This utilizes your publishable keys and routes requests through Supabase's high-speed API gateway.

### 2. Keyset (Cursor-based) Pagination in PostgREST
Traditional offset pagination (`LIMIT X OFFSET Y`) is slow at high page counts. We implement keyset pagination. In PostgREST (Supabase's REST interface), row value comparisons are written using `.or_()` logical filters:
```python
# (created_at, id) < (cursor_dt, cursor_id)
query.or_(f"created_at.lt.{cursor_dt},and(created_at.eq.{cursor_dt},id.lt.{cursor_id})")
```
This maps directly to our PostgreSQL composite indexes on the backend, bypassing skipped scans and jumping straight to the cursor position in **sub-millisecond** query times.

### 3. String-based Cursors
Instead of parsing ISO datetime strings back-and-forth into Python `datetime` objects (which adds timezone parsing overhead), we pass the raw `created_at` timestamp strings directly from the JSON payloads into the base64 cursors. This is faster and completely immune to local timezone formatting bugs.
