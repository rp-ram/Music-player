# authentication.py

import sqlite3
import hashlib

def create_database():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      username TEXT NOT NULL,
                      userid TEXT NOT NULL,
                      password TEXT NOT NULL,
                      email TEXT NOT NULL,
                      mobilenumber TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def register_user(username, userid, password, email, mobilenumber):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, userid, password, email, mobilenumber) VALUES (?, ?, ?, ?, ?)",
                   (username, userid, hashed_password, email, mobilenumber))
    conn.commit()
    conn.close()

def verify_user(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE userid=? AND password=?", (username, hashed_password))
    user = cursor.fetchone()
    conn.close()
    return user
