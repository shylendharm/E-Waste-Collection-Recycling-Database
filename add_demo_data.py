from backend.models import create_user, add_ewaste_record

def add_demo_data():
    """Add demo data to the database for demonstration purposes"""
    print("Adding demo data to the database...")
    
    # Create some demo users
    users_data = [
        ("John Smith", "john.smith@college.edu", "password123"),
        ("Sarah Johnson", "sarah.j@college.edu", "password123"),
        ("Michael Brown", "michael.b@college.edu", "password123"),
        ("Emily Davis", "emily.d@college.edu", "password123"),
        ("David Wilson", "david.w@college.edu", "password123")
    ]
    
    user_ids = []
    for name, email, password in users_data:
        result = create_user(name, email, password)
        if result['success']:
            user_ids.append(result['user_id'])
            print(f"Created user: {name} (ID: {result['user_id']})")
        else:
            print(f"Failed to create user: {name} - {result.get('error', 'Unknown error')}")
    
    # Create some demo e-waste records
    ewaste_data = [
        (user_ids[0], "Laptop", 2, "Main Campus Computer Lab", "2025-10-10", "Collected"),
        (user_ids[0], "Phone", 1, "Student Center", "2025-10-12", "Pending"),
        (user_ids[1], "Tablet", 1, "Library", "2025-10-08", "Collected"),
        (user_ids[1], "Battery", 5, "Science Building", "2025-10-14", "Pending"),
        (user_ids[2], "Monitor", 2, "IT Department", "2025-10-05", "Collected"),
        (user_ids[2], "Keyboard", 3, "Main Campus Computer Lab", "2025-10-11", "Collected"),
        (user_ids[3], "Mouse", 4, "Engineering Building", "2025-10-09", "Pending"),
        (user_ids[3], "Laptop", 1, "Student Dormitory", "2025-10-13", "Pending"),
        (user_ids[4], "Desktop Computer", 1, "Admin Building", "2025-10-07", "Collected"),
        (user_ids[4], "Printer", 1, "Library", "2025-10-14", "Pending"),
    ]
    
    for user_id, item_type, quantity, location, date, status in ewaste_data:
        result = add_ewaste_record(user_id, item_type, quantity, location, date, status)
        if result['success']:
            print(f"Added record: {item_type} (ID: {result['record_id']}) for user {user_id}")
        else:
            print(f"Failed to add record: {item_type} - {result.get('error', 'Unknown error')}")
    
    print("\nDemo data added successfully!")
    print(f"Created {len(user_ids)} users and {len(ewaste_data)} e-waste records.")

if __name__ == "__main__":
    add_demo_data()