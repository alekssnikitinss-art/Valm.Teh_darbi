import mysql.connector
from datetime import date

# 6.1. MySQL savienojums
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="library"
)
cursor = db.cursor()

# 6.2. Tabulas izveide
cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    author VARCHAR(255),
    isbn VARCHAR(20) UNIQUE
)
""")
db.commit()

# 6.3. Datu struktūra atmiņā
library = {}

# 6.4. Book klase
class Book:
    def __init__(self, id, title, author, isbn):
        self.id = id
        self.title = title
        self.author = author
        self.isbn = isbn

# 6.5. Ielāde no MySQL
def load_books():
    cursor.execute("SELECT * FROM books")
    for row in cursor.fetchall():
        book = Book(*row)
        library[book.isbn] = book

# 6.6. Saglabāšana MySQL
def save_book(book):
    cursor.execute(
        "INSERT INTO books (title, author, isbn) VALUES (%s,%s,%s)",
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
