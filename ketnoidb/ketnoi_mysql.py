import mysql.connector
from mysql.connector import Error


def ket_noi_mysql(host_name, user_name, password, db_name):
    """
    Hàm kết nối đến cơ sở dữ liệu MySQL và trả về đối tượng kết nối (connection object).

    Tham số:
    - host_name (str): Tên host hoặc địa chỉ IP của server MySQL.
    - user_name (str): Tên người dùng MySQL.
    - password (str): Mật khẩu MySQL.
    - db_name (str): Tên cơ sở dữ liệu muốn kết nối.
    """
    connection = None
    try:
        # Cố gắng thiết lập kết nối
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=password,
            database=db_name
        )
        if connection.is_connected():
            print(f"✅ Kết nối thành công đến database '{db_name}'")
            return connection

    except Error as e:
        # Xử lý nếu có lỗi kết nối
        print(f"❌ Lỗi kết nối MySQL: {e}")
        return None


# --- Ví dụ cách sử dụng hàm ---
if __name__ == '__main__':
    # THAY ĐỔI THÔNG TIN KẾT NỐI CỦA BẠN TẠI ĐÂY
    db_conn = ket_noi_mysql(
        host_name="localhost",  # Ví dụ: "127.0.0.1"
        user_name="root",  # Tên người dùng mặc định
        password="",  # Mật khẩu của bạn
        db_name="ql"
    )

    # Sau khi kết thúc thao tác với database, bạn cần đóng kết nối
    if db_conn is not None:
        # Thực hiện các truy vấn SQL tại đây...

        db_conn.close()
        print("Đã đóng kết nối MySQL.")