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

def controller_borrow_book(reader_id, book_id):
    """
    Handles logic for borrowing a book.
    """
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
