
import sqlite3

def update_challenges():
    conn = sqlite3.connect('backend/ecoloop.db')
    cursor = conn.cursor()
    try:
        # Update daily challenges (reward 50 -> 20)
        cursor.execute("UPDATE challenges SET coin_reward = 20 WHERE type = 'daily'")
        
        # Update weekly challenges (reward > 20 -> 20)
        cursor.execute("UPDATE challenges SET coin_reward = 20 WHERE type = 'weekly'")
        
        conn.commit()
        print("Challenges updated to 20 coins.")
        
        # Verify
        cursor.execute("SELECT title, coin_reward, type FROM challenges")
        for row in cursor.fetchall():
            print(f"{row[0]} ({row[2]}): {row[1]}")
            
    except Exception as e:
        print(f"Error updating DB: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    update_challenges()
