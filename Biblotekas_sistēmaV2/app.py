# Paplašināta Flask + MySQL WEB bibliotēkas sistēma
# Funkcijas: lietotāji, admin, grāmatu attēli, aizņemšanās, atgriešana
# Palaišana: python app.py

from flask import Flask, render_template_string, request, redirect, url_for, session
import mysql.connector
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'biblioteka_secret'
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "aleks",
    "database": "biblioteka"
}

# DB savienojums

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

# Inicializācija

def init_db():
    db = get_db()
    c = db.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100) UNIQUE,
        password VARCHAR(100),
        role ENUM('user','admin') DEFAULT 'user'
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS books (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255),
        author VARCHAR(255),
        isbn VARCHAR(50),
        image VARCHAR(255)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS loans (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        book_id INT,
        loan_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        return_date TIMESTAMP NULL,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (book_id) REFERENCES books(id)
    )''')

    # Izveido admin ja nav
    c.execute("SELECT * FROM users WHERE role='admin'")
    if not c.fetchone():
        c.execute("INSERT INTO users (username,password,role) VALUES ('admin','admin','admin')")

    db.commit()
    db.close()

# =================== ROUTES =====================

@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']

        db = get_db(); c = db.cursor()
        c.execute("SELECT * FROM users WHERE username=%s AND password=%s", (u,p))
        user = c.fetchone(); db.close()

        if user:
            session['user'] = user
            return redirect('/dashboard')
    return render_template_string(LOGIN_HTML)

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        db = get_db(); c = db.cursor()
        c.execute("INSERT INTO users (username,password) VALUES (%s,%s)",(u,p))
        db.commit(); db.close()
        return redirect('/')
    return render_template_string(REGISTER_HTML)

@app.route('/dashboard')
def dashboard():
    if 'user' not in session: return redirect('/')
    user = session['user']

    db = get_db(); c = db.cursor()
    c.execute("SELECT * FROM books")
    books = c.fetchall()

    c.execute("SELECT b.title, l.loan_date FROM loans l JOIN books b ON l.book_id=b.id WHERE l.user_id=%s AND l.return_date IS NULL", (user[0],))
    my_loans = c.fetchall()
    db.close()

    return render_template_string(DASHBOARD_HTML, books=books, user=user, loans=my_loans)

@app.route('/borrow/<int:id>')
def borrow(id):
    if 'user' not in session: return redirect('/')
    user = session['user']

    db = get_db(); c = db.cursor()
    c.execute("INSERT INTO loans (user_id,book_id) VALUES (%s,%s)",(user[0],id))
    db.commit(); db.close()
    return redirect('/dashboard')

@app.route('/admin', methods=['GET','POST'])
def admin():
    if 'user' not in session or session['user'][3] != 'admin': return redirect('/')

    if request.method == 'POST':
        f = request.files['image']
        filename = secure_filename(f.filename)
        f.save(os.path.join(UPLOAD_FOLDER, filename))

        t = request.form['title']; a = request.form['author']; i = request.form['isbn']
        db = get_db(); c = db.cursor()
        c.execute("INSERT INTO books (title,author,isbn,image) VALUES (%s,%s,%s,%s)",(t,a,i,filename))
        db.commit(); db.close()

    db = get_db(); c = db.cursor()
    c.execute("SELECT l.id,u.username,b.title,l.loan_date FROM loans l JOIN users u ON l.user_id=u.id JOIN books b ON l.book_id=b.id WHERE l.return_date IS NULL")
    loans = c.fetchall(); db.close()

    return render_template_string(ADMIN_HTML, loans=loans)

@app.route('/return/<int:id>')
def return_book(id):
    db = get_db(); c = db.cursor()
    c.execute("UPDATE loans SET return_date=NOW() WHERE id=%s",(id,))
    db.commit(); db.close()
    return redirect('/admin')

# ================= HTML ===================

LOGIN_HTML = '''<h2>Login</h2><form method=post><input name=username placeholder=Lietotājs><input name=password type=password placeholder=Parole><button>Ieiet</button></form><a href=/register>Reģistrēties</a>'''

REGISTER_HTML = '''<h2>Reģistrācija</h2><form method=post><input name=username placeholder=Lietotājs><input name=password type=password placeholder=Parole><button>Izveidot</button></form>'''

DASHBOARD_HTML = '''<h2>Sveiks {{user[1]}}</h2><a href=/admin>Admin panelis</a><h3>Grāmatas</h3><table border=1>{% for b in books %}<tr><td><img src=/static/uploads/{{b[4]}} width=60></td><td>{{b[1]}}</td><td>{{b[2]}}</td><td><a href=/borrow/{{b[0]}}>Aizņemt</a></td></tr>{% endfor %}</table><h3>Manas aizņemtās</h3>{% for l in loans %}<p>{{l[0]}} - {{l[1]}}</p>{% endfor %}'''

ADMIN_HTML = '''<h2>Admin panelis</h2><form method=post enctype=multipart/form-data><input name=title placeholder=Nosaukums><input name=author placeholder=Autors><input name=isbn placeholder=ISBN><input type=file name=image><button>Pievienot grāmatu</button></form><h3>Aizņemtās</h3><table border=1>{% for l in loans %}<tr><td>{{l[1]}}</td><td>{{l[2]}}</td><td>{{l[3]}}</td><td><a href=/return/{{l[0]}}>Atgriezt</a></td></tr>{% endfor %}</table>'''

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
