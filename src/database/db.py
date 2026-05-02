import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


# -------------------------------
# Connection
# -------------------------------
def get_connection():
    try:
        return psycopg2.connect(
            DATABASE_URL,
            connect_timeout=5,
            sslmode="require"
        )
    except Exception as e:
        print("DB CONNECTION ERROR:", e)
        return None


# -------------------------------
# Normalize Input
# -------------------------------
def normalize(text):
    return text.strip().lower()


# -------------------------------
# Create Table (NO user_id)
# -------------------------------
def create_table():
    conn = get_connection()
    if conn is None:
        return

    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS public.searches (
            id SERIAL PRIMARY KEY,
            skills TEXT NOT NULL,
            location TEXT NOT NULL,
            response TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Index for fast lookup
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_search_lookup
        ON public.searches (LOWER(skills), LOWER(location))
    """)

    conn.commit()
    cur.close()
    conn.close()


# -------------------------------
# Insert Search (GLOBAL)
# -------------------------------
def insert_search(skills, location, response):
    conn = get_connection()
    if conn is None:
        return None

    cur = conn.cursor()

    skills = normalize(skills)
    location = normalize(location)

    try:
        cur.execute("""
            INSERT INTO public.searches (skills, location, response)
            VALUES (%s, %s, %s)
            RETURNING id
        """, (skills, location, response))

        result = cur.fetchone()
        conn.commit()

        return result[0] if result else None

    except Exception as e:
        print("INSERT ERROR:", e)
        return None

    finally:
        cur.close()
        conn.close()


# -------------------------------
# Get Cached Search (GLOBAL)
# -------------------------------
def get_cached_search(skills, location):
    conn = get_connection()
    if conn is None:
        return None

    cur = conn.cursor()

    skills = normalize(skills)
    location = normalize(location)

    cur.execute("""
        SELECT id, skills, location, response
        FROM public.searches
        WHERE LOWER(skills) = %s
        AND LOWER(location) = %s
        LIMIT 1
    """, (skills, location))

    row = cur.fetchone()

    cur.close()
    conn.close()

    if row:
        return {
            "id": row[0],
            "skills": row[1],
            "location": row[2],
            "response": row[3]
        }

    return None


# -------------------------------
# Get Recent Searches (GLOBAL)
# -------------------------------
def get_recent_searches(limit=5):
    conn = get_connection()
    if conn is None:
        return []

    cur = conn.cursor()

    cur.execute("""
        SELECT id, skills, location, response
        FROM public.searches
        ORDER BY created_at DESC
        LIMIT %s
    """, (limit,))

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {
            "id": row[0],
            "skills": row[1],
            "location": row[2],
            "response": row[3]
        }
        for row in rows
    ]


# -------------------------------
# Delete Search
# -------------------------------
def delete_search(search_id):
    conn = get_connection()
    if conn is None:
        return

    cur = conn.cursor()

    cur.execute(
        "DELETE FROM public.searches WHERE id = %s",
        (search_id,)
    )

    conn.commit()
    cur.close()
    conn.close()
