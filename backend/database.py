import sqlite3
import os
import hashlib

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'netrecon.db')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            target TEXT NOT NULL,
            scan_type TEXT NOT NULL,
            status TEXT NOT NULL,
            result TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Database ready")

def create_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO users (username, password) VALUES (?, ?)',
            (username, hash_password(password))
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verify_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM users WHERE username = ? AND password = ?',
        (username, hash_password(password))
    )
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None

def get_user_scans(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT id, target, scan_type, status, created_at FROM scans WHERE user_id = ? ORDER BY created_at DESC',
        (user_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def save_scan(user_id, target, scan_type, result):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO scans (user_id, target, scan_type, status, result) VALUES (?, ?, ?, ?, ?)',
        (user_id, target, scan_type, 'completed', result)
    )
    conn.commit()
    scan_id = cursor.lastrowid
    conn.close()
    return scan_id

if __name__ == "__main__":
    init_db()
    created = create_user("admin", "admin123")
    if created:
        print("Admin user created")
    else:
        print("Admin already exists")
