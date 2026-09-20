# 🏬 Retail Store Billing & Inventory System

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange?logo=mysql)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-lightgrey)
![ReportLab](https://img.shields.io/badge/PDF-ReportLab-red)


Hi! I built this project right before starting my B.Tech CSE degree. My goal was to take the basic Python and MySQL foundations I learned in school and scale them up into a complete, usable desktop app that a real shopkeeper could use.

Instead of writing simple terminal text scripts, I wanted to see how a professional system connects a visual interface, a live database, and automated document generation.

## Things the App does:

*   **Owner Inventory Tab:** A backend panel where store owners can visually see stock levels, add new products, adjust prices, or remove old items directly into a MySQL database.
*   **Cashier Billing Tab:** A point-of-sale customer screen where you enter a Product ID and quantity. The system automatically verifies if there is enough stock in MySQL, calculates running totals, and adds items to a shopping cart grid.
*   **Automatic PDF Receipts:** When you click checkout, the app uses `ReportLab` to immediately generate a clean, print-ready PDF invoice (`Invoice_#.pdf`) and opens it on screen.
*   **Stock Auto-Deduction:** The checkout system instantly updates the main inventory database table, subtracting the purchased quantities in real-time.

---

##  Skills I Practiced & Applied:

*   **Python (GUI Layouts):** Used `Tkinter` and `ttk` to handle the grid layouts, tabs, pop-up warning messages, and data tables.
*   **Relational Databases (MySQL):** Designed a three-table relational system with foreign keys to link products to dynamic invoice rows.
*   **Data Security (.env Integration):** Learned how to use `python-dotenv` to safely hide my local database passwords so they never leak online when I upload to GitHub.

---

## Database Structure:

This is how my MySQL tables are structured and linked together:

```sql
CREATE DATABASE RetailStore;
USE RetailStore;

-- 1. Holds item details
CREATE TABLE Products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INT NOT NULL
);

-- 2. Holds master billing records
CREATE TABLE Invoices (
    invoice_id INT AUTO_INCREMENT PRIMARY KEY,
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2) NOT NULL
);

-- 3. This includes junction table linking products bought to specific invoices
CREATE TABLE InvoiceItems (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    invoice_id INT,
    product_id INT,
    quantity_sold INT NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (invoice_id) REFERENCES Invoices(invoice_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);
```

---

##  How to Run It Locally :

### 1. Set Up Environment Variables

Create a file named `.env` in the project folder and insert your local database connection details:
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=RetailStore
```

### 2. Run the Scripts :
Open your terminal inside the folder and execute:
```bash
# 1. Install required helper libraries
py -m pip install mysql-connector-python reportlab python-dotenv

# 2. Build the database and insert sample products
py setup_database.py

# 3. Launch the application window
py dashboard.py
```
---
*Built by **Chandraditya Debnath** as a self-taught project before joining college.*
