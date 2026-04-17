import sqlite3
from datetime import datetime

DB_name = "internship_agent.db"

def get_connection():
    return sqlite3.connect(DB_name)

def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS search_history (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        skills TEXT,

        location TEXT,

        response TEXT,

        created_at TIMESTAMP

    )

    """)

    conn.commit()
    conn.close()


def insert_search(skills, location, response):
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO search_history (skills, location, response, created_at)

    VALUES (?, ?, ?, ?)

    """, (skills, location, response, datetime.now()))

    conn.commit()

    conn.close()

def get_recent_searches(limit=5):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT skills, location, response, created_at

    FROM search_history

    ORDER BY created_at DESC

    LIMIT ?

    """, (limit,))

    results = cursor.fetchall()

    conn.close()

    return results