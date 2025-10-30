import sqlite3
from backend.database import get_db_connection
from datetime import datetime

# USER CRUD OPERATIONS
def create_user(name, email, password):
    """Create a new user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, password)
        )
        user_id = cursor.lastrowid
        conn.commit()
        return {"success": True, "user_id": user_id}
    except sqlite3.IntegrityError:
        return {"success": False, "error": "Email already exists"}
    finally:
        conn.close()

def get_user_by_id(user_id):
    """Get a user by their ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return dict(user)
    return None

def get_all_users():
    """Get all users"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    
    return [dict(user) for user in users if user]

def update_user(user_id, name=None, email=None, password=None):
    """Update a user's information"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    updates = []
    params = []
    
    if name:
        updates.append("name = ?")
        params.append(name)
    if email:
        updates.append("email = ?")
        params.append(email)
    if password:
        updates.append("password = ?")
        params.append(password)
    
    if updates:
        params.append(user_id)
        query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, params)
        conn.commit()
    
    conn.close()
    return {"success": True}

def delete_user(user_id):
    """Delete a user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    
    return {"success": True}


# E-WASTE RECORD CRUD OPERATIONS
def add_ewaste_record(user_id, item_type, quantity, location, collection_date, status="Pending"):
    """Add a new e-waste record"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO ewaste_records 
        (user_id, item_type, quantity, location, collection_date, status) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, item_type, quantity, location, collection_date, status))
    
    record_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return {"success": True, "record_id": record_id}

def get_ewaste_record_by_id(record_id):
    """Get an e-waste record by its ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM ewaste_records WHERE record_id = ?
    ''', (record_id,))
    record = cursor.fetchone()
    conn.close()
    
    if record:
        return dict(record)
    return None

def get_all_ewaste_records():
    """Get all e-waste records with user information"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT r.*, u.name as user_name, u.email as user_email
        FROM ewaste_records r
        LEFT JOIN users u ON r.user_id = u.id
        ORDER BY r.collection_date DESC
    ''')
    records = cursor.fetchall()
    conn.close()
    
    return [dict(record) for record in records if record]

def update_ewaste_record(record_id, user_id=None, item_type=None, quantity=None, 
                        location=None, collection_date=None, status=None):
    """Update an e-waste record"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    updates = []
    params = []
    
    if user_id is not None:
        updates.append("user_id = ?")
        params.append(user_id)
    if item_type:
        updates.append("item_type = ?")
        params.append(item_type)
    if quantity is not None:
        updates.append("quantity = ?")
        params.append(quantity)
    if location:
        updates.append("location = ?")
        params.append(location)
    if collection_date:
        updates.append("collection_date = ?")
        params.append(collection_date)
    if status:
        updates.append("status = ?")
        params.append(status)
    
    if updates:
        params.append(record_id)
        query = f"UPDATE ewaste_records SET {', '.join(updates)} WHERE record_id = ?"
        cursor.execute(query, params)
        conn.commit()
    
    conn.close()
    return {"success": True}

def delete_ewaste_record(record_id):
    """Delete an e-waste record"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM ewaste_records WHERE record_id = ?", (record_id,))
    conn.commit()
    conn.close()
    
    return {"success": True}

def get_user_ewaste_records(user_id):
    """Get all e-waste records for a specific user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM ewaste_records WHERE user_id = ?
        ORDER BY collection_date DESC
    ''', (user_id,))
    records = cursor.fetchall()
    conn.close()
    
    return [dict(record) for record in records if record]

def get_ewaste_statistics():
    """Get statistics about e-waste records"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Total records
    cursor.execute("SELECT COUNT(*) as total FROM ewaste_records")
    total = cursor.fetchone()['total']
    
    # Records by status
    cursor.execute("SELECT status, COUNT(*) as count FROM ewaste_records GROUP BY status")
    status_counts = cursor.fetchall()
    
    # Records by item type
    cursor.execute("SELECT item_type, COUNT(*) as count FROM ewaste_records GROUP BY item_type")
    type_counts = cursor.fetchall()
    
    conn.close()
    
    return {
        "total_records": total,
        "status_counts": {row['status']: row['count'] for row in status_counts},
        "type_counts": {row['item_type']: row['count'] for row in type_counts}
    }