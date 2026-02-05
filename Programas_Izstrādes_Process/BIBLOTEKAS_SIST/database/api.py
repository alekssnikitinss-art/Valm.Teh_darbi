from flask import Flask, jsonify, request, send_from_directory
import sys
from pathlib import Path
from werkzeug.utils import secure_filename

# Ensure this folder is on sys.path so imports work even if cwd differs
BASE = Path(__file__).parent.resolve()
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

import EIKT_DATUBASE as db

app = Flask(__name__)


@app.after_request
def add_cors_headers(response):
    # allow requests from local static server
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

ADMIN_USER = 'admin'
ADMIN_PASS = 'admin123'

# initialize files managed by EIKT_DATUBASE
db.ensure_files()

@app.route('/data.json')
def data_file():
    # return JSON data produced by the database module
    return jsonify(db.load_data())

@app.route('/api/login', methods=['POST'])
def api_login():
    body = request.json or {}
    u = body.get('username')
    p = body.get('password')
    if u == ADMIN_USER and p == ADMIN_PASS:
        return jsonify({'ok':True,'admin':True})
    # simple user check: accept any non-empty credentials and cache
    if u and p:
        return jsonify({'ok':True,'admin':False})
    return jsonify({'ok':False}), 401

@app.route('/api/cache_user', methods=['POST'])
def api_cache_user():
    body = request.json or {}
    u = body.get('username')
    p = body.get('password')
    if u and p:
        # idempotent cache: if user exists, do nothing; otherwise save
        try:
            db.cache_user(u, p)
            return jsonify({'ok': True})
        except Exception:
            return jsonify({'ok': False, 'error': 'cache_error'}), 500
    return jsonify({'ok':False,'error':'missing'}),400


def _is_admin_request(req):
    # accept admin credentials in JSON body or form fields
    body = None
    if req.is_json:
        body = req.get_json()
        au = body.get('admin_username') if body else None
        ap = body.get('admin_password') if body else None
    else:
        au = req.form.get('admin_username')
        ap = req.form.get('admin_password')
    # also allow credentials via headers for GET or simpler fetches
    if not au:
        au = req.headers.get('X-Admin-Username')
    if not ap:
        ap = req.headers.get('X-Admin-Password')
    return au == ADMIN_USER and ap == ADMIN_PASS


@app.route('/api/admin/delete_book', methods=['POST'])
def api_admin_delete_book():
    body = request.json or {}
    isbn = body.get('isbn')
    if not _is_admin_request(request):
        return jsonify({'ok':False,'error':'forbidden'}),403
    if not isbn:
        return jsonify({'ok':False,'error':'missing'}),400
    res = db.delete_book(isbn)
    if res.get('ok'):
        return jsonify({'ok':True})
    return jsonify(res), 404


@app.route('/api/admin/upload_image', methods=['POST'])
def api_admin_upload_image():
    # expects multipart/form-data with `isbn` and file field `image`
    isbn = request.form.get('isbn')
    if not _is_admin_request(request):
        return jsonify({'ok':False,'error':'forbidden'}),403
    if not isbn or 'image' not in request.files:
        return jsonify({'ok':False,'error':'missing'}),400
    f = request.files['image']
    filename = secure_filename(f.filename)
    content = f.read()
    res = db.add_book_image(isbn, filename, content)
    if res.get('ok'):
        return jsonify({'ok':True,'filename':res.get('filename')})
    return jsonify(res), 400


@app.route('/api/admin/delete_image', methods=['POST'])
def api_admin_delete_image():
    body = request.json or {}
    if not _is_admin_request(request):
        return jsonify({'ok':False,'error':'forbidden'}),403
    isbn = body.get('isbn')
    filename = body.get('filename')
    if not (isbn and filename):
        return jsonify({'ok':False,'error':'missing'}),400
    res = db.remove_book_image(isbn, filename)
    if res.get('ok'):
        return jsonify({'ok':True})
    return jsonify(res), 400


@app.route('/api/admin/reservations', methods=['GET'])
def api_admin_reservations():
    if not _is_admin_request(request):
        return jsonify({'ok':False,'error':'forbidden'}),403
    # return list of reserved books
    books = db.get_books()
    reserved = [b for b in books if b.get('reserved')]
    return jsonify({'ok':True,'reservations': reserved})


@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(str(Path(__file__).parent / 'images'), filename)

@app.route('/api/reserve', methods=['POST'])
def api_reserve():
    body = request.json or {}
    isbn = body.get('isbn')
    user = body.get('user')
    if not isbn or not user:
        return jsonify({'ok':False,'error':'missing'}),400
    res = db.reserve_book(isbn, user)
    if res.get('ok'):
        return jsonify({'ok':True})
    return jsonify(res), 400 if res.get('error')!='not_found' else 404

@app.route('/api/admin/add_book', methods=['POST'])
def api_admin_add_book():
    body = request.json or {}
    if not _is_admin_request(request):
        return jsonify({'ok':False,'error':'forbidden'}),403
    title = body.get('title')
    author = body.get('author')
    isbn = body.get('isbn')
    if not (title and author and isbn):
        return jsonify({'ok':False,'error':'missing'}),400
    try:
        db.add_book(title, author, isbn)
        return jsonify({'ok':True})
    except ValueError as e:
        return jsonify({'ok':False,'error':str(e)}),400

if __name__ == '__main__':
    # start simple dev server
    app.run(host='127.0.0.1', port=5001, debug=True)
