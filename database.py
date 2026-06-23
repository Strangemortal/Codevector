"""
database.py
-----------
This file initializes the connection to the remote Supabase service.
Key Responsibilities:
1. Loads environment variables (SUPABASE_URL and SUPABASE_KEY).
2. Initializes the Supabase Client SDK instance.
3. Exports the client instance for use in seeding and main server endpoints.
"""

import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)
