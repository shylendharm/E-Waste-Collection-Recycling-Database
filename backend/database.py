import sqlite3
import os

def get_db_connection():
    """Create and return a database connection"""
    # Ensure the database directory exists relative to the project root
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database', 'e_waste.db'))
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    return conn

def create_tables():
    """Create the users and ewaste_records tables if they don't exist"""
    conn = get_db_connection()
    
    # Create users table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    
    # Create ewaste_records table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS ewaste_records (
            record_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            item_type TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            location TEXT NOT NULL,
            collection_date TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending',
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database connected successfully")

if __name__ == "__main__":
    # Create tables
    create_tables()