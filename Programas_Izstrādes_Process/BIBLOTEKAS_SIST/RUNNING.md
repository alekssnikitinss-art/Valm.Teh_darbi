RUNNING THE BIBLIOTĒKA DEMO
===========================

This document describes how to run the library demo locally on Windows (PowerShell).
It assumes you have Python 3.8+ installed and available on PATH.

Overview
--------
- Start the API server (Flask) which reads/writes JSON files in `Programas_Izstrādes_Process/BIBLOTEKAS_SIST/database`.
- Serve the static frontend from `Programas_Izstrādes_Process/BIBLOTEKAS_SIST` (so `bibloteka.html` can fetch the API).

Files you will use
------------------
- `Programas_Izstrādes_Process/BIBLOTEKAS_SIST/bibloteka.html` (frontend)
- `Programas_Izstrādes_Process/BIBLOTEKAS_SIST/func/bibloteka.js` (frontend JS)
- `Programas_Izstrādes_Process/BIBLOTEKAS_SIST/style/bibloteka.css` (CSS)
- `Programas_Izstrādes_Process/BIBLOTEKAS_SIST/database/api.py` (Flask API)
- `Programas_Izstrādes_Process/BIBLOTEKAS_SIST/database/EIKT_DATUBASE.py` (persistence module)
- `Programas_Izstrādes_Process/BIBLOTEKAS_SIST/database/data.json` (books data)
- `Programas_Izstrādes_Process/BIBLOTEKAS_SIST/database/cache/users.json` (cached users)
- `start_api_launcher.py` (helper at repo root that starts the API safely)
- `Programas_Izstrādes_Process/BIBLOTEKAS_SIST/database/run_api.ps1` (PowerShell helper script)

Steps (recommended)
-------------------
1) From repo root, create and activate a virtual environment, then install requirements:

```powershell
cd 'c:\Users\Dators\Valmieras_Teh_darbi\Valm.Teh_darbi'
python -m venv .venv; .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install flask
```

2) Start the API using the repo-root launcher (avoids path issues on Windows):

```powershell
python start_api_launcher.py
```

Alternatively, use the PowerShell helper from the `database` folder:

```powershell
cd 'c:\Users\Dators\Valmieras_Teh_darbi\Valm.Teh_darbi\Programas_Izstrades_Process\BIBLOTEKAS_SIST\database'
.\run_api.ps1
```

The API listens at: http://127.0.0.1:5001

3) Serve the static frontend in a second terminal so the browser can fetch the API without CORS/file issues:

```powershell
cd 'c:\Users\Dators\Valmieras_Teh_darbi\Valm.Teh_darbi\Programas_Izstrades_Process\BIBLOTEKAS_SIST'
python -m http.server 8000
```

Open in browser: http://127.0.0.1:8000/bibloteka.html

Quick usage
-----------
- Admin credentials: username `admin` password `admin123` (admin panel appears after login).
- Add books from admin panel — they are saved to `database/data.json`.
- Any user can login (any non-empty username/password) and will be cached to `database/cache/users.json` when logging in.
- Reserve a book as a logged-in user; the reservation is saved to `database/data.json`.

Troubleshooting
---------------
- If `import flask` fails, ensure you're using the Python from the venv you activated and run `pip install flask`.
- If the API fails to start with an import error for `EIKT_DATUBASE`, run the API using `start_api_launcher.py` from repo root (this sets the import path correctly).
- If the frontend can't load books, make sure both the API and static server are running and that the API is on port 5001.
- If you see stale data in the browser, try a hard refresh (Ctrl+F5) or check `database/data.json` for current state.

Notes
-----
- This demo stores cached user passwords in plaintext. It's only for local testing. Do not use this approach in production.
- For more durability or multiple users/processes, consider switching the persistence to SQLite.

Next steps I can help with
--------------------------
- Add an admin reservation management UI (list/unreserve/assign).
- Migrate persistence to SQLite for safer concurrent writes.
- Add automated tests for the API and database module.
 - Upload and delete book images from the admin UI. Images are stored in `Programas_Izstrādes_Process/BIBLOTEKAS_SIST/database/images` and served at `/images/<filename>` by the API.
 - Delete books via the admin panel (book data and associated images are removed).
