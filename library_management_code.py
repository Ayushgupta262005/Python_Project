import mysql.connector as sql
from datetime import datetime, timedelta

con = sql.connect(host="localhost", password="rootroot", user="root", database="library_db")


def user_reg():
    name = str(input("Enter your name:- "))
    user_registration_no = str(input("Enter your registration number:- "))
    length_of_registration_no = len(user_registration_no)

    if length_of_registration_no == 10:
        registration_validation(name, user_registration_no)
    else:
        print("Registration number is not of exactly 10 digits, please enter again")
        user_reg()


def insert_data_into_sql(name, user_registration_no):
    query = "insert into user_input (name,user_registration_no) values (%s,%s);"
    data = (name, user_registration_no)
    c = con.cursor()
    c.execute(query, data)
    con.commit()

    query2 = "select user_id from  user_input where user_registration_no=%s;"
    data2 = (user_registration_no,)
    c2 = con.cursor()
    c2.execute(query2, data2)
    user_id = c2.fetchone()
    print("Congratulations your registration in library is successful. Your User ID is " + str(user_id[0]))
    main()


def registration_validation(name, user_registration_no):
    query = "select * from  user_input where user_registration_no=%s;"
    data = (user_registration_no,)
    c = con.cursor()
    c.execute(query, data)
    number_exist = c.fetchone()
    if number_exist:
        print("Please enter a different number, this number is already available in the database.")
        user_reg()
    else:
        insert_data_into_sql(name, user_registration_no)


def issue_book():
    c = con.cursor()
    c.execute("SELECT DISTINCT book_subject FROM book_list")
    subjects = c.fetchall()
    print("Please select from below book subject:-\nBook_subjects")
    sno = 1

    for subject in subjects:
        print(f"{sno}. {subject[0]}")
        sno += 1

    subject_id = int(input("please enter the selected subject id"))
    selected_sub = subjects[subject_id - 1]
    print(selected_sub)

    query = "select book_id,book_name from  book_list where book_subject=%s ;"
    c.execute(query, selected_sub)
    existing_books = c.fetchall()
    print("Please select from below book list:-\nBook_id, Book_name")
    for i in existing_books:
        print(str(i).replace("(", "").replace(")", "").replace("'", ""))
    book_id = int(input("Please enter the selected book id:-"))

    c = con.cursor()
    c.execute("select * from book_list where book_id=%s and book_subject=%s;", (book_id, selected_sub[0]))

    if not c.fetchone():
        print("\n\nSorry this book id doesn't exist in Library")
        issue_book()

    user_id = int(input("Please enter your user id:-"))
    c.execute("select * from  user_input where user_id=%s;", (user_id,))
    if not c.fetchone():
        print("\n\nIncorrect user id, please enter again.")
        issue_book()

    # Store current date and calculate the due date (30 days later)
    issuance_date = datetime.now().date()

    due_date = issuance_date + timedelta(days=30)

    c.execute("insert into issue_book (book_id,user_id, issuance_date, due_date) values (%s,%s,%s,%s);",
              (book_id, user_id, issuance_date.strftime('%Y-%m-%d'), due_date.strftime('%Y-%m-%d')))
    con.commit()
    print("Book issued to the user.")
    a = input("Do you want to select more books?\n")
    if a in ('yes', 'YES', 'Yes', 'Y', 'y'):
        issue_book()
    else:
        main()



def issued_book():
    user_id = int(input("Please enter your user id:- "))
    c = con.cursor()
    c.execute("select * from  user_input where user_id=%s;", (user_id,))
    if not c.fetchone():
        print("Incorrect user id, please try again.")
        issued_book()

    c.execute("select i.book_id, b.book_name, i.issuance_date from issue_book i, book_list b "
              "where i.book_id=b.book_id and user_id=%s;", (user_id,))
    book_list = c.fetchall()
    #print(book_list)
    if len(book_list):
        print("Issued books are : ")
        for i in book_list:
            book_name = i[1]
            issuance_date = datetime.strptime(i[2], '%Y-%m-%d')
            due_date = issuance_date + timedelta(days=30)
            #print(issuance_date)
            #print(due_date)
            if due_date < datetime.now():
                print(f"{book_name} (Overdue)")
            else:
                print(book_name)
    else:
        print("No books found for User Id - ", str(user_id))
    exit()


def main():
    print(''' 
    LIBRARY MANAGEMENT APPLICATION.
    Please enter your choice:
    1) User Registration
    2) Issue a book
    3) Issued Books
    4) Exit Application
    ''')

    choice = str(input("Enter task Number:- "))
    print("\n")
    if choice == '1':
        user_reg()
    elif choice == '2':
        issue_book()
    elif choice == '3':
        issued_book()
    elif choice == '4':
        print("Thank you.")
        exit()
    else:
        print("Incorrect choice given, please try again...\n\n")
        main()


program = main()
