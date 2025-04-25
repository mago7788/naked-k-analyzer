import sqlite3
import bcrypt
import os

DB_PATH = "users.db"

def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash BLOB NOT NULL,
                role TEXT DEFAULT 'user'
            )
        ''')
        # 預設帳號 admin / 爆神123
        hashed_pw = bcrypt.hashpw("爆神123".encode("utf-8"), bcrypt.gensalt())
        cur.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                    ("admin", hashed_pw, "admin"))
        conn.commit()
        conn.close()

def verify_user(username, password):
    init_db()  # 確保資料庫存在
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    if row:
        return bcrypt.checkpw(password.encode("utf-8"), row[0])
    return False
