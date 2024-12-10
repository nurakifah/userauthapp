import pyotp
import psycopg2
from db_connection import get_db_connection

def generate_mfa_secret(username):
    """Generates and saves a new MFA secret for the user."""
    conn = get_db_connection()
    if conn is None:
        return None

    try:
        cursor = conn.cursor()

        # Generate a new TOTP secret (base32 encoded)
        mfa_secret = pyotp.random_base32()

        # SQL query to update the user's MFA secret
        update_query = """
        UPDATE users SET mfa_secret = %s WHERE username = %s;
        """
        cursor.execute(update_query, (mfa_secret, username))
        conn.commit()

        if cursor.rowcount > 0:
            print(f"MFA secret generated and saved for user '{username}': {mfa_secret}")
            return mfa_secret
        else:
            print("User not found. MFA secret not generated.")
            return None

    except Exception as e:
        print("Error generating MFA secret:", e)
        return None

    finally:
        cursor.close()
        conn.close()

def get_totp_code(mfa_secret):
    """Generates a TOTP code using the user's MFA secret."""
    totp = pyotp.TOTP(mfa_secret)
    return totp.now()

def verify_totp_code(username, code):
    """Verifies the TOTP code entered by the user."""
    conn = get_db_connection()
    if conn is None:
        return False

    try:
        cursor = conn.cursor()

        # Fetch the user's MFA secret from the database
        select_query = """
        SELECT mfa_secret FROM users WHERE username = %s;
        """
        cursor.execute(select_query, (username,))
        result = cursor.fetchone()

        if result is None:
            print("User not found.")
            return False

        mfa_secret = result[0]
        totp = pyotp.TOTP(mfa_secret)

        if totp.verify(code):
            print("TOTP verification successful!")
            return True
        else:
            print("Invalid TOTP code.")
            return False

    except Exception as e:
        print("Error verifying TOTP code:", e)
        return False

    finally:
        cursor.close()
        conn.close()