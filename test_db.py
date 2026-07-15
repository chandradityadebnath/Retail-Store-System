import mysql.connector
import os
from dotenv import load_dotenv


load_dotenv()

try:
    # Connect securely using environment variables
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    if connection.is_connected():
        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        
        print("🎉 SUCCESS! Python is connected to MySQL securely.")
        print(f"MySQL Server Version: {db_version}")
        
        # Clean up and close connection
        cursor.close()
        connection.close()

except Exception as error:
    print("❌ CONNECTION FAILED!")
    print(f"Error Details: {error}")
