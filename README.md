This Python project is a simple command-line-based Library Management System, which allows users to register, issue books, and view issued books. It uses mysql.connector to interact with a MySQL database. Here's a breakdown of the key components and functions:

1. Database Connection
The project establishes a connection to a MySQL database named library_db using the credentials provided (host="localhost", user="root", password="rootroot").
2. User Registration (user_reg function)
The user_reg() function handles the registration process by prompting the user to enter a name and a registration number.
If the registration number is exactly 10 digits, the system validates whether the number is already in the database using registration_validation(). If not, it stores the user details using insert_data_into_sql().
If the registration number is already taken or invalid, the function asks for input again.
3. Inserting User Data (insert_data_into_sql function)
This function inserts the user's name and registration number into the user_input table.
It then retrieves the generated user_id and confirms successful registration.
4. Registration Validation (registration_validation function)
Checks if a given registration number already exists in the database by querying the user_input table.
If the registration number is already in use, it prompts the user to enter a different one.
5. Issue Book (issue_book function)
This function allows a user to issue a book.
It starts by displaying available book subjects and books based on the selected subject.
The user selects a book and provides their user_id.
The function then checks if the book and user ID are valid before issuing the book.
The current date is recorded as the issuance date, and the due date is set to 30 days later.
The issuance details are stored in the issue_book table, and the user is asked if they want to issue more books.
6. Viewing Issued Books (issued_book function)
This function lists the books that have been issued to a user.
The user provides their user_id, which is validated against the user_input table.
If the user has issued books, the details (book name, issuance date) are displayed.
It also checks if any issued book is overdue (past the 30-day due date) and indicates this in the output.
7. Main Menu (main function)
The main function provides a menu-driven interface for the user.
Users can choose to register, issue a book, view issued books, or exit the application.
It directs users to the appropriate function based on their choice.
Database Structure
The following tables are used:

user_input: Stores user details (name, registration number, and user ID).
book_list: Stores book details (book ID, book name, and book subject).
issue_book: Stores information about issued books, including the book ID, user ID, issuance date, and due date.
Limitations and Suggestions for Improvement:
Error Handling: The program uses basic input validation. It can be improved by catching more specific exceptions and providing more informative error messages.
User Interface: It's a command-line program; a graphical user interface (GUI) using a library like tkinter could make it more user-friendly.
Database Security: Storing passwords directly in the code is not secure. Consider using environment variables or secure credential management.
Concurrency Issues: For multiple users accessing the system, there should be locks or checks to avoid data integrity issues.
