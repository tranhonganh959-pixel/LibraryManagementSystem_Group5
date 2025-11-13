import src.database as db  # Gọi file database.py
import src.models as models # Gọi file models.py
from datetime import date, timedelta

# --- Logic Xác thực & Người dùng ---

def controller_login(username, password):
    """
    Xử lý logic đăng nhập.
    Trả về một đối tượng (User, Librarian,...) nếu thành công,
    hoặc None nếu thất bại.
    """
    # 1. Mở kết nối
    conn = db.connect_db()
    if conn is None:
        return None
        
    try:
        # 2. Gọi hàm từ database.py
        user_data = db.db_get_user_by_username(conn, username)
        
        if user_data is None:
            print("Lỗi: Tên đăng nhập không tồn tại.")
            return None
        
        # 3. Chuyển dữ liệu thô (tuple) thành một đối tượng
        # user_data[0] = user_id, [1] = username, [2] = password,...
        db_user_id, db_username, db_password, db_name, db_email, db_phone, db_user_type = user_data
        
        # 4. Kiểm tra mật khẩu
        if password == db_password:
            print(f"Đăng nhập thành công! Chào mừng {db_name}")
            
            # 5. Tạo đối tượng Model tương ứng
            if db_user_type == 'reader':
                # (Tạm thời tạo đối tượng Reader cơ bản, cần thêm hàm để lấy reader_id)
                user_obj = models.Reader(db_user_id, db_username, db_name, db_email, password, reader_id=db_user_id) 
            elif db_user_type == 'librarian':
                # (Tạm thời tạo đối tượng Librarian cơ bản, cần thêm hàm để lấy staff_id)
                user_obj = models.Librarian(db_user_id, db_username, db_name, db_email, password, staff_id="TBD", role="Librarian") 
            else: 
                user_obj = models.User(db_user_id, db_username, db_name, db_email, password)
                
            return user_obj
        else:
            print("Lỗi: Sai mật khẩu.")
            return None
            
    finally:
        # 6. Đóng kết nối
        conn.close()


def controller_register_reader(username, password, name, email, phone):
    """
    Xử lý logic đăng ký bạn đọc mới.
    """
    conn = db.connect_db()
    if conn is None:
        return None
        
    try:
        # 1. Gọi hàm từ database.py để tạo User trước
        user_id = db.db_add_user(conn, username, password, name, email, phone, 'reader')
        
        if user_id is None:
            return None # Lỗi đã được in từ database.py
            
        # 2. Dùng user_id đó để tạo Reader
        membership_date = date.today().isoformat() # Lấy ngày hôm nay
        reader_id = db.db_add_reader(conn, user_id, membership_date)
        
        if reader_id:
            print(f"Đăng ký bạn đọc '{name}' thành công!")
            return reader_id
        else:
            print("Đăng ký bạn đọc thất bại ở bước tạo Reader.")
return None
            
    finally:
        conn.close()

# --- Logic Nghiệp vụ Sách ---

def controller_add_new_book(title, author, genre):
    """
    Xử lý logic thêm sách mới.
    """
    conn = db.connect_db()
    if conn is None:
        return False
        
    try:
        book_id = db.db_add_book(conn, title, author, genre, 'available')
        if book_id:
            print(f"Đã thêm sách '{title}' (ID: {book_id}) vào hệ thống.")
            return True
        else:
            print("Thêm sách thất bại.")
            return False
    finally:
        conn.close()

def controller_search_book(keyword):
    """
    Xử lý logic tìm kiếm sách.
    Trả về một danh sách các đối tượng Book.
    """
    conn = db.connect_db()
    if conn is None:
        return [] # Trả về danh sách rỗng
        
    try:
        results = db.db_search_books(conn, keyword)
        
        book_list = []
        for row in results:
            # Chuyển từng hàng dữ liệu thô (tuple) thành đối tượng Book
            book_obj = models.Book(book_id=row[0], title=row[1], author=row[2], genre=row[3], status=row[4])
            book_list.append(book_obj)
            
        return book_list
    finally:
        conn.close()

# --- Logic Nghiệp vụ Mượn/Trả ---

def controller_borrow_book(reader_id, book_id):
    """
    Xử lý logic mượn sách.
    """
    conn = db.connect_db()
    if conn is None:
        return False

    try:
        # 1. Kiểm tra trạng thái sách
        book_data = db.db_get_book_by_id(conn, book_id)
        if book_data is None:
            print(f"Lỗi: Không tìm thấy sách với ID {book_id}.")
            return False
            
        book_status = book_data[4] # status là cột thứ 5 (index 4)
        
        if book_status == 'borrowed':
            print(f"Lỗi: Sách '{book_data[1]}' hiện đang được mượn.")
            return False
        
        # 2. Sách có sẵn, tiến hành cho mượn
        # Đổi trạng thái sách
        success_update = db.db_update_book_status(conn, book_id, 'borrowed')
        
        if not success_update:
            print("Lỗi: Không thể cập nhật trạng thái sách.")
            return False
            
        # 3. Tạo bản ghi mượn
        borrow_date = date.today()
        due_date = borrow_date + timedelta(days=14) # Cho mượn 14 ngày
        
        record_id = db.db_create_borrow_record(conn, book_id, reader_id, 
                                               borrow_date.isoformat(), 
                                               due_date.isoformat())
        
        if record_id:
            print(f"Bạn đọc {reader_id} đã mượn thành công sách {book_id}.")
            return True
        else:
            print("Lỗi: Không thể tạo bản ghi mượn.")
            return False
            
    finally:
        conn.close()