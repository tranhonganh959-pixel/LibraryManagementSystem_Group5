import sqlite3
from sqlite3 import Error

DATABASE_NAME = "src/library.db"

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

    # Dùng triple-quotes (''') để viết các câu lệnh SQL dài
    # Dùng CREATE TABLE IF NOT EXISTS để không bị lỗi nếu chạy lại file

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
    
    # Bảng LIBRARY_SYSTEM (từ thiết kế CSDL của bạn)
    # Ghi chú: Bảng này có vẻ lạ, nhưng tôi thêm vào cho khớp thiết kế.
    # Nó có thể dùng để lưu trạng thái của hệ thống.
    sql_create_library_system_table = """
    CREATE TABLE IF NOT EXiSTS LIBRARY_SYSTEM (
        system_id INTEGER PRIMARY KEY,
        current_user_id INTEGER,
        FOREIGN KEY (current_user_id) REFERENCES User (user_id)
    );
    """

    try:
        c = conn.cursor()
        # Thực thi các lệnh tạo bảng
        c.execute(sql_create_user_table)
        c.execute(sql_create_books_table)
        c.execute(sql_create_reader_table)
        c.execute(sql_create_librarian_table)
        c.execute(sql_create_admin_table)
        c.execute(sql_create_borrowing_table)
        c.execute(sql_create_library_system_table)
        
        print("Tạo bảng thành công.")
    except Error as e:
        print(f"Lỗi khi tạo bảng: {e}")

# --- Hàm chính để chạy file này ---
if __name__ == '__main__':
    # Đoạn code này chỉ chạy khi bạn thực thi file database.py trực tiếp
    # bằng lệnh: python src/database.py
    
    print("Khởi tạo cơ sở dữ liệu...")
    
    db_conn = connect_db()
    
    if db_conn is not None:
        create_tables(db_conn)
        db_conn.close()
        print("Đóng kết nối CSDL.")