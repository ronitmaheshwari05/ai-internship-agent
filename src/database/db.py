import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


# -------------------------------
# Connection (RELIABLE)
# -------------------------------
def get_connection():
    try:
        return psycopg2.connect(
            DATABASE_URL,
            connect_timeout=3,
            sslmode="require"
        )
    except Exception as e:
        print("DB CONNECTION ERROR:", e)
        return None


# -------------------------------
# Create Table
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

    conn.commit()
    cur.close()
    conn.close()


# -------------------------------
# Insert Search
# -------------------------------
def insert_search(skills, location, response):
    conn = get_connection()
    if conn is None:
        return None

    cur = conn.cursor()

    cur.execute("""
        INSERT INTO public.searches (skills, location, response)
        VALUES (%s, %s, %s)
        RETURNING id
    """, (skills, location, response))

    search_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    print("✅ INSERTED:", search_id)   # debug confirmation

    return search_id


# -------------------------------
# Get Cached Search
# -------------------------------
def get_cached_search(skills, location):
    conn = get_connection()
    if conn is None:
        return None

    cur = conn.cursor()

    cur.execute("""
        SELECT id, skills, location, response
        FROM public.searches
        WHERE LOWER(skills) = LOWER(%s)
        AND LOWER(location) = LOWER(%s)
        ORDER BY id DESC
        LIMIT 1
    """, (skills.strip(), location.strip()))

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
# Get Recent Searches (FIXED)
# -------------------------------
def get_recent_searches(limit=5):
    conn = get_connection()
    if conn is None:
        return []

    cur = conn.cursor()

    cur.execute("""
        SELECT id, skills, location, response
        FROM public.searches
        ORDER BY id DESC
        LIMIT %s
    """, (limit,))

    rows = cur.fetchall()

    cur.close()
    conn.close()

    # convert to clean dict list
    results = []
    for row in rows:
        results.append({
            "id": row[0],
            "skills": row[1],
            "location": row[2],
            "response": row[3]
        })

    return results


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

    print("🗑 DELETED:", search_id)
