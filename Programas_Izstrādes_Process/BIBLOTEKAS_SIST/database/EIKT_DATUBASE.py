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


def ensure_files():
    """Create data and cache files with defaults if they don't exist."""
    CACHE_DIR.mkdir(exist_ok=True)
    if not DATA_FILE.exists():
        DATA_FILE.write_text(json.dumps({
            'books': [
                {'id': 1, 'title': '1984', 'author': 'George Orwell', 'isbn': '9780451524935', 'reserved': False, 'reserved_by': None},
            ]
        }, ensure_ascii=False, indent=2), encoding='utf-8')
    if not USERS_CACHE.exists():
        USERS_CACHE.write_text(json.dumps({'users': []}, ensure_ascii=False, indent=2), encoding='utf-8')


def load_data() -> Dict[str, Any]:
    ensure_files()
    with DATA_FILE.open('r', encoding='utf-8') as f:
        return json.load(f)


def save_data(data: Dict[str, Any]):
    with DATA_FILE.open('w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_books():
    data = load_data()
    return data.get('books', [])


def _next_id(books: list) -> int:
    return max((b.get('id', 0) for b in books), default=0) + 1


def add_book(title: str, author: str, isbn: str) -> Dict[str, Any]:
    data = load_data()
    books = data.get('books', [])
    if any(b.get('isbn') == isbn for b in books):
        raise ValueError('exists')
    new = {'id': _next_id(books), 'title': title, 'author': author, 'isbn': isbn, 'reserved': False, 'reserved_by': None}
    books.append(new)
    data['books'] = books
    save_data(data)
    return new


def find_book_by_isbn(isbn: str) -> Optional[Dict[str, Any]]:
    for b in get_books():
        if b.get('isbn') == isbn:
            return b
    return None


def reserve_book(isbn: str, user: str) -> Dict[str, Any]:
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
    data = load_data()
    for b in data.get('books', []):
        if b.get('isbn') == isbn:
            b['reserved'] = False
            b['reserved_by'] = None
            save_data(data)
            return {'ok': True}
    return {'ok': False, 'error': 'not_found'}


def cache_user(username: str, password: str):
    ensure_files()
    with USERS_CACHE.open('r', encoding='utf-8') as f:
        data = json.load(f)
    users = data.get('users', [])
    users = [u for u in users if u.get('username') != username]
    users.append({'username': username, 'password': password})
    with USERS_CACHE.open('w', encoding='utf-8') as f:
        json.dump({'users': users}, f, ensure_ascii=False, indent=2)


def get_cached_users():
    ensure_files()
    with USERS_CACHE.open('r', encoding='utf-8') as f:
        return json.load(f).get('users', [])


if __name__ == '__main__':
    # simple CLI for manual operations
    ensure_files()
    print('EIKT_DATUBASE helper module')
    print('Books:')
    for b in get_books():
        print(f"{b.get('id')} | {b.get('title')} | {b.get('author')} | {b.get('isbn')} | reserved={b.get('reserved')}")
