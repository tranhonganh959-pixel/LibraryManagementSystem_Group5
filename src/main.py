import controller as controller
import database as database
import models as models 

def book_management_menu():
    """Menu con Quản lý Sách"""
    while True:
        print("\n--- 1. Book Management ---")
        print("1. Add new book")
        print("2. Update book information")
        print("3. Delete book")
        print("4. View list of all books")
        print("5. Back to Librarian Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            print("--- Add New Book ---")
            title = input("Enter title: ")
            author = input("Enter author: ")
            genre = input("Enter genre: ")
            controller.controller_add_new_book(title, author, genre)
            print("Press Enter to continue...")
            input()
        
        elif choice == '2':
            print("--- Update Book (Not implemented) ---")
            
            
        elif choice == '3':
            print("--- Delete Book (Not implemented) ---")
           
        
      
        elif choice == '4': 
            print("--- View All Books (Not implemented) ---")
            
            
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

def reader_management_menu():
    """Menu con Quản lý Bạn đọc"""
    while True:
        print("\n--- 2. Reader Management ---")
        print("1. Register new reader")
        print("2. Update reader details")
        print("3. Delete reader profile")
        print("4. View list of all readers")
        print("5. Back to Librarian Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            print("--- Register New Reader ---")
            username = input("Enter new username: ")
            password = input("Enter new password: ")
            name = input("Enter reader's full name: ")
            email = input("Enter reader's email: ")
            phone = input("Enter reader's phone: ")
            controller.controller_register_reader(username, password, name, email, phone)
            print("Press Enter to continue...")
            input()

        
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

def borrow_return_menu():
    """Menu con Quản lý Mượn/Trả"""
    
    while True:
        print("\n--- 3. Borrow/Return Management ---")
        print("1. Record new borrow transaction")
        print("2. Process book return")
        print("3. Back to Librarian Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            print("--- Borrow Book ---")
            try:
                reader_id = int(input("Enter Reader ID: "))
                book_id = int(input("Enter Book ID: "))
                controller.controller_borrow_book(reader_id, book_id)
            except ValueError:
                print("Error: ID must be a number.")
            print("Press Enter to continue...")
            input()
            
       
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

def search_statistics_menu():
    """Menu con Tìm kiếm & Thống kê"""
    while True:
        print("\n--- 4. Search & Statistics ---")
        print("1. Search for books (by keyword)")
        print("2. View statistics")
        print("3. Back to Librarian Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            print("--- Search Books ---")
            keyword = input("Enter title or author keyword: ")
            results = controller.controller_search_book(keyword)
            
            if not results:
                print(f"No books found matching '{keyword}'.")
            else:
                print(f"Found {len(results)} book(s):")
                for book in results:
                    
                    print(f"  - {book.get_details()}")
            print("Press Enter to continue...")
            input()

        
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")



def librarian_menu(librarian_user):
    """Menu chính cho Thủ thư sau khi đăng nhập thành công"""
   
    role_name = "Admin" if isinstance(librarian_user, models.Admin) else "Librarian"
    print(f"\n--- Welcome, {role_name} {librarian_user.name}! (Staff ID: {librarian_user.staff_id}) ---")
    
    while True:
        print("\n--- Librarian Main Menu ---")
        print("1. Book Management")
        print("2. Reader Management")
        print("3. Borrow/Return Management")
        print("4. Search & Statistics")
        print("5. Logout")
        choice = input("Enter your choice: ")

        if choice == '1':
            book_management_menu()
        elif choice == '2':
            reader_management_menu()
        elif choice == '3':
            borrow_return_menu()
        elif choice == '4':
            search_statistics_menu()
        elif choice == '5':
            print(f"Logging out user {librarian_user.username}...")
            break 
        else:
            print("Invalid choice. Please try again.")

def login_screen():
    """Màn hình Đăng nhập"""
    print("\n--- LOGIN SCREEN ---")
    username = input("Enter username: ")
    password = input("Enter password: ")
   
    user = controller.controller_login(username, password)
    
    if user:
        if isinstance(user, models.Librarian):
            librarian_menu(user) 
        elif isinstance(user, models.Reader):
            print(f"Login successful! (Reader menu not implemented). Welcome {user.name}!")
        else:
            print(f"Login successful! (User role '{type(user)}' has no menu).")
    else:
       
        print("Login failed. Invalid username or password.")
        print("Press Enter to continue...")
        input()



def main_menu():
    """Menu chính của chương trình khi bắt đầu"""
    while True:
        print("\n==========================================")
        print("   WELCOME TO LIBRARY MANAGEMENT SYSTEM   ")
        print("==========================================")
        print("--- Main Menu ---")
        print("1. Log In")
        print("2. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            login_screen()
        elif choice == '2':
            print("Goodbye! Thank you for using the system.")
            break
        else:
            print("Invalid choice. Please select 1 or 2.")

def initialize_database():
    """
    Hàm này đảm bảo CSDL và các bảng được tạo
    trước khi chương trình chính chạy.
    """
    print("Initializing database...")
    conn = database.connect_db()
    if conn:
        database.create_tables(conn)
        conn.close()
        print("Database is ready.")
    else:
        print("FATAL ERROR: Could not connect to database.")
        exit()

    initialize_database() 
    main_menu() 