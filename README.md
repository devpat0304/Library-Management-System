# 📚 Library Management System – SQL, Python & GUI Integration

The **Library Management System** is a comprehensive, multi-phase database application engineered to support the full lifecycle of book circulation within a multi-branch library network. This academic project models real-world library logistics through schema design, data management, and user interaction. This project was developed as part of **CSE 3330: Database Systems and File Structures** at **The University of Texas at Arlington** (Fall 2024).

This project was executed across **three development phases**:

- **Phase 1:** ER modeling and relational schema creation
- **Phase 2:** Data loading and query development
- **Phase 3:** Frontend integration via a Python-based Tkinter GUI

The system is centered on managing:

- 📚 **Book and copy availability** across multiple branches
- 👤 **Borrower account management**
- 📖 **Loan and return transactions**
- 💰 **Late fee calculations and record-keeping**

It emphasizes practical experience in:

- 📐 Designing **normalized relational schemas** with primary/foreign key constraints
- 💾 Writing and optimizing **SQL queries** to retrieve and update book/loan data
- 🖥️ Building a **Python GUI (Tkinter)** to interact with the backend database
- 📊 Importing structured datasets for books, authors, borrowers, and branches
- 🧠 Enforcing data integrity and validation in real-time

The user interface allows intuitive operations such as:

> _Searching for books, checking availability by branch, checking out and returning books, and creating borrower accounts — all executed through SQL interactions behind the scenes._

---


## 🗃️ Database Schema Overview

This section outlines the schema design of the Library Management System database, detailing each entity (table), its purpose, and key attributes.

---

### 📚 Book

- **Purpose**: Stores information about each unique book title.
- **Key Attributes**:
  - `Book_ID` (Primary Key): Unique identifier for the book.
  - `Title`: The name of the book.
  - `Publisher_Name`: References the publisher.
- **Relationships**:
  - Linked to `Book_Authors`, `Book_Copies`, and `Book_Loans`.

---

### 👤 Book_Authors

- **Purpose**: Maps books to their authors (supports multiple authors per book).
- **Key Attributes**:
  - `Book_ID` (Foreign Key → Book)
  - `Author_Name`: Name of the author.
- **Primary Key**: Composite → (`Book_ID`, `Author_Name`)

---

### 🏛️ Library_Branch

- **Purpose**: Holds information about individual library branches.
- **Key Attributes**:
  - `Branch_ID` (Primary Key): Unique identifier for each branch.
  - `Branch_Name`: Branch’s name.
  - `Branch_Address`: Physical address.

---

### 📦 Book_Copies

- **Purpose**: Tracks the number of copies of each book available at each library branch.
- **Key Attributes**:
  - `Book_ID` (Foreign Key → Book)
  - `Branch_ID` (Foreign Key → Library_Branch)
  - `No_Of_Copies`: Integer count.
- **Primary Key**: Composite → (`Book_ID`, `Branch_ID`)

---

### 🙋 Borrower

- **Purpose**: Stores information about users who can borrow books.
- **Key Attributes**:
  - `Card_No` (Primary Key): Unique borrower ID.
  - `Name`: Full name.
  - `Address`: Mailing address.
  - `Phone`: Contact number.

---

### 📝 Book_Loans

- **Purpose**: Logs borrowing activity and due/return dates.
- **Key Attributes**:
  - `Book_ID` (Foreign Key → Book)
  - `Branch_ID` (Foreign Key → Library_Branch)
  - `Card_No` (Foreign Key → Borrower)
  - `Date_Out`: Loan start date.
  - `Due_Date`: Expected return date.
  - `Returned_Date`: Actual return date (if applicable).
- **Primary Key**: Composite → (`Book_ID`, `Branch_ID`, `Card_No`)

  ---

## 📁 Project File Descriptions 

This section provides a structured overview of all major files used in the **Library Management System** project. The files are grouped by folder for clarity and each entry includes a short description of its role in the system.

---

### 📦 Folder: `Reports/`

#### `Phase1_Report.pdf`
Describes the **conceptual and ER modeling** of the database, including an Entity-Relationship Diagram and schema justification. This sets the foundation for the database structure.

#### `Phase2_Report.pdf`
Covers the **implementation phase**, including SQL `CREATE TABLE` statements, data population strategies, and initial schema testing.

#### `Phase3_Report.pdf`
Focuses on **application integration** and the **Python GUI**, along with SQL query implementation and testing procedures.

---

### 🧮 File: `Library_Database_SchemaData.sql`
This SQL script includes the schema used to create the **entire database**, including table creation, primary/foreign keys, and constraints. This is the foundation for the database layer.

---

### 🖼️ File: `Library_Management_GUI.py`
A **Tkinter-based Python GUI** application that interacts with the library database. Allows users to:
- View available books
- Loan or return books
- Search for borrowers
- Execute pre-defined queries

---

### 📂 Folder: `Dataset_Spreadsheets/`

These CSV files represent the **initial data** loaded into the system. Each file corresponds to a relational table in the library database:

#### `Books_Table.csv`
Contains ISBN, book title, and publisher name.

#### `Book_Authors_Table.csv`
Maps books to their authors. Supports **many-to-many** relationships between books and authors.

#### `Library_Branches_Table.csv`
Defines library branches, including address and name. Each branch hosts book copies.

#### `Book_Copies_Table.csv`
Links books to branches and tracks how many copies are available at each.

#### `Borrowers_Table.csv`
Stores borrower records, including names, addresses, and unique card numbers.

#### `Book_Loans_Table.csv`
Tracks which borrower checked out which book and when. Also used for overdue and return date checks.

---

## 📥 How to Run the Project

This section provides step-by-step instructions to set up and run the **Library Management System** on your local machine.

---

### 🔧 Prerequisites

Before running the project, ensure you have the following installed:

- 🐍 **Python 3.x**
- 🗃️ **SQLite** or a GUI tool like **SQLiteStudio**
- 🧰 Python standard libraries (used in script):
  - `sqlite3` (for database operations)
  - `tkinter` (for GUI interface)
  - `os` (for file operations)

> All required libraries are part of the Python standard library, so no additional installation should be needed.

---

### 🚀 Steps to Run

1. **Clone or Download the Repository**

   Download or clone the project folder from your source (GitHub, ZIP, etc.).

2. **Load the Database Schema**

   - Open `Library_Database_SchemaData.sql` using SQLiteStudio or the `sqlite3` CLI tool.
   - Run the SQL script to create all necessary tables and populate initial data.

3. **Open the GUI Application Script**

   - Locate the file `Library_Management_GUI.py`.
   - Open it using any Python IDE or a text editor.

4. **Run the Python Script**

   ```bash
   python Library_Management_GUI.py
   ```

5. **Launch the App**

   A window will launch providing the interface to:
   - Search for books
   - Loan books to borrowers
   - Return books
   - Track book copies across library branches

---

### 📎 Notes

- Make sure the database file is in the expected path or modify the database connection in the script.
- You can edit or extend the interface using the `tkinter` code provided.
- If using SQLiteStudio, you can manually inspect table contents or test queries.

---

Each of these files contributes to either **data definition**, **data population**, or **application interaction**, forming a complete relational system for managing a library’s operations.

