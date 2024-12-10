import bcrypt
import psycopg2

def get_db_connection():
    print("Attempting to connect to the database...")  # Debug message
    try:
        conn = psycopg2.connect(
            dbname="user_auth_db",  # Your database name
            user="postgres",   # Your username
            password="12345",  # Your password
            host="localhost",        # Host (localhost if running locally)
            port="5432"              # The port (usually 5432)
        )
        print("Connected to the database!")  # Success message
        return conn
    except Exception as e:
        print("Error connecting to the database:", e)  # Error message
        return None

# Call the function to test
get_db_connection()
