
import database as db  
import models as models 


from datetime import date, timedelta



def controller_login(username, password):

    
    conn = db.connect_db()
    if conn is None:
        return None

    try:
        
        user_data = db.db_get_user_by_username(conn, username)

        if user_data is None:
            print("Lỗi: Tên đăng nhập không tồn tại.")
            return None

       
        db_user_id, db_username, db_password, db_name, db_email, db_phone, db_user_type = user_data

        
        if password == db_password:
            print(f"Đăng nhập thành công! Chào mừng {db_name} (Role: {db_user_type})")

            
            user_obj = None
            
            if db_user_type == 'reader':
                reader_details = db.db_get_reader_by_user_id(conn, db_user_id)
                if reader_details:
                    actual_reader_id = reader_details[0] 
                    user_obj = models.Reader(db_user_id, db_username, db_name, db_email, password, 
                                            reader_id=actual_reader_id)
                else:
                    print(f"Lỗi dữ liệu: User {username} là 'reader' nhưng không tìm thấy bản ghi READER.")
            
            elif db_user_type == 'librarian':
                librarian_details = db.db_get_librarian_by_user_id(conn, db_user_id)
                if librarian_details:
                    actual_staff_id = librarian_details[1] 
                    actual_role = librarian_details[2]     
                    user_obj = models.Librarian(db_user_id, db_username, db_name, db_email, password, 
                                                staff_id=actual_staff_id, role=actual_role)
                else:
                    print(f"Lỗi dữ liệu: User {username} là 'librarian' nhưng không tìm thấy bản ghi LIBRARIAN.")
            
            elif db_user_type == 'admin':
               
                librarian_details = db.db_get_librarian_by_user_id(conn, db_user_id)
                admin_details = db.db_get_admin_by_user_id(conn, db_user_id)
                
                if librarian_details and admin_details:
                    staff_id = librarian_details[1]
                    role = librarian_details[2]
                    admin_id = admin_details[0]
                    privilege_level = admin_details[1]
                    
                    user_obj = models.Admin(db_user_id, db_username, db_name, db_email, password, 
                                            staff_id=staff_id, role=role, 
                                            admin_id=admin_id, privilege_level=privilege_level)
                else:
                    print(f"Lỗi dữ liệu: User {username} là 'admin' nhưng thiếu bản ghi LIBRARIAN hoặc ADMIN.")

            else: 
                
                user_obj = models.User(db_user_id, db_username, db_name, db_email, password)

            return user_obj
        
        else:
            print("Lỗi: Sai mật khẩu.")
            return None

    finally:
      
        conn.close()


def controller_register_reader(username, password, name, email, phone):
    """
    Xử lý logic đăng ký bạn đọc mới.
    """
    conn = db.connect_db()
    if conn is None:
        return None

    try:
        user_id = db.db_add_user(conn, username, password, name, email, phone, 'reader')

        if user_id is None:
            return None 

        membership_date = date.today().isoformat() 
        reader_id = db.db_add_reader(conn, user_id, membership_date)

        if reader_id:
            print(f"Đăng ký bạn đọc '{name}' thành công!")
            return reader_id
        else:
            print("Đăng ký bạn đọc thất bại ở bước tạo Reader.")
            return None

    finally:
        conn.close()



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
        return [] 

    try:
        results = db.db_search_books(conn, keyword)

        book_list = []
        for row in results:
           
            book_obj = models.Book(book_id=row[0], title=row[1], author=row[2], genre=row[3], status=row[4])
            book_list.append(book_obj)

        return book_list
    finally:
        conn.close()



def controller_borrow_book(reader_id, book_id):
    """
    Xử lý logic mượn sách.
    """
    conn = db.connect_db()
    if conn is None:
        return False

    try:

        book_data = db.db_get_book_by_id(conn, book_id)
        if book_data is None:
            print(f"Lỗi: Không tìm thấy sách với ID {book_id}.")
            return False

        book_status = book_data[4] 
        if book_status == 'borrowed':
            print(f"Lỗi: Sách '{book_data[1]}' hiện đang được mượn.")
            return False


        success_update = db.db_update_book_status(conn, book_id, 'borrowed')

        if not success_update:
            print("Lỗi: Không thể cập nhật trạng thái sách.")
            return False


        borrow_date = date.today()
        due_date = borrow_date + timedelta(days=14) 

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