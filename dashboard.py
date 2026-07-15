import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import os

from dotenv import load_dotenv  
load_dotenv()  

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

class RetailApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Retail Store Management System")
        self.root.geometry("950x700")
        self.root.configure(bg="#f4f6f9")
        
        # Connect to MySQL Database
        try:
            self.db = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD",
                database=os.getenv("DB_NAME")
            )
            self.cursor = self.db.cursor()

        except Exception as e:
            messagebox.showerror("Database Error", f"Could not connect to MySQL: {e}")
            self.root.destroy()
            return

        # Main Title
        title_label = tk.Label(root, text="🏬 Retail Store Management System", font=("Arial", 18, "bold"), fg="#2c3e50", bg="#f4f6f9")
        title_label.pack(pady=10)

        # Create Tabs Dashboard
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tab_inventory = tk.Frame(self.notebook, bg="#f4f6f9")
        self.notebook.add(self.tab_inventory, text=" 📦 Manage Inventory ")
        
        self.tab_billing = tk.Frame(self.notebook, bg="#f4f6f9")
        self.notebook.add(self.tab_billing, text=" 💳 Customer Billing (POS) ")

        self.setup_inventory_tab()
        self.setup_billing_tab()
        # ==================== INVENTORY SECTION ====================
    def setup_inventory_tab(self):
        table_frame = tk.Frame(self.tab_inventory, bg="#f4f6f9")
        table_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        columns = ("id", "name", "price", "stock")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=6)
        
        self.tree.heading("id", text="Product ID")
        self.tree.heading("name", text="Product Name")
        self.tree.heading("price", text="Price (INR)")
        self.tree.heading("stock", text="Available Stock")
        
        self.tree.column("id", width=80, anchor=tk.CENTER)
        self.tree.column("name", width=250, anchor=tk.W)
        self.tree.column("price", width=120, anchor=tk.E)
        self.tree.column("stock", width=120, anchor=tk.CENTER)
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<<TreeviewSelect>>", self.get_selected_row)

        form_frame = tk.LabelFrame(self.tab_inventory, text=" Product Details ", font=("Arial", 11, "bold"), bg="#ffffff", padx=15, pady=15)
        form_frame.pack(padx=20, pady=10, fill=tk.X)

        self.var_id = tk.StringVar()
        self.var_name = tk.StringVar()
        self.var_price = tk.StringVar()
        self.var_stock = tk.StringVar()

        tk.Label(form_frame, text="Product Name:", bg="#ffffff").grid(row=0, column=0, sticky=tk.W, pady=5)
        tk.Entry(form_frame, textvariable=self.var_name, width=30).grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Price (INR):", bg="#ffffff").grid(row=1, column=0, sticky=tk.W, pady=5)
        tk.Entry(form_frame, textvariable=self.var_price, width=15).grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)

        tk.Label(form_frame, text="Stock Qty:", bg="#ffffff").grid(row=1, column=2, sticky=tk.W, pady=5)
        tk.Entry(form_frame, textvariable=self.var_stock, width=15).grid(row=1, column=3, sticky=tk.W, padx=10, pady=5)

        btn_frame = tk.Frame(self.tab_inventory, bg="#f4f6f9")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="➕ Add", bg="#2ecc71", fg="white", width=10, command=self.add_product).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="🔄 Update", bg="#f39c12", fg="white", width=10, command=self.update_product).grid(row=0, column=1, padx=10)
        tk.Button(btn_frame, text="🗑️ Delete", bg="#e74c3c", fg="white", width=10, command=self.delete_product).grid(row=0, column=2, padx=10)
        tk.Button(btn_frame, text="🧹 Clear", bg="#7f8c8d", fg="white", width=10, command=self.clear_form).grid(row=0, column=3, padx=10)

        self.load_data_from_db()
        # ==================== BILLING SYSTEM SECTION ====================
    def setup_billing_tab(self):
        input_frame = tk.LabelFrame(self.tab_billing, text=" Scan / Enter Items ", font=("Arial", 11, "bold"), bg="#ffffff", padx=15, pady=15)
        input_frame.pack(padx=20, pady=10, fill=tk.X)

        self.bill_prod_id = tk.StringVar()
        self.bill_qty = tk.StringVar(value="1")

        tk.Label(input_frame, text="Product ID:", bg="#ffffff").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(input_frame, textvariable=self.bill_prod_id, width=10).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Quantity:", bg="#ffffff").grid(row=0, column=2, padx=5, pady=5)
        tk.Entry(input_frame, textvariable=self.bill_qty, width=8).grid(row=0, column=3, padx=5, pady=5)

        tk.Button(input_frame, text="🛒 Add to Cart", bg="#3498db", fg="white", command=self.add_to_cart).grid(row=0, column=4, padx=15)

        cart_frame = tk.Frame(self.tab_billing, bg="#f4f6f9")
        cart_frame.pack(padx=20, pady=5, fill=tk.BOTH, expand=True)

        cart_cols = ("id", "name", "price", "qty", "total")
        self.cart_tree = ttk.Treeview(cart_frame, columns=cart_cols, show="headings", height=8)
        
        self.cart_tree.heading("id", text="ID")
        self.cart_tree.heading("name", text="Product Name")
        self.cart_tree.heading("price", text="Price")
        self.cart_tree.heading("qty", text="Qty")
        self.cart_tree.heading("total", text="Total (INR)")
        
        self.cart_tree.column("id", width=50, anchor=tk.CENTER)
        self.cart_tree.column("name", width=250, anchor=tk.W)
        self.cart_tree.column("price", width=100, anchor=tk.E)
        self.cart_tree.column("qty", width=80, anchor=tk.CENTER)
        self.cart_tree.column("total", width=120, anchor=tk.E)
        self.cart_tree.pack(fill=tk.BOTH, expand=True)

        checkout_frame = tk.Frame(self.tab_billing, bg="#ffffff", height=80)
        checkout_frame.pack(fill=tk.X, padx=20, pady=10)

        self.lbl_grand_total = tk.Label(checkout_frame, text="Grand Total: ₹0.00", font=("Arial", 14, "bold"), bg="#ffffff", fg="#2c3e50")
        self.lbl_grand_total.pack(side=tk.LEFT, padx=20, pady=15)

        tk.Button(checkout_frame, text="💳 Checkout & Print PDF", font=("Arial", 12, "bold"), bg="#2ecc71", fg="white", padx=15, command=self.checkout_bill).pack(side=tk.RIGHT, padx=20, pady=10)

        self.cart_items = [] 
        self.grand_total = 0.0

    def add_to_cart(self):
        pid = self.bill_prod_id.get()
        qty_needed = self.bill_qty.get()

        if not pid or not qty_needed.isdigit():
            messagebox.showwarning("Input Error", "Please enter valid Product ID and Quantity.")
            return

        qty_needed = int(qty_needed)
        self.cursor.execute("SELECT name, price, stock_quantity FROM Products WHERE product_id = %s", (pid,))
        product = self.cursor.fetchone()

        if not product:
            messagebox.showerror("Not Found", "No product found with this ID!")
            return

        name, price, stock_available = product
        if stock_available < qty_needed:
            messagebox.showerror("Out of Stock", f"Only {stock_available} units available in inventory!")
            return

        item_total = float(price) * qty_needed
        self.cart_tree.insert("", tk.END, values=(pid, name, f"₹{price}", qty_needed, f"₹{item_total:.2f}"))
        self.cart_items.append({"id": pid, "name": name, "price": float(price), "qty": qty_needed, "subtotal": item_total})
        
        self.grand_total += item_total
        self.lbl_grand_total.config(text=f"Grand Total: ₹{self.grand_total:.2f}")
        self.bill_prod_id.set("")
        self.bill_qty.set("1")

    def checkout_bill(self):
        if not self.cart_items:
            messagebox.showwarning("Empty Cart", "No items inside the shopping cart!")
            return

        try:
            self.db.start_transaction()
            self.cursor.execute("INSERT INTO Invoices (total_amount) VALUES (%s)", (self.grand_total,))
            invoice_id = self.cursor.lastrowid

            for item in self.cart_items:
                self.cursor.execute(
                    "INSERT INTO InvoiceItems (invoice_id, product_id, quantity_sold, subtotal) VALUES (%s, %s, %s, %s)",
                    (invoice_id, item["id"], item["qty"], item["subtotal"])
                )
                self.cursor.execute(
                    "UPDATE Products SET stock_quantity = stock_quantity - %s WHERE product_id = %s",
                    (item["qty"], item["id"])
                )

            self.db.commit()
            
            # Generate the professional printable document
            self.generate_pdf_invoice(invoice_id, self.cart_items, self.grand_total)
            messagebox.showinfo("Success", f"Invoice #{invoice_id} processed! PDF generated.")
            
            # Clear Cart UI
            self.cart_items.clear()
            self.grand_total = 0.0
            self.lbl_grand_total.config(text="Grand Total: ₹0.00")
            for row in self.cart_tree.get_children():
                self.cart_tree.delete(row)
            self.load_data_from_db()

        except Exception as e:
            self.db.rollback()
            messagebox.showerror("Transaction Error", f"Checkout failed: {e}")

    # ==================== PDF MAKER ENGINE ====================
    def generate_pdf_invoice(self, invoice_id, items_list, grand_total):
        pdf_filename = f"Invoice_{invoice_id}.pdf"
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
        story = []
        
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=22, leading=26, textColor=colors.HexColor("#2c3e50"), alignment=1)
        meta_style = ParagraphStyle('MetaStyle', parent=styles['Normal'], fontSize=10, leading=14, textColor=colors.HexColor("#7f8c8d"))
        
        story.append(Paragraph("🏬 SUPERMARKET RETAIL SYSTEM", title_style))
        story.append(Spacer(1, 15))
        story.append(Paragraph(f"<b>Invoice ID:</b> #{invoice_id}<br/><b>Status:</b> PAID & VERIFIED", meta_style))
        story.append(Spacer(1, 15))
        
        table_data = [["Product Name", "Price", "Qty", "Subtotal"]]
        for item in items_list:
            table_data.append([item["name"], f"Rs. {item['price']:.2f}", str(item["qty"]), f"Rs. {item['subtotal']:.2f}"])
            
        table_data.append(["", "", "Grand Total:", f"Rs. {grand_total:.2f}"])
        
        invoice_table = Table(table_data, colWidths=[200, 100, 80, 100])
        invoice_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#34495e")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,0), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 8),
            ('ALIGN', (1,1), (-1,-1), 'RIGHT'),
            ('FONTNAME', (-2,-1), (-1,-1), 'Helvetica-Bold'),
            ('LINEBELOW', (0,0), (-1,-2), 0.5, colors.HexColor("#bdc3c7")),
            ('LINEABOVE', (2,-1), (3,-1), 1, colors.HexColor("#2c3e50")),
            ('TOPPADDING', (0,1), (-1,-1), 6),
            ('BOTTOMPADDING', (0,1), (-1,-1), 6),
        ]))
        
        story.append(invoice_table)
        story.append(Spacer(1, 30))
        story.append(Paragraph("<center>Thank you for shopping with us! Generated by Python Engine.</center>", meta_style))
        
        doc.build(story)
        try:
            os.startfile(pdf_filename)
        except Exception:
            pass

    # ==================== GENERAL LOGIC HELPERS ====================
    def load_data_from_db(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            self.cursor.execute("SELECT product_id, name, price, stock_quantity FROM Products;")
            for row in self.cursor.fetchall():
                self.tree.insert("", tk.END, values=row)
        except Exception as e:
            print(f"Database sync issue: {e}")

    def get_selected_row(self, event):
        selected_item = self.tree.focus()
        if not selected_item: return
        row = self.tree.item(selected_item)['values']
        self.var_id.set(row[0])
        self.var_name.set(row[1])
        self.var_price.set(row[2])
        self.var_stock.set(row[3])

    def add_product(self):
        try:
            query = "INSERT INTO Products (name, price, stock_quantity) VALUES (%s, %s, %s);"
            self.cursor.execute(query, (self.var_name.get(), float(self.var_price.get()), int(self.var_stock.get())))
            self.db.commit()
            self.clear_form()
            self.load_data_from_db()
        except Exception as e: messagebox.showerror("Error", f"{e}")

    def update_product(self):
        try:
            query = "UPDATE Products SET name=%s, price=%s, stock_quantity=%s WHERE product_id=%s;"
            self.cursor.execute(query, (self.var_name.get(), float(self.var_price.get()), int(self.var_stock.get()), self.var_id.get()))
            self.db.commit()
            self.clear_form()
            self.load_data_from_db()
        except Exception as e: messagebox.showerror("Error", f"{e}")

    def delete_product(self):
        if messagebox.askyesno("Confirm", "Delete item?"):
            try:
                self.cursor.execute("DELETE FROM Products WHERE product_id=%s;", (self.var_id.get(),))
                self.db.commit()
                self.clear_form()
                self.load_data_from_db()
            except Exception as e: messagebox.showerror("Error", f"{e}")

    def clear_form(self):
        self.var_id.set("")
        self.var_name.set("")
        self.var_price.set("")
        self.var_stock.set("")

if __name__ == "__main__":
    window = tk.Tk()
    app = RetailApp(window)
    window.mainloop()



