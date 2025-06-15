# Database file for managing the database with SQLite. I learnt how to use SQLite myself, as we weren't taught it in class.

import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_file):
        """Initialize database connection and create tables if they don't exist."""
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self._create_tables()
    
    def _create_tables(self):
        """Create database tables if they don't exist."""
        # This looks like a really long string, but it's actually a multi-line sql command string.
        self.cursor.executescript('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password_hash TEXT NOT NULL,
                joined_date TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS cart_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                item_name TEXT,
                price REAL,
                quantity INTEGER,
                FOREIGN KEY (username) REFERENCES users(username)
            );

            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                order_date TEXT,
                total_amount REAL,
                final_amount REAL,
                budget REAL,
                discount_applied REAL,
                FOREIGN KEY (username) REFERENCES users(username)
            );

            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER,
                item_name TEXT,
                price REAL,
                quantity INTEGER,
                FOREIGN KEY (order_id) REFERENCES orders(id)
            );
        ''')
        self.conn.commit()
    
    def add_user(self, username, password_hash):
        """Add a new user to the database."""
        try:
            self.cursor.execute(
                'INSERT INTO users (username, password_hash, joined_date) VALUES (?, ?, ?)',
                (username, password_hash, datetime.now().strftime("%Y-%m-%d"))
            )
            self.conn.commit()
            # Returns True if user can be added
            return True
        # Returns False if user already exists, although I don't think we will encounter this error as we already check if the username exists in the get_user function. This may only be relevant in something like a web application, or something where multiple users can be running the program at the same time.
        except sqlite3.IntegrityError:
            return False
    
    def get_user(self, username):
        """Get user data from database."""
        self.cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        # fetchone() returns a single row as a tuple, or None if no user found
        return self.cursor.fetchone() # Returns username and password hash and join date.
    
    def get_cart(self, username):
        """Get all cart items for a user."""
        self.cursor.execute(
            'SELECT item_name, price, quantity FROM cart_items WHERE username = ?',
            (username,)
        )
        # Returns a dictionary with item names as keys and a dictionary of price and quantity  as values.
        return {row[0]: {"price": row[1], "quantity": row[2]} for row in self.cursor.fetchall()}
    
    def update_cart(self, username, cart):
        """Update user's cart with new items."""
        # Delete existing cart items for current user
        self.cursor.execute('DELETE FROM cart_items WHERE username = ?', (username,))
        
        # This function, rather than just deleting one specific item from a cart, it deletes the whole user's cart, then updates it with the user's temporary cart from self.items

        # Insert new cart items
        for item_name, details in cart.items():
            self.cursor.execute(
                'INSERT INTO cart_items (username, item_name, price, quantity) VALUES (?, ?, ?, ?)',
                (username, item_name, details['price'], details['quantity']) # price and quantity are in square brackets because it correlates to the keys in the dictionary.
            )
        self.conn.commit()
    
    def save_order(self, username, cart_items, total, final_amount, budget, discount):
        """Save order with budget and discount info."""
        order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Save order summary
        self.cursor.execute(
            'INSERT INTO orders (username, order_date, total_amount, final_amount, budget, discount_applied) VALUES (?, ?, ?, ?, ?, ?)',
            (username, order_date, total, final_amount, budget, discount)
        )
        order_id = self.cursor.lastrowid
        
        # Save individual order items
        for item_name, details in cart_items.items():
            self.cursor.execute(
                'INSERT INTO order_items (order_id, item_name, price, quantity) VALUES (?, ?, ?, ?)',
                (order_id, item_name, details['price'], details['quantity'])
            )
        
        self.conn.commit()

    def get_order_history(self, username):
        """Get user's order history."""
        # Get all orders for user
        self.cursor.execute('''
            SELECT id, order_date, total_amount, final_amount, budget, discount_applied 
            FROM orders 
            WHERE username = ? 
            ORDER BY order_date DESC''', (username,))
        orders = self.cursor.fetchall()

        # For each order, get its items
        complete_history = []
        for order in orders:
            order_id, date, total, final, budget, discount = order
            
            # Get items for this order
            self.cursor.execute('''
                SELECT item_name, price, quantity 
                FROM order_items 
                WHERE order_id = ?''', (order_id,))
            items = self.cursor.fetchall()
            
            # Combine order info with its items
            complete_history.append({
                'date': date,
                'total': total,
                'final_amount': final,
                'budget': budget,
                'discount': discount,
                'items': items
            })
        
        return complete_history

    def close(self):
        """Close database connection."""
        self.conn.close()
