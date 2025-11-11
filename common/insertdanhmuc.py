import mysql.connector
from mysql.connector import Error

# Định nghĩa lại thông tin kết nối (Cần đặt nó ở phạm vi toàn cục hoặc truyền vào)
DB_CONFIG = {
    "host_name": "localhost",
    "user_name": "root",
    "password": "",  # Đảm bảo mật khẩu này là đúng
    "db_name": "ql"
}


def insert_danhmuc_tu_ket_noi(ten_danhmuc):
    """
    Thêm một danh mục mới, tự động kết nối và đóng kết nối.

    Tham số:
    - ten_danhmuc (str): Tên danh mục muốn thêm vào.
    """
    connection = None
    try:
        # 1. THIẾT LẬP KẾT NỐI BÊN TRONG HÀM
        connection = mysql.connector.connect(
            host=DB_CONFIG["host_name"],
            user=DB_CONFIG["user_name"],
            passwd=DB_CONFIG["password"],
            database=DB_CONFIG["db_name"]
        )

        # 2. Thực thi lệnh INSERT
        sql_insert = "INSERT INTO danhmuc (ten_danhmuc) VALUES (%s)"
        data = (ten_danhmuc,)

        cursor = connection.cursor()
        cursor.execute(sql_insert, data)
        connection.commit()

        print(f"✅ Đã thêm danh mục '{ten_danhmuc}' thành công. ID mới: {cursor.lastrowid}")
        return True

    except Error as e:
        print(f"❌ Lỗi khi thêm danh mục: {e}")
        if connection:
            connection.rollback()
        return False

    finally:
        # 3. ĐÓNG KẾT NỐI SAU KHI THAO TÁC XONG
        if connection and connection.is_connected():
            connection.close()
            print("Đã đóng kết nối MySQL.")

