# Implementation Plan: High-Performance Product Directory with Drift-Resistant Pagination

This document outlines the design and implementation plan for building a product browsing backend capable of paginating, filtering, and sorting 200,000 products.

## Goal Description

The task is to build a fast backend to browse ~200,000 products (newest first), filter by category, and paginate through them. The system must:
1. Be fast even at high page numbers.
2. Prevent duplicate or skipped items (data drift) when new products are added or existing products are updated while a user is browsing.
3. Include a fast data-seeding script (avoiding slow single-row loops).
4. Provide a simple optional UI to browse the data.

### Architectural Choices

* **Backend Framework**: **FastAPI (Python)**. It is fast, modern, asynchronous, and provides built-in Swagger documentation (`/docs`) for easy testing.
* **Database**: **PostgreSQL** (hosted on Neon for production/live URL). For local development, we will support both a local PostgreSQL instance and a local **SQLite** database (ensuring the SQL syntax is fully compatible).
* **Pagination Strategy**: **Keyset (Cursor-based) Pagination**.
  * Traditional Offset Pagination (`LIMIT X OFFSET Y`) becomes slow ($O(N)$) for large datasets (e.g. `OFFSET 150000`) and suffers from data drift (if 50 products are added at the top, page 2 will show products already shown on page 1).
  * Keyset Pagination uses a cursor (based on the sorting columns, `(created_at, id)`) to retrieve the next set of rows. The database query is:
    ```sql
    WHERE created_at < :cursor_created_at 
       OR (created_at = :cursor_created_at AND id < :cursor_id)
    ```
    This is extremely fast ($O(\log N)$ with indexes) and completely immune to insertions at the top of the list.

---

## User Review Required

> [!IMPORTANT]
> **Pagination UI Limitation**
> Cursor-based pagination only supports **Next / Previous** navigation (or infinite scroll) and does not natively support jumping to a specific page number (e.g., "Go to Page 45"). We recommend this approach as it is standard for modern feeds (like Twitter, LinkedIn, product lists) and ensures $O(\log N)$ query speeds.
>
> **If arbitrary page jumping is strictly required**, we will need to use Offset Pagination, but we will lock pagination queries to a session snapshot timestamp (e.g., `WHERE created_at <= :session_start_time`) to prevent data drift. However, this will be slower for deep pages. We propose **Cursor-based Pagination** by default.

---

## Open Questions

> [!NOTE]
> 1. **Local Setup Preference**: Do you prefer to use local SQLite for zero-setup local testing, or a local PostgreSQL instance? We will build the seed script and backend to automatically support both via an environment variable.
> 2. **Category Names**: Should we generate a standard set of categories (e.g., "Electronics", "Clothing", "Home", "Books", "Beauty") for the 200,000 seeded products?

---

## Proposed Changes

### Backend Component (Python / FastAPI)

#### [NEW] [requirements.txt](file:///c:/Users/BharatBK/Documents/projectss/code_vector/requirements.txt)
List of Python dependencies, including `fastapi`, `uvicorn`, `psycopg2-binary` (or `psycopg` for postgres), and `sqlalchemy` or raw SQL helper `databases`.

#### [NEW] [database.py](file:///c:/Users/BharatBK/Documents/projectss/code_vector/database.py)
Database connection manager that handles:
* Connecting to SQLite (locally) or PostgreSQL (Neon/Production).
* Executing queries.
* Creating the schema and indexes.

#### [NEW] [seed.py](file:///c:/Users/BharatBK/Documents/projectss/code_vector/seed.py)
Seeding script that generates 200,000 products:
* Generates data in memory using list comprehensions.
* Uses bulk insertion (`executemany` or PostgreSQL `COPY` syntax) in batches of 10,000 to complete the seeding in **under 5 seconds**.
* Automatically creates index on `(category, created_at DESC, id DESC)` and `(created_at DESC, id DESC)`.

#### [NEW] [main.py](file:///c:/Users/BharatBK/Documents/projectss/code_vector/main.py)
FastAPI application containing:
* `GET /api/products`: Fetch products paginated with keyset pagination.
  * Query parameters: `limit` (default 20), `category` (optional filter), `cursor` (encoded string containing `created_at` and `id`).
  * Returns: list of products, next page cursor, previous page cursor.
* Static file mounting for the frontend UI.

---

### Frontend Component (HTML/CSS/JS)

#### [NEW] [index.html](file:///c:/Users/BharatBK/Documents/projectss/code_vector/index.html)
A premium-looking single page UI:
* A modern, elegant dark-mode glassmorphism interface (Tailwind CSS or Vanilla CSS).
* Category filter tabs/dropdowns.
* Product grid cards displaying Name, Category, Price, and Created At.
* Responsive design.
* Pagination controls ("Next Page" and "Previous Page" buttons, or Infinite Scroll).

---

## Verification Plan

### Automated Tests
* We will write a validation script to test that pagination does not miss or duplicate products under concurrent insertion.
* Run API benchmarks using `ab` or a Python script to measure API response times for deep pagination pages.

### Manual Verification
* Start the server locally: `uvicorn main:app --reload`.
* Open the browser and test pagination and filtering.
* Insert 50 products mid-browsing and verify that the page transition remains smooth and correct.
