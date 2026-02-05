# EIKT_DATUBASE — module documentation

Overview
--------

`EIKT_DATUBASE.py` is a lightweight persistence module for the Bibliotēka project.
It centralizes read/write operations for book records and a small cached-users store.

Design & behavior
------------------
- Storage: JSON files under the same `database` folder:
  - `data.json` — stores `{"books": [...]}`. Each book has fields: `id`, `title`, `author`, `isbn`, `reserved`, `reserved_by`.
  - `cache/users.json` — stores cached user credentials (in plaintext here for demo purposes).
- The module exposes a small API (functions) intended to be imported by the project's API server (`api.py`).
- Default mode is file-backed JSON. There's a stub to enable a MySQL backend by setting `USE_MYSQL = True` and providing `DB_CONFIG`, but that path is not wired by default.

Public functions
----------------
- `ensure_files()` — Create `data.json` and cache files with sane defaults if missing.
- `load_data()` / `save_data(data)` — Low-level load/save of the full JSON structure.
- `get_books()` — Returns the list of books.
- `add_book(title, author, isbn)` — Add a new book (raises `ValueError('exists')` on duplicate ISBN).
- `find_book_by_isbn(isbn)` — Return a book dict or `None`.
- `reserve_book(isbn, user)` — Mark a book as reserved by `user`. Returns `{'ok': True}` or `{'ok': False, 'error': ...}`.
- `unreserve_book(isbn)` — Clear reservation.
- `cache_user(username, password)` — Write the provided credentials into `cache/users.json`.
- `get_cached_users()` — Read cached user list.

Security
--------
This module intentionally keeps things simple for a local/demo setup. It stores passwords in plaintext in the cache file. Do not use this in production. For production-grade code:

- Use hashed passwords (bcrypt/scrypt) and proper authentication flows.
- Use a transactional database (SQLite/MySQL/Postgres) instead of flat JSON for concurrency and durability.

Usage example (from `api.py`)
----------------------------
The API server imports the module and calls functions directly, for example:

```python
import EIKT_DATUBASE as db
db.ensure_files()
books = db.get_books()
res = db.reserve_book('9780451524935', 'alice')
if res.get('ok'):
    print('Reserved')
```

Files
-----
- `EIKT_DATUBASE.py` — module implementation.
- `data.json` — book records (created automatically).
- `cache/users.json` — cached users store (created automatically).

Troubleshooting
---------------
- If `api.py` can't import the module, ensure Python's working directory or module path includes the `database` folder. The API and module live in the same folder so `import EIKT_DATUBASE` should work when running `python api.py` from the `database` folder.
- If you want to switch to MySQL you must install `mysql-connector-python` and set `USE_MYSQL = True` and configure `DB_CONFIG`.

Contact
-------
If you want, I can:
- Wire a simple SQLite backend instead of JSON for better durability.
- Add unit tests for the module functions.
- Add admin endpoints for manual reservation management.
