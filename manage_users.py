
import sqlite3
import os

# Define the database path
db_path = os.path.join(os.getcwd(), 'backend', 'ecoloop.db')

if not os.path.exists(db_path):
    print(f"Error: Database not found at {db_path}")
    exit(1)

def get_connection():
    return sqlite3.connect(db_path)

def list_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email FROM users")
    users = cursor.fetchall()
    conn.close()

    if not users:
        print("\n[!] No users found in the database.")
    else:
        print("\n--- User List ---")
        print(f"{'ID':<5} {'Username':<20} {'Email':<30}")
        print("-" * 60)
        for user in users:
            uid, username, email = user
            print(f"{uid:<5} {username:<20} {email:<30}")
        print("-" * 60)

def delete_user(user_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute("SELECT username FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        
        if not user:
            print(f"\n[!] User with ID {user_id} not found.")
            conn.close()
            return

        # Confirm deletion
        confirm = input(f"Are you sure you want to delete user '{user[0]}' (ID: {user_id})? (yes/no): ").lower()
        if confirm == 'yes':
            # Delete related data first (optional but good for cleanup)
            cursor.execute("DELETE FROM user_progress WHERE user_id = ?", (user_id,))
            cursor.execute("DELETE FROM user_challenge_completions WHERE user_id = ?", (user_id,))
            cursor.execute("DELETE FROM user_items WHERE user_id = ?", (user_id,))
            
            # Delete user
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            print(f"\n[✓] User '{user[0]}' (ID: {user_id}) and their data deleted successfully.")
        else:
            print("\n[x] Deletion cancelled.")
            
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

def delete_all_users():
    try:
        confirm = input("\n[WARNING] This will delete ALL users and their progress. This cannot be undone.\nType 'DELETE' to confirm: ")
        if confirm == 'DELETE':
            conn = get_connection()
            cursor = conn.cursor()
            
            # Clear all related tables
            cursor.execute("DELETE FROM user_progress")
            cursor.execute("DELETE FROM user_challenge_completions")
            cursor.execute("DELETE FROM user_items")
            cursor.execute("DELETE FROM users")
            
            conn.commit()
            print("\n[✓] All users and related data have been wiped.")
            conn.close()
        else:
            print("\n[x] Operation cancelled.")
    except Exception as e:
         print(f"Error: {e}")

def main():
    while True:
        print("\n=== EcoLoop User Manager ===")
        print("1. List Users")
        print("2. Delete User by ID")
        print("3. Delete ALL Users")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '1':
            list_users()
        elif choice == '2':
            uid = input("Enter User ID to delete: ")
            if uid.isdigit():
                delete_user(int(uid))
            else:
                print("Invalid ID.")
        elif choice == '3':
            delete_all_users()
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
