from flask import Flask, jsonify, request
from pathlib import Path
import sqlite3
import datetime

BASE = Path(__file__).parent
DB_DIR = BASE / 'database'
DB_DIR.mkdir(exist_ok=True)
DB_FILE = DB_DIR / 'bibloteka.db'

app = Flask(__name__)


def get_conn():
    conn = sqlite3.connect(str(DB_FILE))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            isbn TEXT UNIQUE NOT NULL
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()


@app.after_request
def add_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


@app.route('/books')
def api_books():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT id, title, author, isbn FROM books ORDER BY id')
    rows = cur.fetchall()
    books = [dict(r) for r in rows]
    cur.close(); conn.close()
    return jsonify({'books': books})


@app.route('/add_book', methods=['POST'])
def api_add_book():
    body = request.get_json() or {}
    title = (body.get('title') or '').strip()
    author = (body.get('author') or '').strip()
    isbn = (body.get('isbn') or '').strip()
    if not (title and author and isbn):
        return jsonify({'error': 'missing'}), 400
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO books (title, author, isbn) VALUES (?,?,?)', (title, author, isbn))
        conn.commit()
        new_id = cur.lastrowid
        book = {'id': new_id, 'title': title, 'author': author, 'isbn': isbn}
        cur.close(); conn.close()
        return jsonify({'ok': True, 'book': book})
    except sqlite3.IntegrityError:
        cur.close(); conn.close()
        return jsonify({'error': 'exists'}), 400


@app.route('/delete_book', methods=['POST'])
def api_delete_book():
    body = request.get_json() or {}
    isbn = (body.get('isbn') or '').strip()
    if not isbn:
        return jsonify({'error': 'missing'}), 400
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('DELETE FROM books WHERE isbn = ?', (isbn,))
    changed = cur.rowcount
    conn.commit()
    cur.close(); conn.close()
    if changed:
        return jsonify({'ok': True})
    return jsonify({'error': 'not_found'}), 404


@app.route('/search')
def api_search():
    q = (request.args.get('q') or '').strip()
    conn = get_conn()
    cur = conn.cursor()
    if not q:
        cur.execute('SELECT id, title, author, isbn FROM books ORDER BY id')
    else:
        like = f'%{q}%'
        cur.execute('SELECT id, title, author, isbn FROM books WHERE title LIKE ? OR author LIKE ? ORDER BY id', (like, like))
    rows = cur.fetchall()
    books = [dict(r) for r in rows]
    cur.close(); conn.close()
    return jsonify({'books': books})


@app.route('/export_sql')
def api_export_sql():
    # produce a SQL dump (simple INSERT statements) from current DB
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT id, title, author, isbn FROM books ORDER BY id')
    rows = cur.fetchall()
    lines = ["-- bibloteka SQL dump generated\n", "CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, author TEXT, isbn TEXT UNIQUE);\n"]
    for r in rows:
        title = r['title'].replace("'", "''")
        author = r['author'].replace("'", "''")
        isbn = r['isbn'].replace("'", "''")
        lines.append(f"INSERT INTO books (id, title, author, isbn) VALUES ({r['id']}, '{title}', '{author}', '{isbn}');\n")
    cur.close(); conn.close()
    return ("".join(lines), 200, {'Content-Type': 'text/sql'})


if __name__ == '__main__':
    init_db()
    app.run(host='127.0.0.1', port=5002, debug=True)
