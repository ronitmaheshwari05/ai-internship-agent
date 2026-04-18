import sqlite3
from datetime import datetime
from src.database.models import SearchHistory

DB_NAME = "internship_agent.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS search_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            skills TEXT NOT NULL,
            location TEXT NOT NULL,
            response TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL
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
        SELECT id, skills, location, response, created_at
        FROM search_history
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return [SearchHistory(*row) for row in rows]


def delete_search(search_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM search_history
        WHERE id = ?
    """, (search_id,))

    conn.commit()
    conn.close()


def clear_history():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM search_history
    """)

    conn.commit()
    conn.close()