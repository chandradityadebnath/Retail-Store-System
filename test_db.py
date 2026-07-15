import mysql.connector as mysql

try:
    # Connect to your local MySQL Server
    
    connection = mysql.connect(
        host="localhost",
        user="root",
        password="Jeet"
    )

    if connection.is_connected():
        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        
        print("🎉 SUCCESS! Python is connected to MySQL.")
        print(f"MySQL Server Version: {db_version[0]}")
        
        # Clean up and close connection
        cursor.close()
        connection.close()

except Exception as error:
    print("❌ CONNECTION FAILED!")
    print(f"Error Details: {error}")
