from datetime import date
from typing import List

# --- Ghi chú quan trọng ---
# File models.py định nghĩa "dữ liệu" trông như thế nào.
class Book:
    """
    Đại diện cho một cuốn sách trong thư viện.
    """
    def __init__(self, book_id: int, title: str, author: str, genre: str, status: str = 'available'):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.status = status  # 'available' or 'borrowed'

    def update_status(self, new_status: str):
        """Cập nhật trạng thái của sách (available/borrowed)"""
        # Logic thực tế sẽ nằm trong controller
        self.status = new_status
        print(f"Trạng thái sách {self.book_id} đã cập nhật thành {self.status}")

    def get_details(self) -> str:
        """Trả về chuỗi thông tin chi tiết của sách"""
        return f"ID: {self.book_id}, Title: {self.title}, Author: {self.author}, Status: {self.status}"

    def get_status(self) -> str:
        """Trả về trạng thái hiện tại của sách"""
        return self.status

    def get_book_id(self) -> int:
        return self.book_id

    def is_available(self) -> bool:
        """Kiểm tra xem sách có sẵn để mượn không"""
        return self.status == 'available'

class User:
    """
    Lớp cơ sở (base class) cho tất cả người dùng hệ thống.
    """
    def __init__(self, user_id: int, username: str, name: str, contact_info: str, password: str):
        self.user_id = user_id
        self.username = username
        self.name = name
        self.contact_info = contact_info  
        self.password = password  

    def login(self):
        """Logic đăng nhập (Sẽ nằm trong controller)"""
        print(f"Người dùng {self.username} đang đăng nhập...")
        pass

    def logout(self):
        """Logic đăng xuất (Sẽ nằm trong controller)"""
        print(f"Người dùng {self.username} đã đăng xuất.")
        pass

class BorrowingRecord:
    """
    Đại diện cho một bản ghi mượn/trả sách.
    """
    def __init__(self, record_id: int, book_id: int, reader_id: int, borrow_date: date, due_date: date):
        self.record_id = record_id
        self.book_id = book_id
        self.reader_id = reader_id
        self.borrow_date = borrow_date
        self.due_date = due_date
        self.return_date: date = None  # Sẽ được cập nhật khi sách được trả
        self.fine_amount: float = 0.0

    def calculate_fine(self) -> float:
        """Tính phí phạt nếu trả sách muộn (Logic sẽ nằm trong controller)"""
        if self.return_date and self.return_date > self.due_date:
            days_overdue = (self.return_date - self.due_date).days
            # Giả sử phí phạt là 1000 VNĐ/ngày
            self.fine_amount = days_overdue * 1000
        
        return self.fine_amount

class Reader(User):
    """
    Lớp đại diện cho Bạn đọc, kế thừa từ User.
    """
    def __init__(self, user_id: int, username: str, name: str, contact_info: str, password: str, reader_id: int):
        # Gọi constructor của lớp cha (User)
        super().__init__(user_id, username, name, contact_info, password)
        self.reader_id = reader_id
        self.borrowing_history: List[BorrowingRecord] = [] # Sẽ được tải từ CSDL

    def view_borrowing_history(self):
        """Hiển thị lịch sử mượn sách (Logic sẽ nằm trong controller)"""
        print(f"Lịch sử mượn sách của bạn đọc {self.name}:")
        if not self.borrowing_history:
            print("Chưa mượn cuốn nào.")
            return
        
        for record in self.borrowing_history:
            print(f"  - Record {record.record_id}: Mượn sách {record.book_id} ngày {record.borrow_date}")

class Librarian(User):
    """
    Lớp đại diện cho Thủ thư, kế thừa từ User.
    """
    def __init__(self, user_id: int, username: str, name: str, contact_info: str, password: str, staff_id: str, role: str):
        super().__init__(user_id, username, name, contact_info, password)
        self.staff_id = staff_id
        self.role = role

    # --- Các phương thức này sẽ được triển khai logic trong 'controller.py' ---
    
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
    Lớp đại diện cho Admin, kế thừa từ Librarian.
    """
    def __init__(self, user_id: int, username: str, name: str, contact_info: str, password: str, 
                 staff_id: str, role: str, admin_id: int, privilege_level: str):
        super().__init__(user_id, username, name, contact_info, password, staff_id, role)
        self.admin_id = admin_id
        self.privilege_level = privilege_level

    # --- Các phương thức này sẽ được triển khai logic trong 'controller.py' ---
    
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