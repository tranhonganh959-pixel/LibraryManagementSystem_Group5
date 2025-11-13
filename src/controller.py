from datetime import date
from typing import List, Optional
from models import Book, BorrowingRecord, Reader, Librarian, Admin


class LibraryController:
    """
    Main controller for handling all business logic of the Library Management System.
    """
    def __init__(self):
        self.books: List[Book] = []
        self.readers: List[Reader] = []
        self.librarians: List[Librarian] = []
        self.borrow_records: List[BorrowingRecord] = []

    # ========================
    # USER AUTHENTICATION
    # ========================
    def login(self, username: str, password: str, user_list: List[Librarian | Reader | Admin]) -> Optional[object]:
        """Authenticate a user by username and password."""
        for user in user_list:
            if user.username == username and user.password == password:
                print(f"✅ Login successful: {user.username}")
                return user
        print("❌ Invalid username or password.")
        return None

    def logout(self, user):
        """Log out a user."""
        print(f"👋 User {user.username} has logged out.")


    # ========================
    # BOOK MANAGEMENT
    # ========================
    def add_book(self, librarian: Librarian, book: Book):
        """Add a new book to the library (librarian or admin only)."""
        if isinstance(librarian, Librarian):
            self.books.append(book)
            print(f"✅ Book '{book.title}' added successfully!")
        else:
            print("❌ Only librarians or admins can add books.")

    def update_book(self, librarian: Librarian, book_id: int, new_data: dict):
        """Update book information."""
        for b in self.books:
            if b.book_id == book_id:
                b.title = new_data.get('title', b.title)
                b.author = new_data.get('author', b.author)
                b.genre = new_data.get('genre', b.genre)
                b.status = new_data.get('status', b.status)
                print(f"🔄 Book {b.book_id} updated successfully!")
                return
        print("❌ Book not found.")

    def remove_book(self, librarian: Librarian, book_id: int):
        """Remove a book from the system (only if it's not borrowed)."""
        for b in self.books:
            if b.book_id == book_id:
                if b.status == "borrowed":
                    print("❌ Cannot delete a book that is currently borrowed.")
                    return
                self.books.remove(b)
                print(f"🗑️ Book {book_id} has been removed.")
                return
        print("❌ Book not found for deletion.")

    def search_books(self, keyword: str):
        """Search for books by title or author."""
        results = [b for b in self.books if keyword.lower() in b.title.lower() or keyword.lower() in b.author.lower()]
        if results:
            print("🔍 Search results:")
            for b in results:
                print("  ", b.get_details())
        else:
            print("❌ No books found.")


    # ========================
    # READER MANAGEMENT
    # ========================
    def register_reader(self, librarian: Librarian, reader: Reader):
        """Register a new reader account."""
        self.readers.append(reader)
        print(f"✅ Reader '{reader.name}' registered successfully.")

    def update_reader(self, librarian: Librarian, reader_id: int, new_data: dict):
        """Update reader information."""
        for r in self.readers:
            if r.reader_id == reader_id:
                r.name = new_data.get('name', r.name)
                r.contact_info = new_data.get('contact_info', r.contact_info)
                print(f"🔄 Reader '{r.name}' updated successfully!")
                return
        print("❌ Reader not found.")

    def disable_reader_account(self, librarian: Librarian, reader_id: int):
        """Disable a reader account."""
        for r in self.readers:
            if r.reader_id == reader_id:
                self.readers.remove(r)
                print(f"🚫 Reader account {reader_id} has been disabled.")
                return
        print("❌ Reader not found.")


    # ========================
    # BORROWING / RETURNING
    # ========================
    def issue_book(self, librarian: Librarian, reader_id: int, book_id: int, borrow_date: date, due_date: date):
        """Issue a book to a reader."""
        book = next((b for b in self.books if b.book_id == book_id), None)
        reader = next((r for r in self.readers if r.reader_id == reader_id), None)

        if not book or not reader:
            print("❌ Reader or book not found.")
            return

        if not book.is_available():
            print("❌ Book is not available for borrowing.")
            return

        record = BorrowingRecord(len(self.borrow_records) + 1, book_id, reader_id, borrow_date, due_date)
        self.borrow_records.append(record)
        reader.borrowing_history.append(record)
        book.update_status("borrowed")
        print(f"📚 Reader '{reader.name}' borrowed '{book.title}' successfully.")

    def return_book(self, librarian: Librarian, record_id: int, return_date: date):
        """Process book returning."""
        for record in self.borrow_records:
            if record.record_id == record_id:
                record.return_date = return_date
                fine = record.calculate_fine()
                book = next((b for b in self.books if b.book_id == record.book_id), None)
                if book:
                    book.update_status("available")
                if fine > 0:
                    print(f"⚠️ Book returned late. Fine: {fine} VND.")
                else:
                    print("✅ Book returned on time.")
                return
        print("❌ Borrow record not found.")


    # ========================
    # REPORTS & STATISTICS
    # ========================
    def generate_statistics(self):
        """Generate summary statistics."""
        total_books = len(self.books)
        borrowed_books = len([b for b in self.books if b.status == 'borrowed'])
        total_readers = len(self.readers)
        print("📊 Library Statistics:")
        print(f"   Total books: {total_books}")
        print(f"   Borrowed books: {borrowed_books}")
        print(f"   Total readers: {total_readers}")
