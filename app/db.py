# app/db.py
# Helper koneksi MySQL menggunakan mysql-connector-python

import mysql.connector
from mysql.connector import Error
from app.config import Config


def get_connection():
    """Buka koneksi baru ke MySQL. Tutup manual setelah selesai."""
    try:
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME,
        )
        return connection
    except Error as e:
        print(f"[ERROR] Gagal koneksi MySQL: {e}")
        raise


def fetch_all(query, params=None):
    """Eksekusi SELECT dan kembalikan semua baris sebagai list of dict."""
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        rows = cursor.fetchall()
        return rows
    finally:
        cursor.close()
        conn.close()


def execute(query, params=None):
    """Eksekusi INSERT/UPDATE/DELETE. Kembalikan jumlah baris yang terpengaruh."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        conn.commit()
        return cursor.rowcount
    except Error as e:
        conn.rollback()
        print(f"[ERROR] Query gagal: {e}")
        raise
    finally:
        cursor.close()
        conn.close()
