import sqlite3

class InventorySystem:
    def __init__(self):
        self.conn = sqlite3.connect("inventory.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNI QUE,
            email TEXT UNIQUE,
            role TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT UNIQUE
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS suppliers(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            supplier_name TEXT,
            phone TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS products(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            category_id INTEGER,
            supplier_id INTEGER,
            quantity INTEGER,
            price REAL,

            FOREIGN KEY(category_id)
            REFERENCES categories(id),

            FOREIGN KEY(supplier_id)
            REFERENCES suppliers(id)
        )
        """)

        self.conn.commit()

    def add_user(self):

        username = input("Username: ")
        email = input("Email: ")
        role = input("Role: ")

        self.cursor.execute("""
        INSERT INTO users(username,email,role)
        VALUES(?,?,?)
        """,(username,email,role))

        self.conn.commit()

        print("User Added Successfully")

    def add_category(self):

        name = input("Category Name: ")

        self.cursor.execute("""
        INSERT INTO categories(category_name)
        VALUES(?)
        """,(name,))

        self.conn.commit()

        print("Category Added")

    def add_supplier(self):

        supplier = input("Supplier Name: ")
        phone = input("Phone: ")

        self.cursor.execute("""
        INSERT INTO suppliers(
        supplier_name,
        phone)

        VALUES(?,?)
        """,(supplier,phone))

        self.conn.commit()

        print("Supplier Added")

    def add_product(self):

        name = input("Product Name: ")
        category = int(input("Category ID: "))
        supplier = int(input("Supplier ID: "))
        quantity = int(input("Quantity: "))
        price = float(input("Price: "))

        self.cursor.execute("""
        INSERT INTO products(

        product_name,
        category_id,
        supplier_id,
        quantity,
        price

        )

        VALUES(?,?,?,?,?)

        """,(name,
             category,
             supplier,
             quantity,
             price))

        self.conn.commit()

        print("Product Added")

    def view_products(self):

        self.cursor.execute("""

        SELECT
        p.id,
        p.product_name,
        c.category_name,
        s.supplier_name,
        p.quantity,
        p.price

        FROM products p

        LEFT JOIN categories c
        ON p.category_id=c.id

        LEFT JOIN suppliers s
        ON p.supplier_id=s.id

        """)

        products = self.cursor.fetchall()

        print("\n===== PRODUCT LIST =====")

        for item in products:

            total = item[4] * item[5]

            print(f"""
ID          : {item[0]}
Name        : {item[1]}
Category    : {item[2]}
Supplier    : {item[3]}
Quantity    : {item[4]}
Price       : {item[5]}
Total Value : {total}

---------------------------
""")

    def update_product(self):

        pid = int(input("Product ID: "))
        quantity = int(input("New Quantity: "))
        price = float(input("New Price: "))

        self.cursor.execute("""

        UPDATE products

        SET quantity=?,
            price=?

        WHERE id=?

        """,(quantity,
             price,
             pid))

        self.conn.commit()

        print("Product Updated")

    def delete_product(self):

        pid = int(input("Product ID: "))

        self.cursor.execute("""
        DELETE FROM products
        WHERE id=?
        """,(pid,))

        self.conn.commit()

        print("Product Deleted")

    def menu(self):

        while True:

            print("""
==============================
 INVENTORY MANAGEMENT SYSTEM
==============================

1.Add User
2.Add Category
3.Add Supplier
4.Add Product
5.View Products
6.Update Product
7.Delete Product
8.Exit

""")

            choice = input("Enter Choice: ")

            if choice == "1":
                self.add_user()

            elif choice == "2":
                self.add_category()

            elif choice == "3":
                self.add_supplier()

            elif choice == "4":
                self.add_product()

            elif choice == "5":
                self.view_products()

            elif choice == "6":
                self.update_product()

            elif choice == "7":
                self.delete_product()

            elif choice == "8":
                print("Thank You")
                self.conn.close()
                break

            else:
                print("Invalid Choice")


inventory = InventorySystem()
inventory.menu()