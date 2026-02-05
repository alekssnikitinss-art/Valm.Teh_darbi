Local API and data storage

How to run the small local API (for development):

1. Install Flask (recommended to use a venv):

   python -m pip install flask

2. Run the API from the `database` folder:

   python api.py

The API listens on http://127.0.0.1:5001 and provides endpoints used by the frontend in the parent folder.

Data is stored in `data.json`. Cached user logins are saved to `cache/users.json`.

Note: This is a tiny development server. Do NOT use in production.
