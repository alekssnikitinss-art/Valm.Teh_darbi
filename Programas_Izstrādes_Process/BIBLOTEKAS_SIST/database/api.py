from flask import Flask, jsonify, request
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

def read_data():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_data(d):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

def cache_user(username, password):
    with open(USERS_CACHE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    users = data.get('users', [])
    # store minimal info (do not store plaintext in production)
    users = [u for u in users if u.get('username')!=username]
    users.append({'username':username,'password':password})
    with open(USERS_CACHE, 'w', encoding='utf-8') as f:
        json.dump({'users':users}, f, ensure_ascii=False, indent=2)

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
        db.cache_user(u,p)
        return jsonify({'ok':True})
    return jsonify({'ok':False,'error':'missing'}),400

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
