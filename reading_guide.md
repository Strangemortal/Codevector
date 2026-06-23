# Project Code Reading Guide
============================

This guide outlines the recommended reading sequence to understand the architecture, data flow, and features of the **Fast Catalog** project. 

Read the files in the following order to trace how the backend connects to Supabase, generates data, exposes endpoints, and renders the frontend interface.

---

## 📂 Part 1: Configuration & Database Setup

Start here to understand the dependencies, configuration, and data connection:

1. **[requirements.txt](file:///c:/Users/BharatBK/Documents/projectss/code_vector/requirements.txt)**
   * *What it does*: Declares application libraries (`fastapi`, `uvicorn`, `supabase`, `python-dotenv`).
   * *Why it's first*: Establishes the tool stack we are using.

2. **[.env](file:///c:/Users/BharatBK/Documents/projectss/code_vector/.env)**
   * *What it does*: Holds the environment credentials (`SUPABASE_URL` and `SUPABASE_KEY`).
   * *Why it's next*: Supplies variables used by the database initialization code.

3. **[database.py](file:///c:/Users/BharatBK/Documents/projectss/code_vector/database.py)**
   * *What it does*: Configures and exports the official Supabase Client SDK instance.
   * *Why it's next*: Connects the backend server and seeders to your database.

---

## ⚡ Part 2: Database Seeding (Data Population)

Next, read how the mock data is generated and bulk-loaded:

4. **[seed.py](file:///c:/Users/BharatBK/Documents/projectss/code_vector/seed.py)**
   * *What it does*: Generates 200,000 products chronologically and inserts them in bulk batches of 2,000 over the REST API.
   * *Key Takeaway*: Note how dates are spaced by 5 seconds in memory to create a continuous chronological feed.

5. **[seed_2.py](file:///c:/Users/BharatBK/Documents/projectss/code_vector/seed_2.py)**
   * *What it does*: Appends 50 additional validation items with newer timestamps.
   * *Key Takeaway*: Used to simulate live concurrent updates to verify keyset pagination drift-resistance.

---

## 🚀 Part 3: Backend Server & APIs

Read the core API logic and the keyset pagination implementation:

6. **[main.py](file:///c:/Users/BharatBK/Documents/projectss/code_vector/main.py)**
   * *What it does*: Runs the FastAPI application, mounts public routes, and exposes `/api/products` and `/api/categories`.
   * *Key Takeaway*: Study the keyset cursor helper functions (`encode_cursor` and `decode_cursor`) and the PostgREST logical `.or_()` query:
     ```python
     query.or_(f"created_at.lt.{cursor_dt},and(created_at.eq.{cursor_dt},id.lt.{cursor_id})")
     ```
     This seeks composite indexes to achieve sub-millisecond page fetches.

---

## 🖥️ Part 4: Frontend Layout & Styles

Understand the layout and design systems before looking at interactive logic:

7. **[index.html](file:///c:/Users/BharatBK/Documents/projectss/code_vector/index.html)**
   * *What it does*: Standard layout template container. Holds the sidebar widgets, product grid layout, and script imports.
   * *Why it's first in UI*: Contains the static HTML structure before JavaScript hydration.

8. **[static/css/styles.css](file:///c:/Users/BharatBK/Documents/projectss/code_vector/static/css/styles.css)**
   * *What it does*: Premium design styling rules. Implements the dark-mode glassmorphic cards, responsive columns, and load animations.

---

## ⚙️ Part 5: Modular Frontend Logic

Finally, read the frontend feature modules to see how the client communicates with the APIs:

9. **[static/js/app.js](file:///c:/Users/BharatBK/Documents/projectss/code_vector/static/js/app.js)**
   * *What it does*: The entry point script. Declares the shared global state variables (active cursors and categories) and boots loading routines on DOM load.

10. **[static/js/toasts.js](file:///c:/Users/BharatBK/Documents/projectss/code_vector/static/js/toasts.js)**
    * *What it does*: Houses the success/error popups that display notifications.

11. **[static/js/categories.js](file:///c:/Users/BharatBK/Documents/projectss/code_vector/static/js/categories.js)**
    * *What it does*: Fetches distinct categories from the backend, renders sidebar pills, and resets pagination cursors on active filter swaps.

12. **[static/js/products.js](file:///c:/Users/BharatBK/Documents/projectss/code_vector/static/js/products.js)**
    * *What it does*: Fetches product lists from `/api/products` using active cursors, decodes base64 keyset anchors for log tracing, and prints the product grid.

13. **[static/js/injector.js](file:///c:/Users/BharatBK/Documents/projectss/code_vector/static/js/injector.js)**
    * *What it does*: Collects simulation form values and posts live injections to demonstrate concurrent data stability.

---

## 🛡️ Part 6: Git Exclusions

14. **[.gitignore](file:///c:/Users/BharatBK/Documents/projectss/code_vector/.gitignore)**
    * *What it does*: Ensures your sensitive keys in `.env` are ignored and never pushed to GitHub.
