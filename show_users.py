
import sqlite3
import os

# Define the database path
db_path = os.path.join(os.getcwd(), 'backend', 'ecoloop.db')

if not os.path.exists(db_path):
    print(f"Error: Database not found at {db_path}")
    exit(1)

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query to fetch all users
    cursor.execute("SELECT id, username, email, hashed_password FROM users")
    users = cursor.fetchall()

    if not users:
        print("No users found in the database.")
    else:
        print("\n--- User Data ---")
        print(f"{'ID':<5} {'Username':<20} {'Email':<30} {'Password (Hashed)':<60}")
        print("-" * 115)
        for user in users:
            uid, username, email, password = user
            print(f"{uid:<5} {username:<20} {email:<30} {password:<60}")
        print("-" * 115)

    conn.close()

except sqlite3.Error as e:
    print(f"Database error: {e}")
