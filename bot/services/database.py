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
            language TEXT DEFAULT 'uz',
            joined_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Migration: Add last_active if it exists in an older database
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
    except sqlite3.OperationalError:
        pass # Column already exists
    
    # Migration: Add language if it exists in an older database
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN language TEXT DEFAULT 'uz'")
    except sqlite3.OperationalError:
        pass

    # Settings table: user_id | key | value
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            user_id INTEGER,
            key TEXT,
            value TEXT,
            PRIMARY KEY (user_id, key)
        )
    """)
    # New table for file statistics
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS files_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            filename TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    logging.info("Database initialized.")

def add_user(user_id: int, full_name: str, username: str):
    """Adds a new user or updates their last_active if they exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (id, full_name, username, last_active) 
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(id) DO UPDATE SET 
                full_name = excluded.full_name,
                username = excluded.username,
                last_active = CURRENT_TIMESTAMP
        """, (user_id, full_name, username))
        conn.commit()
    except sqlite3.OperationalError as e:
        if "no column named language" in str(e).lower():
            cursor.execute("ALTER TABLE users ADD COLUMN language TEXT DEFAULT 'uz'")
            cursor.execute("""
                INSERT INTO users (id, full_name, username, last_active) 
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(id) DO UPDATE SET 
                    full_name = excluded.full_name,
                    username = excluded.username,
                    last_active = CURRENT_TIMESTAMP
            """, (user_id, full_name, username))
            conn.commit()
    except Exception as e:
        logging.error(f"Error adding/updating user: {e}")
    finally:
        conn.close()

def get_user_language(user_id: int) -> str:
    """Gets the language preference for a user."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT language FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 'uz'

def set_user_language(user_id: int, lang: str):
    """Sets the language preference for a user."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET language = ? WHERE id = ?", (lang, user_id))
    conn.commit()
    conn.close()

def update_last_active(user_id: int):
    """Updates the last_active timestamp for a user."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE users SET last_active = CURRENT_TIMESTAMP WHERE id = ?", (user_id,))
        conn.commit()
    except Exception as e:
        logging.error(f"Error updating activity: {e}")
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

def get_active_users_count(days: int = 1) -> int:
    """Returns the number of active users in the last N days."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM users WHERE last_active >= datetime('now', ?)", 
        (f'-{days} days',)
    )
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

def get_users_detailed() -> List[Tuple]:
    """Returns all user data for export."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, full_name, username, joined_date, last_active FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

def update_user_setting(user_id: int, key: str, value: str):
    """Updates or inserts a user setting."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO settings (user_id, key, value) VALUES (?, ?, ?)
            ON CONFLICT(user_id, key) DO UPDATE SET value = excluded.value
        """, (user_id, key, value))
        conn.commit()
    except Exception as e:
        logging.error(f"Error updating setting: {e}")
    finally:
        conn.close()

def get_user_setting(user_id: int, key: str, default: str = None) -> str:
    """Returns the value of a user setting."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM settings WHERE user_id = ? AND key = ?", (user_id, key))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else default

def log_file_upload(user_id: int, filename: str, storage_path: str = None):
    """Logs a file upload event with optional storage path."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO files_log (user_id, filename, storage_path) VALUES (?, ?, ?)", 
            (user_id, filename, storage_path)
        )
        conn.commit()
    except Exception as e:
        # Check if storage_path column exists, if not, add it (simple migration)
        if "no such column: storage_path" in str(e).lower():
            cursor.execute("ALTER TABLE files_log ADD COLUMN storage_path TEXT")
            cursor.execute(
                "INSERT INTO files_log (user_id, filename, storage_path) VALUES (?, ?, ?)", 
                (user_id, filename, storage_path)
            )
            conn.commit()
        else:
            logging.error(f"Error logging file: {e}")
    finally:
        conn.close()

def get_user_files_history(user_id: int, limit: int = 5):
    """Returns the last N files uploaded by a user."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, filename, storage_path, timestamp FROM files_log "
        "WHERE user_id = ? AND storage_path IS NOT NULL "
        "ORDER BY timestamp DESC LIMIT ?", 
        (user_id, limit)
    )
    files = cursor.fetchall()
    conn.close()
    return files

def get_total_files_count() -> int:
    """Returns total number of files processed."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM files_log")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_files_count_period(days: int = 1) -> int:
    """Returns number of files processed in the last N days."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM files_log WHERE timestamp >= datetime('now', ?)", 
        (f'-{days} days',)
    )
    count = cursor.fetchone()[0]
    conn.close()
    return count
