# LibraryManagementSystem_Group5
Đồ án môn học Công Nghệ Phần Mềm - Hệ thống Quản lý Thư viện - Nhóm 5
-- Library Management System --
This is a term project for the Programming and Testing (ProgAndTest) course, simulating a basic library management system as a console application written in Python.

----- Main Features
User Management:
Allows new Readers to register for an account.
Handles login for all roles: Admin, Librarian, and Reader.

Librarian/Admin Menu:
Book Management: Add new books.
Reader Management: Register new readers (Admin action).
Borrow/Return Management: Record a new borrow transaction.
Search: Find books by keyword.

Reader Menu:
Search for books.
View personal profile.
Storage: All data is persisted and managed using SQLite.

----- Tech Stack
Language: Python 3
Database: SQLite 3
Source Code Management: Git & GitHub
Packaging: Docker

----- Project Structure
The project is built following a 3-layer architecture (UI, Logic, Data):

ProgAndTest_GroupXY/
├── docs/
│   └── Library Management System.docx
├── src/
│   ├── main.py         # UI Layer & Main Entry Point
│   ├── controller.py   # Business Logic Layer
│   ├── models.py       # Class Models (Data Structure)
│   ├── database.py     # Data Access Layer
│   └── library.db      # Database file (auto-generated)
├── Dockerfile          # Deployment/Packaging instructions
├── Testing document.xlsx # Test Cases File
├── Evidence_GroupXY.pdf  # Tool Usage Evidence File
└── README.md

----- How to Install and Run
Follow these steps to run the program on your local machine.

Step 1: Clone the Repository

git clone https://github.com/tranhonganh959-pixel/LibraryManagementSystem_Group5.git

Step 2: Navigate to the src Directory
Very Important: All of the following commands must be run from inside the src directory.

cd ProgAndTest_GroupXY/src

Step 3: Initialize the Database
Run the database.py file one time to create the tables and two test accounts.

python database.py
After running, you will see a new library.db file appear inside the src directory.

Step 4: Run the Program
After the database is initialized, you can run the main application:

python main.py

----- Usage (Test Accounts)
The system has pre-built 2 accounts for you to log in and test the Librarian/Admin functions:

Admin Account:
Username: admin
Password: 123

Librarian Account:
Username: lib
Password: 123

You can also use the "2. Register (New Reader)" option on the main menu to create your own reader account.

----- Group [5] Members
[Nguyễn Minh Nhựt] - [079206025133]

[Hoàng Thanh Tùng] - [044206024550]

[Thiều Viết Tuấn Anh] - [038206021383]

[Trần Hồng Anh] - [051206004022]
