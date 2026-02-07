import sqlite3
import logging
from typing import List, Tuple

DB_NAME = "bot_database.db"

def init_db():
    """Initializes the database with the users table."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            full_name TEXT,
            username TEXT,
            joined_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    logging.info("Database initialized.")

def add_user(user_id: int, full_name: str, username: str):
    """Adds a new user to the database if they don't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT OR IGNORE INTO users (id, full_name, username) VALUES (?, ?, ?)", 
                       (user_id, full_name, username))
        conn.commit()
    except Exception as e:
        logging.error(f"Error adding user: {e}")
    finally:
        conn.close()

def get_users_count() -> int:
    """Returns the total number of users."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_all_users() -> List[Tuple[int]]:
    """Returns a list of all user IDs."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users")
    users = cursor.fetchall()
    conn.close()
    return users
