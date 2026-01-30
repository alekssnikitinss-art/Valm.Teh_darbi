===== Bibliotēkas sistēma: Python + MySQL =====

Prasības: pip install mysql-connector-python

import mysql.connector

----- Datubāzes konfigurācija -----

DB_CONFIG = { "host": "localhost", "user": "root", "password": "password", "database": "biblioteka" }

----- Savienojums -----

def get_connection(): return mysql.connector.connect(**DB_CONFIG)

----- Tabulu izveide -----

def create_tables(): conn = get_connection() cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    isbn VARCHAR(20) UNIQUE NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS loans (
    id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT,
    user_id INT,
    loan_date DATE,
    return_date DATE,
    FOREIGN KEY (book_id) REFERENCES books(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")

conn.commit()
conn.close()

----- Funkcijas -----

def add_book(title, author, isbn): conn = get_connection() cursor = conn.cursor() cursor.execute("INSERT INTO books (title, author, isbn) VALUES (%s, %s, %s)", (title, author, isbn)) conn.commit() conn.close() print("Grāmata pievienota!")

def search_book(keyword): conn = get_connection() cursor = conn.cursor() cursor.execute("SELECT * FROM books WHERE title LIKE %s OR author LIKE %s", (f"%{keyword}%", f"%{keyword}%")) results = cursor.fetchall() conn.close()

if results:
    for row in results:
        print(row)
else:
    print("Nav atrasta neviena grāmata.")

def delete_book(book_id): conn = get_connection() cursor = conn.cursor() cursor.execute("DELETE FROM books WHERE id=%s", (book_id,)) conn.commit() conn.close() print("Grāmata dzēsta!")

----- Konsoles izvēlne -----

def menu(): while True: print("\n--- Bibliotēkas sistēma ---") print("1 - Pievienot grāmatu") print("2 - Meklēt grāmatu") print("3 - Dzēst grāmatu") print("0 - Iziet")

choice = input("Izvēle: ")

    if choice == "1":
        title = input("Nosaukums: ")
        author = input("Autors: ")
        isbn = input("ISBN: ")
        add_book(title, author, isbn)

    elif choice == "2":
        keyword = input("Meklēšanas vārds: ")
        search_book(keyword)

    elif choice == "3":
        book_id = input("Grāmatas ID: ")
        delete_book(book_id)

    elif choice == "0":
        break

    else:
        print("Nepareiza izvēle!")

----- Programmas starts -----

if name == "main": create_tables() menu()
        (book.title, book.author, book.isbn)
    )
    db.commit()
    book.id = cursor.lastrowid

# 6.7. CRUD funkcijas
def add_book(title, author, isbn):
    if isbn in library:
        print("Šāda grāmata jau eksistē!")
        return
    book = Book(None, title, author, isbn)
    save_book(book)
    library[isbn] = book
    print("Grāmata pievienota!")

def find_by_title(title):
    return [b for b in library.values() if title.lower() in b.title.lower()]

def find_by_author(author):
    return [b for b in library.values() if author.lower() in b.author.lower()]

def delete_book(isbn):
    if isbn not in library:
        print("Grāmata nav atrasta!")
        return
    cursor.execute("DELETE FROM books WHERE isbn=%s", (isbn,))
    db.commit()
    del library[isbn]
    print("Grāmata dzēsta!")

def print_books():
    for b in library.values():
        print(f"{b.id} | {b.title} | {b.author} | {b.isbn}")

# 6.8. Konsoles izvēlne
def menu():
    while True:
        print("\n1. Pievienot grāmatu")
        print("2. Meklēt pēc nosaukuma")
        print("3. Meklēt pēc autora")
        print("4. Dzēst grāmatu")
        print("5. Parādīt visas grāmatas")
        print("0. Iziet")
        choice = input("Izvēle: ")
        if choice == "1":
            add_book(input("Nosaukums: "), input("Autors: "), input("ISBN: "))
        elif choice == "2":
            for b in find_by_title(input("Nosaukums: ")):
                print(f"{b.id} | {b.title} | {b.author} | {b.isbn}")
        elif choice == "3":
            for b in find_by_author(input("Autors: ")):
                print(f"{b.id} | {b.title} | {b.author} | {b.isbn}")
        elif choice == "4":
            delete_book(input("ISBN: "))
        elif choice == "5":
            print_books()
        elif choice == "0":
            break
        else:
            print("Nepareiza izvēle!")

# 6.9. Startējam programmu
load_books()
menu()
