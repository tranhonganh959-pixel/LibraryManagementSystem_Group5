
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
            print("Error: Username does not exist.")
            return None

        
        db_user_id, db_username, db_password, db_name, db_email, db_phone, db_user_type = user_data

        
        if password == db_password:
            print(f"Login successful! Welcome {db_name} (Role: {db_user_type})")

            
            user_obj = None
            
            if db_user_type == 'reader':
                reader_details = db.db_get_reader_by_user_id(conn, db_user_id)
                if reader_details:
                    actual_reader_id = reader_details[0] 
                    user_obj = models.Reader(db_user_id, db_username, db_name, db_email, password, 
                                            reader_id=actual_reader_id)
                else:
                    print(f"Data Error: User {username} is 'reader' but no READER record found.")
            
            elif db_user_type == 'librarian':
                librarian_details = db.db_get_librarian_by_user_id(conn, db_user_id)
                if librarian_details:
                    actual_staff_id = librarian_details[1] 
                    actual_role = librarian_details[2]     
                    user_obj = models.Librarian(db_user_id, db_username, db_name, db_email, password, 
                                                staff_id=actual_staff_id, role=actual_role)
                else:
                    print(f"Data Error: User {username} is 'librarian' but no LIBRARIAN record found.")
            
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
                    print(f"Data Error: User {username} is 'admin' but missing LIBRARIAN or ADMIN record.")

            else: 
                
                user_obj = models.User(db_user_id, db_username, db_name, db_email, password)

            return user_obj
        
        else:
            print("Error:Incorrect password.")
            return None

    finally:
        
        conn.close()


def controller_register_reader(username, password, name, email, phone):
    """
    Handles logic for registering a new reader.
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
            print(f"Reader '{name}' registered successfully!")
            return reader_id
        else:
            print("Reader registration failed at Reader creation step.")
            return None

    finally:
        conn.close()

def controller_update_reader_info(reader_id, new_name, new_email, new_phone):
    
    conn = db.connect_db()
    if conn is None:
        return False

    try:
        
        user_id = db.db_get_user_id_from_reader_id(conn, reader_id)
        if user_id is None:
            print(f"Error: No user found for reader_id {reader_id}")
            return False
            
        success = db.db_update_user_info(conn, user_id, new_name, new_email, new_phone)
        
        if success:
            print(f"Successfully updated info for reader {reader_id}.")
            return True
        else:
            print(f"Failed to update info for reader {reader_id}.")
            return False
    finally:
        conn.close()

def controller_disable_reader_account(reader_id):
    
    conn = db.connect_db()
    if conn is None:
        return False

    try:
        
        success = db.db_update_reader_status(conn, reader_id, 'disabled')
        
        if success:
            print(f"Successfully disabled account for reader {reader_id}.")
            return True
        else:
            print(f"Failed to disable account for reader {reader_id}.")
            return False
    finally:
        conn.close()

def controller_logout():
    
    print("User logged out. Client should clear session.")
    return True

def controller_add_new_book(title, author, genre):
    
    conn = db.connect_db()
    if conn is None:
        return False

    try:
        book_id = db.db_add_book(conn, title, author, genre, 'available')
        if book_id:
            print(f"Added book '{title}' (ID: {book_id}) to the system.")
            return True
        else:
            print("Failed to add book.")
            return False
    finally:
        conn.close()

def controller_search_book(keyword):
    
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

def controller_get_book_details(book_id):
    
    conn = db.connect_db()
    if conn is None:
        return None

    try:
        book_data = db.db_get_book_by_id(conn, book_id)

        if book_data:
            book_obj = models.Book(book_id=book_data[0], title=book_data[1], 
                                    author=book_data[2], genre=book_data[3], 
                                    status=book_data[4])
            return book_obj
        else:
            print(f"Error: Book with ID {book_id} not found.")
            return None
    finally:
        conn.close()

def controller_update_book(book_id, new_title, new_author, new_genre):
    
    conn = db.connect_db()
    if conn is None:
        return False

    try:
        success = db.db_update_book_info(conn, book_id, new_title, new_author, new_genre)
        
        if success:
            print(f"Successfully updated book {book_id}.")
            return True
        else:
            print(f"Failed to update book {book_id}.")
            return False
    finally:
        conn.close()

def controller_remove_book(book_id):
    
    conn = db.connect_db()
    if conn is None:
        return False

    try:
        
        book_data = db.db_get_book_by_id(conn, book_id)
        if book_data and book_data[4] == 'borrowed': 
            print(f"Error: Cannot remove book {book_id}. It is currently borrowed.")
            return False

        success = db.db_delete_book(conn, book_id)
        
        if success:
            print(f"Successfully removed book {book_id}.")
            return True
        else:
            print(f"Failed to remove book {book_id}.")
            return False
    finally:
        conn.close()

LATE_FEE_PER_DAY = 1.00 

def controller_borrow_book(reader_id, book_id):
    
    conn = db.connect_db()
    if conn is None:
        return False

    try:
        
        book_data = db.db_get_book_by_id(conn, book_id)
        if book_data is None:
            print(f"Error: Book with ID {book_id} not found.")
            return False

        book_status = book_data[4] 

        if book_status == 'borrowed':
            print(f"Error: Book '{book_data[1]}' is currently borrowed.")
            return False

    
        success_update = db.db_update_book_status(conn, book_id, 'borrowed')

        if not success_update:
            print("Error: Could not update book status.")
            return False

        
        borrow_date = date.today()
        due_date = borrow_date + timedelta(days=14) 

        record_id = db.db_create_borrow_record(conn, book_id, reader_id, 
                                               borrow_date.isoformat(), 
                                               due_date.isoformat())

        if record_id:
            print(f"Reader {reader_id} successfully borrowed book {book_id}.")
            return True
        else:
            print("Error: Could not create borrow record.")
            return False

    finally:
        conn.close()

def controller_calculate_late_fee(due_date_str, return_date):
    
    try:
        due_date = date.fromisoformat(due_date_str)
        
        if return_date > due_date:
            days_overdue = (return_date - due_date).days
            fee = days_overdue * LATE_FEE_PER_DAY
            return fee, days_overdue
        else:
            return 0.0, 0 
            
    except Exception as e:
        print(f"Error calculating late fee: {e}")
        return 0.0, 0

def controller_return_book(book_id):
    
    conn = db.connect_db()
    if conn is None:
        return False

    try:
        
        record_data = db.db_get_active_borrow_record_for_book(conn, book_id)
        
        if record_data is None:
            print(f"Error: Book ID {book_id} has no active borrow record. It may already be returned.")
            return False
            
        record_id = record_data[0]
        reader_id = record_data[2]
        due_date_str = record_data[4]
        
        
        today = date.today()
        late_fee, days_overdue = controller_calculate_late_fee(due_date_str, today)
        
        
        success_record = db.db_update_borrow_record_return(conn, record_id, today.isoformat(), late_fee)
        
        if not success_record:
            print("Error: Could not update borrow record.")
            return False
            
        
        success_book = db.db_update_book_status(conn, book_id, 'available')
        
        if not success_book:
            print("Error: Could not update book status, but borrow record was closed.")
            return False 

        
        if late_fee > 0:
            print(f"Book {book_id} returned by reader {reader_id}. LATE ({days_overdue} days). Fee: {late_fee}")
        else:
            print(f"Book {book_id} returned on time by reader {reader_id}.")
            
        return True

    finally:
        conn.close()

def controller_view_borrowing_history(reader_id):
    
    conn = db.connect_db()
    if conn is None:
        return []

    try:
        
        history_data = db.db_get_borrow_history_by_reader(conn, reader_id)
        
        return history_data
        
    finally:
        conn.close()

def controller_create_staff_account(username, password, name, email, phone, role, privilege_level=None):

    conn = db.connect_db()
    if conn is None:
        return None

    try:
        
        user_type = 'admin' if role == 'admin' else 'librarian'
        
        user_id = db.db_add_user(conn, username, password, name, email, phone, user_type)
        if user_id is None:
            return None 

        staff_id = db.db_add_librarian(conn, user_id, role)
        if staff_id is None:
            print("Error: Failed to create Librarian record.")
            
            return None
            
        
        if user_type == 'admin':
            admin_id = db.db_add_admin(conn, user_id, privilege_level)
            if admin_id is None:
                print("Error: Failed to create Admin record.")
            
                return None
        
        print(f"Successfully created staff account '{username}' (Role: {role}).")
        return staff_id

    finally:
        conn.close()

def controller_update_staff_info(staff_id, new_name, new_email, new_phone, new_role):
    
    conn = db.connect_db()
    if conn is None:
        return False
        
    try:
        user_id = db.db_get_user_id_from_staff_id(conn, staff_id)
        if user_id is None:
            print(f"Error: No user found for staff_id {staff_id}")
            return False
        
        success_user = db.db_update_user_info(conn, user_id, new_name, new_email, new_phone)
        

        success_role = db.db_update_librarian_role(conn, staff_id, new_role)
        
        if success_user and success_role:
            print(f"Successfully updated info for staff {staff_id}.")
            return True
        else:
            print(f"Failed to update info for staff {staff_id}.")
            return False
    finally:
        conn.close()

def controller_delete_staff_account(staff_id):
    
    conn = db.connect_db()
    if conn is None:
        return False
        
    try:
        
        user_id = db.db_get_user_id_from_staff_id(conn, staff_id)
        if user_id is None:
            print(f"Error: No user found for staff_id {staff_id}")
            return False
        
        db.db_delete_admin_by_user_id(conn, user_id)
        
        success_lib = db.db_delete_librarian_by_user_id(conn, user_id)
        if not success_lib:
            print("Error: Could not delete librarian record.")
            return False
            

        success_user = db.db_delete_user_by_id(conn, user_id)
        if not success_user:
            print("Error: Could not delete user record.")
            return False
            
        print(f"Successfully deleted staff account {staff_id} (User {user_id}).")
        return True
        
    finally:
        conn.close()

def controller_generate_statistics():
    
    conn = db.connect_db()
    if conn is None:
        return None
        
    try:
        
        total_books = db.db_get_total_books(conn)
        total_readers = db.db_get_total_readers(conn)
        books_on_loan = db.db_get_total_books_on_loan(conn)
        
        stats = {
            "total_books": total_books,
            "total_readers": total_readers,
            "books_available": total_books - books_on_loan,
            "books_on_loan": books_on_loan
        }
        
        return stats
        
    finally:
        conn.close()

