from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_cors import CORS
import json
import os
import sys
import logging

logging.basicConfig(
    filename='netrecon.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

sys.path.insert(0, os.path.dirname(__file__))

from scanner import run_scan
from parser import parse_scan_result
from database import get_connection, init_db, verify_user, create_user, save_scan, get_user_scans

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), '..', 'frontend', 'templates'),
    static_folder=os.path.join(os.path.dirname(__file__), '..', 'frontend', 'static')
)

app.secret_key = 'netrecon_secret_2026'
CORS(app)
@app.before_request
def log_request():
    logging.info(
        "IP: " + str(request.remote_addr) +
        " Method: " + request.method +
        " Path: " + request.path +
        " User: " + str(session.get('username', 'NOT LOGGED IN'))
    )

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

@app.route('/')
@login_required
def index():
    return render_template('index.html', username=session['username'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        user = verify_user(username, password)
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            logging.info("SUCCESS LOGIN - IP: " + request.remote_addr + " User: " + username)
            return jsonify({"success": True})
        logging.warning("FAILED LOGIN - IP: " + request.remote_addr + " User: " + username)
        return jsonify({"success": False, "error": "Invalid username or password"}), 401
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        if not username or not password:
            return jsonify({"success": False, "error": "All fields required"}), 400
        created = create_user(username, password)
        if created:
            return jsonify({"success": True})
        return jsonify({"success": False, "error": "Username already exists"}), 400
    return render_template('register.html')

@app.route('/api/scan', methods=['POST'])
@login_required
def scan():
    data = request.get_json()
    target = data.get('target', '').strip()
    scan_type = data.get('scan_type', 'basic')
    if not target:
        return jsonify({"error": "Target is required"}), 400
    raw = run_scan(target, scan_type)
    parsed = parse_scan_result(raw)
    scan_id = save_scan(session['user_id'], target, scan_type, json.dumps(parsed))
    parsed['scan_id'] = scan_id
    return jsonify(parsed)

@app.route('/api/scans', methods=['GET'])
@login_required
def get_scans():
    scans = get_user_scans(session['user_id'])
    return jsonify(scans)

@app.route('/api/scans/<int:scan_id>', methods=['GET'])
@login_required
def get_scan(scan_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM scans WHERE id = ? AND user_id = ?',
        (scan_id, session['user_id'])
    )
    row = cursor.fetchone()
    conn.close()
    if row is None:
        return jsonify({"error": "Scan not found"}), 404
    scan = dict(row)
    scan['result'] = json.loads(scan['result'])
    return jsonify(scan)

if __name__ == '__main__':
    init_db()
    print("Starting NetRecon server...")
    app.run(host='0.0.0.0', port=5000, debug=True)
