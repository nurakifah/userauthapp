import bcrypt
from db_connection import get_db_connection


def insert_user(username, email, password):
    """Inserts a new user into the users table with hashed password."""
    conn = get_db_connection()
    if conn is None:
        return

    try:
        cursor = conn.cursor()

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # SQL query to insert user
        insert_query = """
        INSERT INTO users (username, email, password_hash)
        VALUES (%s, %s, %s)
        """

        # Execute the query
        cursor.execute(insert_query, (username, email, hashed_password.decode('utf-8')))
        conn.commit()

        print(f"User '{username}' inserted successfully!")

    except Exception as e:
        print("Error inserting user:", e)

    finally:
        cursor.close()
        conn.close()

# Example usage
insert_user("bima", "bima@example.com", "securepassword123")

def verify_user(username, password):
    """Verifies a user's credentials."""
    conn = get_db_connection()
    if conn is None:
        return False

    try:
        cursor = conn.cursor()

        # SQL query to fetch the user by username
        select_query = """
        SELECT password_hash FROM users WHERE username = %s;
        """
        cursor.execute(select_query, (username,))
        result = cursor.fetchone()

        if result is None:
            print("User not found.")
            return False

        # Fetch the hashed password from the result
        stored_password_hash = result[0]

        # Verify the entered password against the stored hash
        if bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode('utf-8')):
            print("Login successful!")
            return True
        else:
            print("Invalid password.")
            return False

    except Exception as e:
        print("Error verifying user:", e)
        return False

    finally:
        cursor.close()
        conn.close()

# Example usage
if __name__ == "__main__":
    verify_user("bima", "securepassword123")

def reset_password(username, new_password):
    """Resets the user's password by hashing and updating it in the database."""
    conn = get_db_connection()
    if conn is None:
        return False

    try:
        cursor = conn.cursor()

        # Hash the new password
        new_hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

        # SQL query to update the password
        update_query = """
        UPDATE users SET password_hash = %s WHERE username = %s;
        """
        cursor.execute(update_query, (new_hashed_password.decode('utf-8'), username))
        conn.commit()

        if cursor.rowcount > 0:
            print(f"Password reset successful for user '{username}'.")
            return True
        else:
            print("User not found. Password reset failed.")
            return False

    except Exception as e:
        print("Error resetting password:", e)
        return False

    finally:
        cursor.close()
        conn.close()

# Example usage
if __name__ == "__main__":
    reset_password("john_doe", "new_secure_password456")