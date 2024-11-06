# database.py
import sqlite3

conn = sqlite3.connect("user_data.db")
cursor = conn.cursor()

def create_tables():
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        username TEXT,
                        full_name TEXT,
                        phone_number TEXT,
                        photo TEXT,
                        description TEXT,
                        price INTEGER,
                        seminar_link TEXT
                    )''')
    conn.commit()

def add_user(data):
    cursor.execute('''INSERT INTO users 
                      (user_id, username, full_name, phone_number, photo, description, price, seminar_link)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (
        data['user_id'], data['username'], data['full_name'], data['phone_number'],
        data['photo'], data['description'], data['price'], data['seminar_link']
    ))
    conn.commit()

def get_user(user_id):
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    return cursor.fetchone()

def delete_user(user_id):
    cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
    conn.commit()

# Викличемо функцію створення таблиць
create_tables()
