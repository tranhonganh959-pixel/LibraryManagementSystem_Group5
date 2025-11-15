import sqlite3
from sqlite3 import Error
import os # <-- Thêm thư viện 'os'

# --- SỬA LỖI PATH ---
# Lấy đường dẫn tuyệt đối của thư mục chứa file này (tức là thư mục 'src')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Tạo đường dẫn tới file CSDL (nằm trong thư mục 'src')
DATABASE_NAME = os.path.join(BASE_DIR, "library.db")
# ---------------------

def connect_db():
    """ Tạo kết nối tới CSDL SQLite """
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        # Bật hỗ trợ Foreign Key (rất quan trọng)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
    except Error as e:
        print(f"Lỗi khi kết nối tới CSDL: {e}")
    
    return conn

def create_tables(conn):
    """ Tạo các bảng trong CSDL dựa trên thiết kế """
    if conn is None:
        print("Lỗi! Không có kết nối CSDL.")
        return

    # 1. Bảng User (Bảng trung tâm)
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

    # 2. Bảng Books
    sql_create_books_table = """
    CREATE TABLE IF NOT EXISTS books (
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT,
        genre TEXT,
        status TEXT NOT NULL DEFAULT 'available' CHECK(status IN ('available', 'borrowed'))
    );
    """

    # 3. Bảng Reader (Kế thừa từ User)
    sql_create_reader_table = """
    CREATE TABLE IF NOT EXISTS READER (
        reader_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL UNIQUE,
        membership_date TEXT,
        total_borrowed INTEGER DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES User (user_id) ON DELETE CASCADE
    );
    """

    # 4. Bảng Librarian (Kế thừa từ User)
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

    # 5. Bảng Admin (Kế thừa từ User)
    # Ghi chú: Theo models.py, Admin kế thừa Librarian,
    # Cần đảm bảo khi tạo Admin, họ CÓ MỘT BẢN GHI ở LIBRARIAN
    sql_create_admin_table = """
    CREATE TABLE IF NOT EXISTS ADMIN (
        admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL UNIQUE,
        privileged_level TEXT,
        FOREIGN KEY (user_id) REFERENCES User (user_id) ON DELETE CASCADE
    );
    """

    # 6. Bảng Borrowing Record (Bảng ghi mượn sách)
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
        
        print("Tạo bảng thành công (hoặc bảng đã tồn tại).")
    except Error as e:
        print(f"Lỗi khi tạo bảng: {e}")

# ===============================================
# ===== CÁC HÀM CRUD (THÊM, SỬA, XÓA, LẤY) =====
# ===============================================

def db_add_user(conn, username, password, name, email, phone, user_type):
    """Thêm một user mới và trả về user_id"""
    sql = ''' INSERT INTO User(username, password, name, email, phone, user_type)
              VALUES(?,?,?,?,?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (username, password, name, email, phone, user_type))
        conn.commit()
        return cur.lastrowid # Trả về ID của user vừa tạo
    except sqlite3.IntegrityError as e:
        print(f"Lỗi: Username '{username}' hoặc Email '{email}' đã tồn tại. {e}")
        return None
    except Error as e:
        print(f"Lỗi khi thêm user: {e}")
        return None

def db_add_reader(conn, user_id, membership_date):
    """Thêm một reader mới (liên kết với user_id)"""
    sql = ''' INSERT INTO READER(user_id, membership_date) VALUES(?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (user_id, membership_date))
        conn.commit()
        return cur.lastrowid
    except Error as e:
        print(f"Lỗi khi thêm reader: {e}")
        return None

def db_get_user_by_username(conn, username):
    """Lấy thông tin user bằng username"""
    sql = "SELECT * FROM User WHERE username = ?"
    cur = conn.cursor()
    cur.execute(sql, (username,))
    # fetchone() trả về một hàng (row) dưới dạng tuple
    return cur.fetchone()

# --- HÀM MỚI 1 ---
def db_get_reader_by_user_id(conn, user_id):
    """Lấy chi tiết Reader bằng user_id"""
    sql = "SELECT reader_id, membership_date, total_borrowed FROM READER WHERE user_id = ?"
    cur = conn.cursor()
    cur.execute(sql, (user_id,))
    return cur.fetchone()

# --- HÀM MỚI 2 ---
def db_get_librarian_by_user_id(conn, user_id):
    """Lấy chi tiết Librarian bằng user_id"""
    sql = "SELECT librarian_id, staff_id, role, hire_date FROM LIBRARIAN WHERE user_id = ?"
    cur = conn.cursor()
    cur.execute(sql, (user_id,))
    return cur.fetchone()

# --- HÀM MỚI 3 ---
def db_get_admin_by_user_id(conn, user_id):
    """Lấy chi tiết Admin bằng user_id"""
    sql = "SELECT admin_id, privileged_level FROM ADMIN WHERE user_id = ?"
    cur = conn.cursor()
    cur.execute(sql, (user_id,))
    return cur.fetchone()

def db_add_book(conn, title, author, genre, status='available'):
    """Thêm một cuốn sách mới"""
    sql = ''' INSERT INTO books(title, author, genre, status)
              VALUES(?,?,?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (title, author, genre, status))
        conn.commit()
        return cur.lastrowid
    except Error as e:
        print(f"Lỗi khi thêm sách: {e}")
        return None

def db_get_book_by_id(conn, book_id):
    """Lấy thông tin sách bằng ID"""
    sql = "SELECT * FROM books WHERE book_id = ?"
    cur = conn.cursor()
    cur.execute(sql, (book_id,))
    return cur.fetchone()

def db_update_book_status(conn, book_id, new_status):
    """Cập nhật trạng thái của sách (available/borrowed)"""
    sql = "UPDATE books SET status = ? WHERE book_id = ?"
    try:
        cur = conn.cursor()
        cur.execute(sql, (new_status, book_id))
        conn.commit()
        return True
    except Error as e:
        print(f"Lỗi khi cập nhật trạng thái sách: {e}")
        return False

def db_create_borrow_record(conn, book_id, reader_id, borrow_date, due_date):
    """Tạo một bản ghi mượn sách mới"""
    sql = ''' INSERT INTO BORROWING_RECORD(book_id, reader_id, borrow_date, due_date, fine_amount)
              VALUES(?,?,?,?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (book_id, reader_id, borrow_date, due_date, 0))
        conn.commit()
        return cur.lastrowid
    except Error as e:
        print(f"Lỗi khi tạo bản ghi mượn: {e}")
        return None

def db_update_return_record(conn, record_id, return_date, fine_amount):
    """Cập nhật bản ghi khi trả sách"""
    sql = "UPDATE BORROWING_RECORD SET return_date = ?, fine_amount = ? WHERE record_id = ?"
    try:
        cur = conn.cursor()
        cur.execute(sql, (return_date, fine_amount, record_id))
        conn.commit()
        return True
    except Error as e:
        print(f"Lỗi khi cập nhật trả sách: {e}")
        return False

def db_search_books(conn, keyword):
    """Tìm sách theo tiêu đề hoặc tác giả"""
    sql = "SELECT * FROM books WHERE title LIKE ? OR author LIKE ?"
    cur = conn.cursor()
    keyword_like = f"%{keyword}%" # Thêm dấu % để tìm kiếm
    cur.execute(sql, (keyword_like, keyword_like))
    return cur.fetchall() # fetchall() trả về một danh sách các hàng

# --- SỬA LỖI NAME ERROR ---
# Di chuyển khối này xuống CUỐI CÙNG của file
if __name__ == '__main__':
    # Đoạn code này chỉ chạy khi bạn thực thi file database.py trực tiếp
    # bằng lệnh: python src/database.py
    
    print("Khởi tạo cơ sở dữ liệu...")
    db_conn = connect_db()
    
    if db_conn is not None:
        create_tables(db_conn)
        
        # --- THÊM 1 ADMIN/LIBRARIAN ĐỂ TEST ---
        try:
            print("Đang thử thêm user test 'admin' và 'lib'...")
            # 1. Tạo User "lib"
            user_lib_id = db_add_user(db_conn, "lib", "123", "Thủ Thư", "lib@test.com", "0123", "librarian")
            if user_lib_id:
                # 2. Tạo Librarian liên kết
                db_conn.execute("INSERT INTO LIBRARIAN(user_id, staff_id, role) VALUES (?, ?, ?)", (user_lib_id, "S001", "Librarian"))
                print("Tạo user 'lib' (pass: 123) thành công.")

            # 1. Tạo User "admin"
            user_admin_id = db_add_user(db_conn, "admin", "123", "Admin Quyền Lực", "admin@test.com", "999", "admin")
            if user_admin_id:
                # 2. Admin phải có cả bản ghi Librarian (vì kế thừa)
                db_conn.execute("INSERT INTO LIBRARIAN(user_id, staff_id, role) VALUES (?, ?, ?)", (user_admin_id, "A001", "Admin"))
                # 3. Và bản ghi Admin
                db_conn.execute("INSERT INTO ADMIN(user_id, privileged_level) VALUES (?, ?)", (user_admin_id, "Full"))
                print("Tạo user 'admin' (pass: 123) thành công.")
            
            db_conn.commit()
        except Exception as e:
            print(f"Không thể thêm user test (có thể đã tồn tại): {e}")
        
        db_conn.close()
        print("Đóng kết nối CSDL.")