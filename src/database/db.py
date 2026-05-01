import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


# -------------------------------
# Connection
# -------------------------------
def get_connection():
    return psycopg2.connect(DATABASE_URL)


# -------------------------------
# Create Table
# -------------------------------
def create_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS searches (
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
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO searches (skills, location, response)
        VALUES (%s, %s, %s)
        RETURNING id
        """,
        (skills, location, response)
    )

    search_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return search_id


# -------------------------------
# Get Cached Search
# -------------------------------
def get_cached_search(skills, location):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute(
        """
        SELECT * FROM searches
        WHERE LOWER(skills) = LOWER(%s)
        AND LOWER(location) = LOWER(%s)
        ORDER BY id DESC
        LIMIT 1
        """,
        (skills.strip(), location.strip())
    )

    result = cur.fetchone()

    cur.close()
    conn.close()

    return result


# -------------------------------
# Get Recent Searches
# -------------------------------
def get_recent_searches(limit=5):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute(
        """
        SELECT * FROM searches
        ORDER BY id DESC
        LIMIT %s
        """,
        (limit,)
    )

    results = cur.fetchall()

    cur.close()
    conn.close()

    return results


# -------------------------------
# Delete Search
# -------------------------------
def delete_search(search_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM searches WHERE id = %s",
        (search_id,)
    )

    conn.commit()
    cur.close()
    conn.close()


# -------------------------------
# Clear All
# -------------------------------
def clear_history():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM searches")

    conn.commit()
    cur.close()
    conn.close()
