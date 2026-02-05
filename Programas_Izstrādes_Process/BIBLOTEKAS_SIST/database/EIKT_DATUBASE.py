"""EIKT_DATUBASE.py

Lightweight database abstraction for the library project.

This module provides a JSON-backed storage by default (located next to this file).
It also contains a small optional MySQL stub (disabled by default).

Functions provided:
 - ensure_files()
 - load_data() / save_data(data)
 - get_books()
 - add_book(title, author, isbn)
 - reserve_book(isbn, user)
 - unreserve_book(isbn)
 - cache_user(username, password)
 - get_cached_users()

This file is intended to be imported by the project's API server so all
persistence is centralized.
"""

from pathlib import Path
import json
from typing import Optional, Dict, Any
import datetime
import os

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    HAS_PG = True
except Exception:
    HAS_PG = False

BASE = Path(__file__).parent
DATA_FILE = BASE / 'data.json'
CACHE_DIR = BASE / 'cache'
USERS_CACHE = CACHE_DIR / 'users.json'

# If you want to use MySQL instead, set USE_MYSQL = True and configure DB_CONFIG
USE_MYSQL = False
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'database': 'biblioteka',
}
USE_POSTGRES = os.getenv('USE_POSTGRES', 'False').lower() in ('1', 'true', 'yes')
PG_CONFIG = {
    'host': os.getenv('PG_HOST', 'localhost'),
    'port': int(os.getenv('PG_PORT', '5432')),
    'user': os.getenv('PG_USER', 'postgres'),
    'password': os.getenv('PG_PASSWORD', 'password'),
    'dbname': os.getenv('PG_DBNAME', 'biblioteka')
}


def ensure_files():
    """Create data and cache files with defaults if they don't exist."""
    CACHE_DIR.mkdir(exist_ok=True)
    # images folder for book images
    (BASE / 'images').mkdir(exist_ok=True)
    if not DATA_FILE.exists():
        DATA_FILE.write_text(json.dumps({
            'books': [
                {'id': 1, 'title': '1984', 'author': 'George Orwell', 'isbn': '9780451524935', 'reserved': False, 'reserved_by': None, 'images': []},
            ]
        }, ensure_ascii=False, indent=2), encoding='utf-8')
    if not USERS_CACHE.exists():
        USERS_CACHE.write_text(json.dumps({'users': []}, ensure_ascii=False, indent=2), encoding='utf-8')


def load_data() -> Dict[str, Any]:
    ensure_files()
    if USE_POSTGRES:
        return {'books': get_books()}
    with DATA_FILE.open('r', encoding='utf-8') as f:
        return json.load(f)


def save_data(data: Dict[str, Any]):
    if USE_POSTGRES:
        # in Postgres mode we persist via SQL; nothing to do here
        return
    with DATA_FILE.open('w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_books():
    if USE_POSTGRES:
        return _pg_get_books()
    data = load_data()
    return data.get('books', [])


def _next_id(books: list) -> int:
    return max((b.get('id', 0) for b in books), default=0) + 1


def add_book(title: str, author: str, isbn: str) -> Dict[str, Any]:
    if USE_POSTGRES:
        return _pg_add_book(title, author, isbn)
    data = load_data()
    books = data.get('books', [])
    if any(b.get('isbn') == isbn for b in books):
        raise ValueError('exists')
    new = {'id': _next_id(books), 'title': title, 'author': author, 'isbn': isbn, 'reserved': False, 'reserved_by': None, 'images': []}
    books.append(new)
    data['books'] = books
    save_data(data)
    return new


def delete_book(isbn: str) -> Dict[str, Any]:
    data = load_data()
    books = data.get('books', [])
    for i, b in enumerate(books):
        if b.get('isbn') == isbn:
            # remove associated images from disk
            for img in b.get('images', []) or []:
                img_path = BASE / 'images' / img
                try:
                    if img_path.exists():
                        img_path.unlink()
                except Exception:
                    pass
            del books[i]
            data['books'] = books
            save_data(data)
            return {'ok': True}
    return {'ok': False, 'error': 'not_found'}


def add_book_image(isbn: str, filename: str, content: bytes) -> Dict[str, Any]:
    """Save image bytes under database/images and add filename to book record."""
    ensure_files()
    img_dir = BASE / 'images'
    # sanitize filename a little
    safe_name = Path(filename).name
    target = img_dir / safe_name
    # avoid overwrite by adding suffix if exists
    if target.exists():
        base = target.stem
        ext = target.suffix
        i = 1
        while True:
            candidate = img_dir / f"{base}-{i}{ext}"
            if not candidate.exists():
                target = candidate
                break
            i += 1
    with target.open('wb') as f:
        f.write(content)
    # add to book
    data = load_data()
    for b in data.get('books', []):
        if b.get('isbn') == isbn:
            imgs = b.get('images') or []
            imgs.append(target.name)
            b['images'] = imgs
            save_data(data)
            return {'ok': True, 'filename': target.name}
    # cleanup file if book not found
    try:
        target.unlink()
    except Exception:
        pass
    return {'ok': False, 'error': 'not_found'}


def remove_book_image(isbn: str, filename: str) -> Dict[str, Any]:
    data = load_data()
    for b in data.get('books', []):
        if b.get('isbn') == isbn:
            imgs = b.get('images') or []
            if filename in imgs:
                imgs.remove(filename)
                b['images'] = imgs
                save_data(data)
                # delete file
                p = BASE / 'images' / filename
                try:
                    if p.exists():
                        p.unlink()
                except Exception:
                    pass
                return {'ok': True}
            return {'ok': False, 'error': 'image_not_found'}
    return {'ok': False, 'error': 'not_found'}


def find_book_by_isbn(isbn: str) -> Optional[Dict[str, Any]]:
    for b in get_books():
        if b.get('isbn') == isbn:
            return b
    return None


def reserve_book(isbn: str, user: str) -> Dict[str, Any]:
    if USE_POSTGRES:
        return _pg_reserve_book(isbn, user)
    data = load_data()
    for b in data.get('books', []):
        if b.get('isbn') == isbn:
            if b.get('reserved'):
                return {'ok': False, 'error': 'already_reserved'}
            b['reserved'] = True
            b['reserved_by'] = user
            save_data(data)
            return {'ok': True}
    return {'ok': False, 'error': 'not_found'}


def unreserve_book(isbn: str) -> Dict[str, Any]:
    if USE_POSTGRES:
        return _pg_unreserve_book(isbn)
    data = load_data()
    for b in data.get('books', []):
        if b.get('isbn') == isbn:
            b['reserved'] = False
            b['reserved_by'] = None
            save_data(data)
            return {'ok': True}
    return {'ok': False, 'error': 'not_found'}


def cache_user(username: str, password: str):
    if USE_POSTGRES:
        return _pg_cache_user(username, password)
    ensure_files()
    with USERS_CACHE.open('r', encoding='utf-8') as f:
        data = json.load(f)
    users = data.get('users', [])
    users = [u for u in users if u.get('username') != username]
    users.append({'username': username, 'password': password})
    with USERS_CACHE.open('w', encoding='utf-8') as f:
        json.dump({'users': users}, f, ensure_ascii=False, indent=2)


def get_cached_users():
    if USE_POSTGRES:
        return _pg_get_cached_users()
    ensure_files()
    with USERS_CACHE.open('r', encoding='utf-8') as f:
        return json.load(f).get('users', [])

# ----------------- Postgres-backed implementations -----------------
def _pg_connect():
    if not HAS_PG:
        raise RuntimeError('psycopg2 not installed')
    return psycopg2.connect(**PG_CONFIG)


def _pg_create_tables():
    conn = _pg_connect()
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT
    );
    CREATE TABLE IF NOT EXISTS books (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        isbn TEXT UNIQUE NOT NULL
    );
    CREATE TABLE IF NOT EXISTS loans (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        book_id INTEGER REFERENCES books(id),
        borrow_date DATE,
        return_date DATE
    );
    CREATE TABLE IF NOT EXISTS images (
        id SERIAL PRIMARY KEY,
        book_id INTEGER REFERENCES books(id),
        filename TEXT
    );
    ''')
    conn.commit()
    cur.close()
    conn.close()


def _pg_get_books():
    conn = _pg_connect()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT b.id, b.title, b.author, b.isbn FROM books b')
    books = cur.fetchall()
    result = []
    for b in books:
        cur.execute('SELECT id, user_id, borrow_date, return_date FROM loans WHERE book_id=%s AND return_date IS NULL', (b['id'],))
        loan = cur.fetchone()
        reserved = bool(loan)
        reserved_by = None
        if loan:
            cur.execute('SELECT username FROM users WHERE id=%s', (loan['user_id'],))
            u = cur.fetchone()
            reserved_by = u['username'] if u else None
        # images
        cur.execute('SELECT filename FROM images WHERE book_id=%s', (b['id'],))
        imgs = [r['filename'] for r in cur.fetchall()]
        result.append({'id': b['id'], 'title': b['title'], 'author': b['author'], 'isbn': b['isbn'], 'reserved': reserved, 'reserved_by': reserved_by, 'images': imgs})
    cur.close()
    conn.close()
    return result


def _pg_add_book(title, author, isbn):
    conn = _pg_connect()
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO books (title, author, isbn) VALUES (%s,%s,%s) RETURNING id', (title, author, isbn))
        new_id = cur.fetchone()[0]
        conn.commit()
        return {'id': new_id, 'title': title, 'author': author, 'isbn': isbn, 'reserved': False, 'reserved_by': None, 'images': []}
    except psycopg2.IntegrityError:
        conn.rollback()
        raise ValueError('exists')
    finally:
        cur.close(); conn.close()


def _pg_get_or_create_user(username, password=None):
    conn = _pg_connect()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT id, username FROM users WHERE username=%s', (username,))
    u = cur.fetchone()
    if u:
        cur.close(); conn.close(); return u
    cur.execute('INSERT INTO users (username, password) VALUES (%s,%s) RETURNING id, username', (username, password))
    new = cur.fetchone()
    conn.commit(); cur.close(); conn.close()
    return new


def _pg_reserve_book(isbn, username):
    conn = _pg_connect()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    # find book
    cur.execute('SELECT id FROM books WHERE isbn=%s', (isbn,))
    b = cur.fetchone()
    if not b:
        cur.close(); conn.close(); return {'ok': False, 'error': 'not_found'}
    book_id = b['id']
    # check already loaned
    cur.execute('SELECT id FROM loans WHERE book_id=%s AND return_date IS NULL', (book_id,))
    if cur.fetchone():
        cur.close(); conn.close(); return {'ok': False, 'error': 'already_reserved'}
    user = _pg_get_or_create_user(username)
    borrow_date = datetime.date.today()
    cur = conn.cursor()
    cur.execute('INSERT INTO loans (user_id, book_id, borrow_date, return_date) VALUES (%s,%s,%s,NULL)', (user['id'], book_id, borrow_date))
    conn.commit()
    cur.close(); conn.close()
    return {'ok': True}


def _pg_unreserve_book(isbn):
    conn = _pg_connect()
    cur = conn.cursor()
    cur.execute('SELECT id FROM books WHERE isbn=%s', (isbn,))
    b = cur.fetchone()
    if not b:
        cur.close(); conn.close(); return {'ok': False, 'error': 'not_found'}
    book_id = b[0]
    cur.execute('UPDATE loans SET return_date=%s WHERE book_id=%s AND return_date IS NULL', (datetime.date.today(), book_id))
    conn.commit()
    cur.close(); conn.close()
    return {'ok': True}


def _pg_cache_user(username, password):
    conn = _pg_connect()
    cur = conn.cursor()
    cur.execute('SELECT id FROM users WHERE username=%s', (username,))
    if cur.fetchone():
        cur.close(); conn.close(); return {'ok': True}
    cur.execute('INSERT INTO users (username, password) VALUES (%s,%s)', (username, password))
    conn.commit(); cur.close(); conn.close(); return {'ok': True}


def _pg_get_cached_users():
    conn = _pg_connect()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT username FROM users')
    rows = cur.fetchall()
    cur.close(); conn.close()
    return [{'username': r['username']} for r in rows]


# If Postgres mode is requested via environment, try to ensure tables exist on import.
if USE_POSTGRES:
    if not HAS_PG:
        print('WARNING: USE_POSTGRES=True but psycopg2 is not installed. Postgres mode will not work until you install psycopg2.')
    else:
        try:
            _pg_create_tables()
        except Exception as e:
            print('Failed to initialize Postgres tables:', e)


if __name__ == '__main__':
    # simple CLI for manual operations
    ensure_files()
    print('EIKT_DATUBASE helper module')
    print('Books:')
    for b in get_books():
        print(f"{b.get('id')} | {b.get('title')} | {b.get('author')} | {b.get('isbn')} | reserved={b.get('reserved')}")
