import mysql.connector
import os
from dotenv import load_dotenv


load_dotenv()

try:
    # 1. Connect to MySQL Server securely using environment variables
    db = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")  
    )
    cursor = db.cursor()

    # 2. Create the Database
    cursor.execute("CREATE DATABASE IF NOT EXISTS RetailStore;")
    cursor.execute("USE RetailStore;")
    print("📦 Database 'RetailStore' initialized.")

    # 3. Create Products Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Products (
        product_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        price DECIMAL(10, 2) NOT NULL,
        stock_quantity INT NOT NULL
    );
    """)
    print("✔️ 'Products' table verified.")

    # 4. Create Invoices Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Invoices (
        invoice_id INT AUTO_INCREMENT PRIMARY KEY,
        sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        total_amount DECIMAL(10, 2) NOT NULL
    );
    """)
    print("✔️ 'Invoices' table verified.")

    # 5. Create InvoiceItems Table (with Foreign Keys)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS InvoiceItems (
        item_id INT AUTO_INCREMENT PRIMARY KEY,
        invoice_id INT,
        product_id INT,
        quantity_sold INT NOT NULL,
        subtotal DECIMAL(10, 2) NOT NULL,
        FOREIGN KEY (invoice_id) REFERENCES Invoices(invoice_id) ON DELETE CASCADE,
        FOREIGN KEY (product_id) REFERENCES Products(product_id)
    );
    """)
    print("✔️ 'InvoiceItems' table verified.")

    # 6. Add some mock/dummy data so your store isn't empty!
    cursor.execute("SELECT COUNT(*) FROM Products;")
    if cursor.fetchone()[0] == 0:
        mock_products = [
            ("Gaming Mouse", 1200.00, 50),
            ("Mechanical Keyboard", 3500.00, 20),
            ("HDMI Cable 2m", 450.00, 100),
            ("Wireless Headset", 2800.00, 15)
        ]
        cursor.executemany("INSERT INTO Products (name, price, stock_quantity) VALUES (%s, %s, %s);", mock_products)
        db.commit()
        print("🚀 Successfully loaded initial inventory items!")

    cursor.close()
    db.close()
    print("\n🎉 SETUP COMPLETE! Your database schema matches professional software standards.")

except Exception as e:
    print(f"❌ Setup failed: {e}")
