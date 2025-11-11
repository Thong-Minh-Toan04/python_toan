# db_connector.py

import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host_name": "localhost",
    "user_name": "root",
    "password": "",
    "db_name": "ql"
}

def connect_mysql():
    """Thiết lập kết nối database."""
    try:
        connection = mysql.connector.connect(
            host=DB_CONFIG["host_name"],
            user=DB_CONFIG["user_name"],
            passwd=DB_CONFIG["password"],
            database=DB_CONFIG["db_name"]
        )
        return connection
    except Error as e:
        print(f"❌ Lỗi kết nối: {e}")
        return None