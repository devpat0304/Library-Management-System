# 📚 Library Management System – SQL, Python & GUI Integration

The **Library Management System** is a comprehensive, multi-phase database application engineered to support the full lifecycle of book circulation within a multi-branch library network. Built in **Spring 2025** as part of **CSE 3330: Database Systems** at **The University of Texas at Arlington**, this academic project models real-world library logistics through schema design, data management, and user interaction.

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
