from datetime import date
from typing import List

# --- Important Note ---
# The models.py file defines what the "data" looks like.
class Book:
    """
    Represents a book in the library.
    """
    def __init__(self, book_id: int, title: str, author: str, genre: str, status: str = 'available'):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.status = status  # 'available' or 'borrowed'

    def update_status(self, new_status: str):
        """Updates the book's status (available/borrowed)"""
        # Actual logic will be in the controller
        self.status = new_status
        print(f"Book {self.book_id} status updated to {self.status}")

    def get_details(self) -> str:
        """Returns a detailed info string for the book"""
        return f"ID: {self.book_id}, Title: {self.title}, Author: {self.author}, Status: {self.status}"

    def get_status(self) -> str:
        """Returns the current status of the book"""
        return self.status

    def get_book_id(self) -> int:
        return self.book_id

    def is_available(self) -> bool:
        """Checks if the book is available for borrowing"""
        return self.status == 'available'

class User:
    """
    Base class for all system users.
    """
    def __init__(self, user_id: int, username: str, name: str, contact_info: str, password: str):
        self.user_id = user_id
        self.username = username
        self.name = name
        self.contact_info = contact_info  
        self.password = password  

    def login(self):
        """Login logic (Will be in the controller)"""
        print(f"User {self.username} is logging in...")
        pass

    def logout(self):
        """Logout logic (Will be in the controller)"""
        print(f"User {self.username} has logged out.")
        pass

class BorrowingRecord:
    """
    Represents a book borrowing/returning record.
    """
    def __init__(self, record_id: int, book_id: int, reader_id: int, borrow_date: date, due_date: date):
        self.record_id = record_id
        self.book_id = book_id
        self.reader_id = reader_id
        self.borrow_date = borrow_date
        self.due_date = due_date
        self.return_date: date = None  # Will be updated when the book is returned
        self.fine_amount: float = 0.0

    def calculate_fine(self) -> float:
        """Calculates the fine if the book is returned late (Logic will be in the controller)"""
        if self.return_date and self.return_date > self.due_date:
            days_overdue = (self.return_date - self.due_date).days
            # Assuming the fine is 1000 VND/day
            self.fine_amount = days_overdue * 1000
        
        return self.fine_amount

class Reader(User):
    """
    Class representing a Reader, inherits from User.
    """
    def __init__(self, user_id: int, username: str, name: str, contact_info: str, password: str, reader_id: int):
        # Call the constructor of the parent class (User)
        super().__init__(user_id, username, name, contact_info, password)
        self.reader_id = reader_id
        self.borrowing_history: List[BorrowingRecord] = [] # Will be loaded from DB

    def view_borrowing_history(self):
        """Displays borrowing history (Logic will be in the controller)"""
        print(f"Borrowing history for reader {self.name}:")
        if not self.borrowing_history:
            print("No books borrowed yet.")
            return
        
        for record in self.borrowing_history:
            print(f"  - Record {record.record_id}: Borrowed book {record.book_id} on {record.borrow_date}")

class Librarian(User):
    """
    Class representing a Librarian, inherits from User.
    """
    def __init__(self, user_id: int, username: str, name: str, contact_info: str, password: str, staff_id: str, role: str):
        super().__init__(user_id, username, name, contact_info, password)
        self.staff_id = staff_id
        self.role = role

    # --- These methods will have their logic implemented in 'controller.py' ---
    
    def add_book(self):
        pass

    def update_book(self):
        pass

    def remove_book(self):
        pass

    def register_reader(self):
        pass

    def update_reader(self):
        pass

    def disable_reader_account(self):
        pass

    def issue_book(self):
        pass

    def receive_return_book(self):
        pass

    def generate_report(self):
        pass

    def search(self):
        pass

    def validate_delete(self):
        pass

class Admin(Librarian):
    """
    Class representing an Admin, inherits from Librarian.
    """
    def __init__(self, user_id: int, username: str, name: str, contact_info: str, password: str, 
                 staff_id: str, role: str, admin_id: int, privilege_level: str):
        super().__init__(user_id, username, name, contact_info, password, staff_id, role)
        self.admin_id = admin_id
        self.privilege_level = privilege_level

    # --- These methods will have their logic implemented in 'controller.py' ---
    
    def create_staff_account(self):
        pass

    def update_staff_account(self):
        pass

    def remove_staff_account(self):
        pass

    def assign_role(self):
        pass

    def view_system_report(self):
        pass