from tkinter import *
from tkinter import ttk
import sqlite3
import random

# Create tkinter window
root = Tk()
root.title('Library Management System')
root.geometry("600x700")

# Create a canvas and scrollbar for the scrollable frame
main_frame = Frame(root)
main_frame.pack(fill=BOTH, expand=1)

canvas = Canvas(main_frame)
canvas.pack(side=LEFT, fill=BOTH, expand=1)

scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Create a frame inside the canvas
scrollable_frame = Frame(canvas)
canvas.create_window((300, 0), window=scrollable_frame, anchor="n")


# Connect to SQLite database
conn = sqlite3.connect('lms.db')
cursor = conn.cursor()

# Helper to display results
def display_results(title, rows):
    result_window = Toplevel(root)
    result_window.title(title)
    result_window.geometry("400x400")

    result_text = Text(result_window, wrap=WORD)
    result_text.insert(INSERT, title + "\n\n")
    for row in rows:
        result_text.insert(INSERT, str(row) + "\n")
    result_text.pack()

# Generate a unique random 6-digit card number
def generate_random_card_no():
    conn = sqlite3.connect('lms.db')
    cursor = conn.cursor()

    while True:
        random_card_no = random.randint(100000, 999999)
        cursor.execute("SELECT Card_No FROM Borrower WHERE Card_No = ?", (random_card_no,))
        if cursor.fetchone() is None:
            return random_card_no

# Task 1: Checkout Book
def checkout_book():
    book_id = book_id_entry.get()
    branch_id = branch_id_entry.get()
    card_no = card_no_entry.get()
    date_out = date_out_entry.get()
    due_date = due_date_entry.get()

    conn = sqlite3.connect('lms.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
        INSERT INTO Book_Loans (Book_ID, Branch_ID, Card_No, Date_Out, Due_Date, Returned_Date, Late)
        VALUES (?, ?, ?, ?, ?, NULL, 0)
        """, (book_id, branch_id, card_no, date_out, due_date))
        cursor.execute("SELECT * FROM Book_Copies WHERE Book_ID = ? AND Branch_ID = ?", (book_id, branch_id))
        updated_copies = cursor.fetchall()
        conn.commit()
        display_results("Updated Book Copies:", updated_copies)
    except Exception as e:
        display_results("Error:", [(str(e),)])
    finally:
        conn.close()

# Task 2: Add Borrower
def add_borrower():
    borrower_name = borrower_name_entry.get()
    borrower_address = borrower_address_entry.get()
    borrower_phone = borrower_phone_entry.get()

    conn = sqlite3.connect('lms.db')
    cursor = conn.cursor()

    try:
        new_card_no = generate_random_card_no()
        cursor.execute("""
        INSERT INTO Borrower (Card_No, Name, Address, Phone)
        VALUES (?, ?, ?, ?)
        """, (new_card_no, borrower_name, borrower_address, borrower_phone))
        conn.commit()
        display_results("New Card Number:", [(new_card_no,)])
        cursor.execute("SELECT * FROM Borrower")
        all_borrowers = cursor.fetchall()
        display_results("Updated Borrower Table:", all_borrowers)
    except Exception as e:
        display_results("Error:", [(str(e),)])
    finally:
        conn.close()

# Task 3: Add New Book
def add_new_book():
    book_title = book_title_entry.get()
    publisher = publisher_entry.get()
    author_name = author_name_entry.get()

    conn = sqlite3.connect('lms.db')
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO Book (Title, Publisher)
        VALUES (?, ?)
        """, (book_title, publisher))
        book_id = cursor.lastrowid

        cursor.execute("""
        INSERT INTO Author (Book_ID, Author_Name)
        VALUES (?, ?)
        """, (book_id, author_name))

        for branch_id in range(1, 6):
            cursor.execute("""
            INSERT INTO Book_Copies (Book_ID, Branch_ID, No_Of_Copies)
            VALUES (?, ?, 5)
            """, (book_id, branch_id))

        conn.commit()

        cursor.execute("SELECT * FROM Book WHERE Book_ID = ?", (book_id,))
        new_book = cursor.fetchall()
        display_results("New Book Added:", new_book)

        cursor.execute("SELECT * FROM Author")
        updated_authors = cursor.fetchall()
        display_results("Updated Author Table:", updated_authors)

        cursor.execute("SELECT * FROM Book_Copies WHERE Book_ID = ?", (book_id,))
        updated_copies = cursor.fetchall()
        display_results("Updated Book Copies Table:", updated_copies)
    except Exception as e:
        display_results("Error:", [(str(e),)])
    finally:
        conn.close()


# Task 4: Get Loaned Copies Per Branch
def get_loaned_copies():
    book_title = loaned_copies_entry.get()

    conn = sqlite3.connect('lms.db')
    cursor = conn.cursor()

    try:
        # Query to count loaned copies per branch
        cursor.execute("""
        SELECT bl.Branch_ID, COUNT(bl.Book_ID) as Loaned_Copies
        FROM Book b
        JOIN Book_Loans bl ON b.Book_ID = bl.Book_ID
        WHERE b.Title = ?
        GROUP BY bl.Branch_ID
        """, (book_title,))

        loaned_copies = cursor.fetchall()

        if loaned_copies:
            display_results(f"Loaned Copies for '{book_title}':", loaned_copies)
        else:
            display_results(f"No Loans Found for '{book_title}'", [])
    except Exception as e:
        display_results("Error:", [(str(e),)])
    finally:
        conn.close()


# Task 5: Late Returns
def late_returns():
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()

    conn = sqlite3.connect('lms.db')
    cursor = conn.cursor()

    try:
        cursor.execute("""
        SELECT 
            bl.Book_ID, 
            b.Title AS Book_Title, 
            bl.Branch_ID, 
            lb.Branch_Name, 
            bl.Card_No, 
            bl.Due_Date, 
            bl.Returned_Date, 
            (JULIANDAY(bl.Returned_Date) - JULIANDAY(bl.Due_Date)) AS Days_Late
        FROM 
            Book_Loans bl
        JOIN 
            Book b ON bl.Book_ID = b.Book_ID
        JOIN 
            Library_Branch lb ON bl.Branch_ID = lb.Branch_ID
        WHERE 
            bl.Returned_Date IS NOT NULL 
            AND bl.Returned_Date > bl.Due_Date
            AND bl.Due_Date BETWEEN ? AND ?
        ORDER BY 
            bl.Due_Date
        """, (start_date, end_date))
        late_books = cursor.fetchall()
        display_results("Late Returns:", late_books)
    except Exception as e:
        display_results("Error:", [(str(e),)])
    finally:
        conn.close()

# Task 6a: View Borrower Balance
def view_borrower_balance():
    borrower_id = borrower_id_entry.get()
    borrower_name = borrower_name_entry.get()

    conn = sqlite3.connect('lms.db')
    cursor = conn.cursor()

    try:
        # Execute the query with the provided inputs
        cursor.execute("""
        SELECT 
            br.Card_No AS Borrower_ID,
            br.Name AS Borrower_Name,
            IFNULL(SUM(lb.LateFee), 0.00) AS LateFee_Balance
        FROM 
            Borrower br
        LEFT JOIN 
            Book_Loans bl ON br.Card_No = bl.Card_No
        LEFT JOIN 
            Library_Branch lb ON bl.Branch_ID = lb.Branch_ID
        WHERE 
            (br.Card_No = ? OR ? IS NULL) AND 
            (br.Name LIKE '%' || ? || '%' OR ? IS NULL)
        GROUP BY 
            br.Card_No, br.Name
        ORDER BY 
            LateFee_Balance DESC;
        """, (borrower_id if borrower_id else None, 
              borrower_id if borrower_id else None, 
              borrower_name if borrower_name else None, 
              borrower_name if borrower_name else None))
        
        # Fetch and display the results
        results = cursor.fetchall()
        display_results("Borrower Balance Results", results)
    except Exception as e:
        display_results("Error:", [(str(e),)])
    finally:
        conn.close()
        
# Task 6b: Search Book Information
def search_book_info():
    borrower_id = borrower_id_search_entry.get()
    book_id = book_id_search_entry.get()
    book_title = book_title_search_entry.get()
    part_book_title = part_book_title_search_entry.get()

    conn = sqlite3.connect('lms.db')
    cursor = conn.cursor()

    try:
        # Build the query dynamically based on user inputs
        query = """
        SELECT 
            b.Book_ID AS Book_ID,
            b.Title AS Book_Title,
            br.Card_No AS Borrower_ID,
            br.Name AS Borrower_Name,
            CASE 
                WHEN lb.LateFee IS NULL THEN 'Non-Applicable'
                ELSE '$' || printf('%.2f', lb.LateFee)
            END AS LateFee
        FROM 
            Book b
        JOIN 
            Book_Loans bl ON b.Book_ID = bl.Book_ID
        JOIN 
            Borrower br ON bl.Card_No = br.Card_No
        LEFT JOIN 
            Library_Branch lb ON bl.Branch_ID = lb.Branch_ID
        WHERE 
            br.Card_No = ? 
            AND (? IS NULL OR b.Book_ID = ?)
            AND (? IS NULL OR b.Title = ?)
            AND (? IS NULL OR b.Title LIKE '%' || ? || '%')
        ORDER BY 
            LateFee DESC;
        """
        
        # Execute query with parameters
        cursor.execute(query, (
            borrower_id,
            book_id if book_id else None, book_id,
            book_title if book_title else None, book_title,
            part_book_title if part_book_title else None, part_book_title
        ))

        results = cursor.fetchall()
        display_results("Book Information Results", results)
    except Exception as e:
        display_results("Error:", [(str(e),)])
    finally:
        conn.close()


# Task 1: Checkout Book
Label(scrollable_frame, text="Task 1: Checkout Book", font=("Arial", 14, "bold"), justify="center").pack(pady=10)
Label(scrollable_frame, text=(
    "Purpose: Checkout a book and update the number of available copies.\n"
    "Inputs: Provide Book ID, Branch ID, Card No, Date Out, and Due Date.\n"
    "Output: Displays the updated Book Copies table."
), font=("Arial", 10), justify="center", wraplength=550).pack(anchor="center", pady=5)
Label(scrollable_frame, text="Book ID:", justify="center").pack(anchor="center")
book_id_entry = Entry(scrollable_frame, width=30)
book_id_entry.pack()
Label(scrollable_frame, text="Branch ID:", justify="center").pack(anchor="center")
branch_id_entry = Entry(scrollable_frame, width=30)
branch_id_entry.pack()
Label(scrollable_frame, text="Card No:", justify="center").pack(anchor="center")
card_no_entry = Entry(scrollable_frame, width=30)
card_no_entry.pack()
Label(scrollable_frame, text="Date Out:", justify="center").pack(anchor="center")
date_out_entry = Entry(scrollable_frame, width=30)
date_out_entry.pack()
Label(scrollable_frame, text="Due Date:", justify="center").pack(anchor="center")
due_date_entry = Entry(scrollable_frame, width=30)
due_date_entry.pack()
Button(scrollable_frame, text="Checkout Book", command=checkout_book).pack(pady=5)

# Task 2: Add Borrower
Label(scrollable_frame, text="Task 2: Add Borrower", font=("Arial", 14, "bold"), justify="center").pack(pady=10)
Label(scrollable_frame, text=(
    "Purpose: Add a new borrower to the system.\n"
    "Inputs: Provide Borrower's Name, Address, and Phone.\n"
    "Output: Generates a new library card number and displays the updated Borrower table."
), font=("Arial", 10), justify="center", wraplength=550).pack(anchor="center", pady=5)
Label(scrollable_frame, text="Borrower Name:", justify="center").pack(anchor="center")
borrower_name_entry = Entry(scrollable_frame, width=30)
borrower_name_entry.pack()
Label(scrollable_frame, text="Borrower Address:", justify="center").pack(anchor="center")
borrower_address_entry = Entry(scrollable_frame, width=30)
borrower_address_entry.pack()
Label(scrollable_frame, text="Borrower Phone:", justify="center").pack(anchor="center")
borrower_phone_entry = Entry(scrollable_frame, width=30)
borrower_phone_entry.pack()
Button(scrollable_frame, text="Add Borrower", command=add_borrower).pack(pady=5)

# Task 3: Add New Book
Label(scrollable_frame, text="Task 3: Add New Book", font=("Arial", 14, "bold"), justify="center").pack(pady=10)
Label(scrollable_frame, text=(
    "Purpose: Add a new book to the system with its publisher and author information.\n"
    "Inputs: Provide Book Title, Publisher Name, and Author Name.\n"
    "Output: Displays the added book details and updates the Book Copies table for all branches."
), font=("Arial", 10), justify="center", wraplength=550).pack(anchor="center", pady=5)
Label(scrollable_frame, text="Book Title:", justify="center").pack(anchor="center")
book_title_entry = Entry(scrollable_frame, width=30)
book_title_entry.pack()
Label(scrollable_frame, text="Publisher:", justify="center").pack(anchor="center")
publisher_entry = Entry(scrollable_frame, width=30)
publisher_entry.pack()
Label(scrollable_frame, text="Author Name:", justify="center").pack(anchor="center")
author_name_entry = Entry(scrollable_frame, width=30)
author_name_entry.pack()
Button(scrollable_frame, text="Add New Book", command=add_new_book).pack(pady=5)

# Task 4: Get Loaned Copies Per Branch
Label(scrollable_frame, text="Task 4: Get Loaned Copies Per Branch", font=("Arial", 14, "bold"), justify="center").pack(pady=10)
Label(scrollable_frame, text=(
    "Purpose: List the number of copies loaned out per branch for a given book title.\n"
    "Inputs: Provide the Book Title.\n"
    "Output: Displays the number of loaned copies for each branch."
), font=("Arial", 10), justify="center", wraplength=550).pack(anchor="center", pady=5)
Label(scrollable_frame, text="Book Title for Loaned Copies:", justify="center").pack(anchor="center")
loaned_copies_entry = Entry(scrollable_frame, width=30)
loaned_copies_entry.pack()
Button(scrollable_frame, text="Get Loaned Copies Per Branch", command=get_loaned_copies).pack(pady=5)

# Task 5: Check Late Returns
Label(scrollable_frame, text="Task 5: Check Late Returns", font=("Arial", 14, "bold"), justify="center").pack(pady=10)
Label(scrollable_frame, text=(
    "Purpose: List books that were returned late during a specific date range.\n"
    "Inputs: Provide Start Date and End Date (YYYY-MM-DD).\n"
    "Output: Displays the details of late returns and the number of days they were late."
), font=("Arial", 10), justify="center", wraplength=550).pack(anchor="center", pady=5)
Label(scrollable_frame, text="Start Date (YYYY-MM-DD):", justify="center").pack(anchor="center")
start_date_entry = Entry(scrollable_frame, width=30)
start_date_entry.pack()
Label(scrollable_frame, text="End Date (YYYY-MM-DD):", justify="center").pack(anchor="center")
end_date_entry = Entry(scrollable_frame, width=30)
end_date_entry.pack()
Button(scrollable_frame, text="Check Late Returns", command=late_returns).pack(pady=5)

# Task 6a: View Borrower Balance
Label(scrollable_frame, text="Task 6a: View Borrower Balance", font=("Arial", 14, "bold"), justify="center").pack(pady=10)
Label(scrollable_frame, text=(
    "Purpose: View borrowers' late fee balance.\n"
    "Inputs: Optionally provide Borrower ID or Name (or part of the name).\n"
    "Output: Displays borrower ID, name, and balance. Orders by balance if no filters are applied."
), font=("Arial", 10), justify="center", wraplength=550).pack(anchor="center", pady=5)
Label(scrollable_frame, text="Borrower ID:", justify="center").pack(anchor="center")
borrower_id_entry = Entry(scrollable_frame, width=30)
borrower_id_entry.pack()
Label(scrollable_frame, text="Borrower Name (or part of name):", justify="center").pack(anchor="center")
borrower_name_entry = Entry(scrollable_frame, width=30)
borrower_name_entry.pack()
Button(scrollable_frame, text="View Borrower Balance", command=view_borrower_balance).pack(pady=5)

# Task 6b: Search Book Information
Label(scrollable_frame, text="Task 6b: Search Book Information", font=("Arial", 14, "bold"), justify="center").pack(pady=10)
Label(scrollable_frame, text=(
    "Purpose: Search for book information and late fees for a given borrower.\n"
    "Inputs: Provide Borrower ID (required), and optionally Book ID, Title, or Part of Title.\n"
    "Output: Displays book information and late fees (formatted as $0.00 or Non-Applicable)."
), font=("Arial", 10), justify="center", wraplength=550).pack(anchor="center", pady=5)
Label(scrollable_frame, text="Borrower ID (required):", justify="center").pack(anchor="center")
borrower_id_search_entry = Entry(scrollable_frame, width=30)
borrower_id_search_entry.pack()
Label(scrollable_frame, text="Book ID (optional):", justify="center").pack(anchor="center")
book_id_search_entry = Entry(scrollable_frame, width=30)
book_id_search_entry.pack()
Label(scrollable_frame, text="Book Title (optional):", justify="center").pack(anchor="center")
book_title_search_entry = Entry(scrollable_frame, width=30)
book_title_search_entry.pack()
Label(scrollable_frame, text="Part of Book Title (optional):", justify="center").pack(anchor="center")
part_book_title_search_entry = Entry(scrollable_frame, width=30)
part_book_title_search_entry.pack()
Button(scrollable_frame, text="Search Book Info", command=search_book_info).pack(pady=5)


# Start the Tkinter main loops
root.mainloop()