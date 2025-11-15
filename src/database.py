import sqlite3
from sqlite3 import Error
import os # <-- Added 'os' library

# --- PATH FIX ---
# Get the absolute path of the directory containing this file (i.e., 'src')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Create the path to the DB file (inside the 'src' directory)
DATABASE_NAME = os.path.join(BASE_DIR, "library.db")
# ---------------------

def connect_db():
    """ Creates a connection to the SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        # Enable Foreign Key support (very important)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
    
    return conn

def create_tables(conn):
    """ Creates tables in the database based on the design """
    if conn is None:
        print("Error! No database connection.")
        return

    # 1. User Table (Central table)
    sql_create_user_table = """
    CREATE TABLE IF NOT EXISTS User (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        name TEXT,
        email TEXT UNIQUE,
        phone TEXT,
        user_type TEXT NOT NULL CHECK(user_type IN ('admin', 'librarian', 'reader'))
    );
    """

    # 2. Books Table
    sql_create_books_table = """
    CREATE TABLE IF NOT EXISTS books (
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT,
        genre TEXT,
        status TEXT NOT NULL DEFAULT 'available' CHECK(status IN ('available', 'borrowed'))
    );
    """

    # 3. Reader Table (Inherits from User)
    sql_create_reader_table = """
    CREATE TABLE IF NOT EXISTS READER (
        reader_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL UNIQUE,
        membership_date TEXT,
        total_borrowed INTEGER DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES User (user_id) ON DELETE CASCADE
    );
    """

    # 4. Librarian Table (Inherits from User)
    sql_create_librarian_table = """
    CREATE TABLE IF NOT EXISTS LIBRARIAN (
        librarian_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL UNIQUE,
        staff_id TEXT NOT NULL UNIQUE,
        role TEXT,
        hire_date TEXT,
        FOREIGN KEY (user_id) REFERENCES User (user_id) ON DELETE CASCADE
    );
    """

    # 5. Admin Table (Inherits from User)
    # Note: As per models.py, Admin inherits Librarian,
    # Must ensure when creating an Admin, they ALSO have a LIBRARIAN record.
    sql_create_admin_table = """
    CREATE TABLE IF NOT EXISTS ADMIN (
        admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL UNIQUE,
        privileged_level TEXT,
        FOREIGN KEY (user_id) REFERENCES User (user_id) ON DELETE CASCADE
    );
    """

    # 6. Borrowing Record Table
    sql_create_borrowing_table = """
    CREATE TABLE IF NOT EXISTS BORROWING_RECORD (
        record_id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id INTEGER NOT NULL,
        reader_id INTEGER NOT NULL,
        borrow_date TEXT NOT NULL,
        due_date TEXT NOT NULL,
        return_date TEXT,
        fine_amount REAL DEFAULT 0,
        FOREIGN KEY (book_id) REFERENCES books (book_id),
        FOREIGN KEY (reader_id) REFERENCES READER (reader_id)
    );
    """

    try:
        c = conn.cursor()
        c.execute(sql_create_user_table)
        c.execute(sql_create_books_table)
        c.execute(sql_create_reader_table)
        c.execute(sql_create_librarian_table)
        c.execute(sql_create_admin_table)
        c.execute(sql_create_borrowing_table)
        
        print("Tables created successfully (or already exist).")
    except Error as e:
        print(f"Error creating tables: {e}")

# ===============================================
# ===== CRUD FUNCTIONS (CREATE, READ, UPDATE, DELETE) =====
# ===============================================

def db_add_user(conn, username, password, name, email, phone, user_type):
    """Adds a new user and returns the user_id"""
    sql = ''' INSERT INTO User(username, password, name, email, phone, user_type)
              VALUES(?,?,?,?,?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (username, password, name, email, phone, user_type))
        conn.commit()
        return cur.lastrowid # Return the ID of the just-created user
    except sqlite3.IntegrityError as e:
        print(f"Error: Username '{username}' or Email '{email}' already exists. {e}")
        return None
    except Error as e:
        print(f"Error adding user: {e}")
        return None

def db_add_reader(conn, user_id, membership_date):
    """Adds a new reader (linked to user_id)"""
    sql = ''' INSERT INTO READER(user_id, membership_date) VALUES(?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (user_id, membership_date))
        conn.commit()
        return cur.lastrowid
    except Error as e:
        print(f"Error adding reader: {e}")
        return None

def db_get_user_by_username(conn, username):
    """Gets user info by username"""
    sql = "SELECT * FROM User WHERE username = ?"
    cur = conn.cursor()
    cur.execute(sql, (username,))
    # fetchone() returns one row as a tuple
    return cur.fetchone()

# --- NEW FUNCTION 1 ---
def db_get_reader_by_user_id(conn, user_id):
    """Gets Reader details by user_id"""
    sql = "SELECT reader_id, membership_date, total_borrowed FROM READER WHERE user_id = ?"
    cur = conn.cursor()
    cur.execute(sql, (user_id,))
    return cur.fetchone()

# --- NEW FUNCTION 2 ---
def db_get_librarian_by_user_id(conn, user_id):
    """Gets Librarian details by user_id"""
    sql = "SELECT librarian_id, staff_id, role, hire_date FROM LIBRARIAN WHERE user_id = ?"
    cur = conn.cursor()
    cur.execute(sql, (user_id,))
    return cur.fetchone()

# --- NEW FUNCTION 3 ---
def db_get_admin_by_user_id(conn, user_id):
    """Gets Admin details by user_id"""
    sql = "SELECT admin_id, privileged_level FROM ADMIN WHERE user_id = ?"
    cur = conn.cursor()
    cur.execute(sql, (user_id,))
    return cur.fetchone()

def db_add_book(conn, title, author, genre, status='available'):
    """Adds a new book"""
    sql = ''' INSERT INTO books(title, author, genre, status)
              VALUES(?,?,?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (title, author, genre, status))
        conn.commit()
        return cur.lastrowid
    except Error as e:
        print(f"Error adding book: {e}")
        return None

def db_get_book_by_id(conn, book_id):
    """Gets book info by ID"""
    sql = "SELECT * FROM books WHERE book_id = ?"
    cur = conn.cursor()
    cur.execute(sql, (book_id,))
    return cur.fetchone()

def db_update_book_status(conn, book_id, new_status):
    """Updates the status of a book (available/borrowed)"""
    sql = "UPDATE books SET status = ? WHERE book_id = ?"
    try:
        cur = conn.cursor()
        cur.execute(sql, (new_status, book_id))
        conn.commit()
        return True
    except Error as e:
        print(f"Error updating book status: {e}")
        return False

def db_create_borrow_record(conn, book_id, reader_id, borrow_date, due_date):
    """Creates a new borrow record"""
    sql = ''' INSERT INTO BORROWING_RECORD(book_id, reader_id, borrow_date, due_date, fine_amount)
              VALUES(?,?,?,?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (book_id, reader_id, borrow_date, due_date, 0))
        conn.commit()
        return cur.lastrowid
    except Error as e:
        print(f"Error creating borrow record: {e}")
        return None

def db_update_return_record(conn, record_id, return_date, fine_amount):
    """Updates the record when a book is returned"""
    sql = "UPDATE BORROWING_RECORD SET return_date = ?, fine_amount = ? WHERE record_id = ?"
    try:
        cur = conn.cursor()
        cur.execute(sql, (return_date, fine_amount, record_id))
        conn.commit()
        return True
    except Error as e:
        print(f"Error updating return record: {e}")
        return False

def db_search_books(conn, keyword):
    """Finds books by title or author"""
    sql = "SELECT * FROM books WHERE title LIKE ? OR author LIKE ?"
    cur = conn.cursor()
    keyword_like = f"%{keyword}%" # Add % for wildcard search
    cur.execute(sql, (keyword_like, keyword_like))
    return cur.fetchall() # fetchall() returns a list of rows

# --- NAME ERROR FIX ---
# Moved this block to the END of the file
if __name__ == '__main__':
    # This code only runs when you execute database.py directly
    # with the command: python src/database.py
    
    print("Initializing database...")
    db_conn = connect_db()
    
    if db_conn is not None:
        create_tables(db_conn)
        
        # --- ADD 1 ADMIN/LIBRARIAN FOR TESTING ---
        try:
            print("Attempting to add test users 'admin' and 'lib'...")
            # 1. Create User "lib"
            user_lib_id = db_add_user(db_conn, "lib", "123", "Librarian User", "lib@test.com", "0123", "librarian")
            if user_lib_id:
                # 2. Create linked Librarian
                db_conn.execute("INSERT INTO LIBRARIAN(user_id, staff_id, role) VALUES (?, ?, ?)", (user_lib_id, "S001", "Librarian"))
                print("Created user 'lib' (pass: 123) successfully.")

            # 1. Create User "admin"
            user_admin_id = db_add_user(db_conn, "admin", "123", "Power Admin", "admin@test.com", "999", "admin")
            if user_admin_id:
                # 2. Admin must also have a Librarian record (due to inheritance)
                db_conn.execute("INSERT INTO LIBRARIAN(user_id, staff_id, role) VALUES (?, ?, ?)", (user_admin_id, "A001", "Admin"))
                # 3. And an Admin record
                db_conn.execute("INSERT INTO ADMIN(user_id, privileged_level) VALUES (?, ?)", (user_admin_id, "Full"))
                print("Created user 'admin' (pass: 123) successfully.")
            
            db_conn.commit()
        except Exception as e:
            print(f"Could not add test users (may already exist): {e}")
        
        db_conn.close()
        print("Database connection closed.")