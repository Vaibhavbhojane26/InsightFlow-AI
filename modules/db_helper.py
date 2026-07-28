import sqlite3
import os

DATABASE_PATH = "database/database.db"


def create_database():

    os.makedirs("database", exist_ok=True)

    conn = sqlite3.connect(DATABASE_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS uploaded_files(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        rows_count INTEGER,
        columns_count INTEGER,
        upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def save_file(filename, rows, columns):

    conn = sqlite3.connect(DATABASE_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO uploaded_files(filename, rows_count, columns_count)
    VALUES(?,?,?)
    """, (filename, rows, columns))

    conn.commit()
    conn.close()


def get_uploaded_files():

    conn = sqlite3.connect(DATABASE_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM uploaded_files
    ORDER BY upload_date DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data