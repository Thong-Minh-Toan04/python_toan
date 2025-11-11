import mysql.connector
from mysql.connector import Error

# THÔNG TIN KẾT NỐI (Cần được định nghĩa hoặc import)
DB_CONFIG = {
    "host_name": "localhost",
    "user_name": "root",
    "password": "",
    "db_name": "ql"
}


# --- Hàm Giả định Kết nối (Bạn cần đảm bảo hàm này tồn tại hoặc thay thế bằng logic kết nối của bạn) ---
def connect_mysql():
    """Tự động kết nối và trả về đối tượng connection."""
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


# --------------------------------------------------------------------------------------------------------

def get_all_danhmuc():
    """
    Lấy tất cả danh mục và trả về dưới dạng danh sách các dictionary.
    """
    connection = None
    result = []

    try:
        # 1. Kết nối database
        connection = connect_mysql()
        if connection is None:
            return []

        # 2. Tạo cursor VỚI dictionary=True
        # Điều này cho phép truy cập dữ liệu bằng tên cột (ví dụ: row['ten_danhmuc'])
        cursor = connection.cursor(dictionary=True)

        # 3. Định nghĩa và thực thi lệnh SQL
        # Bạn nên liệt kê tên cột rõ ràng thay vì dùng SELECT *, nhưng SELECT * vẫn hoạt động
        sql = "SELECT id_danhmuc, ten_danhmuc, slug_danhmuc FROM danhmuc"
        cursor.execute(sql)

        # 4. Lấy tất cả kết quả
        result = cursor.fetchall()

        # 5. In kết quả ra màn hình (Giống như trong hình ảnh của bạn)
        print("✅ Danh sách danh mục:")
        for row in result:
            # Truy cập dữ liệu bằng tên cột (key)
            # Lưu ý: Tôi dùng tên cột SQL (id_danhmuc, ten_danhmuc) thay vì madm, tendm nếu chưa được alias.
            # Nếu bạn dùng SELECT * trong SQL, tên key sẽ là tên cột trong DB.
            # Giả định: madm -> id_danhmuc, tendm -> ten_danhmuc, mota -> slug_danhmuc
            print(f"ID: {row['id_danhmuc']}, Tên: {row['ten_danhmuc']}, Slug: {row.get('slug_danhmuc', 'N/A')}")

        return result

    except Error as e:
        print(f"❌ Lỗi khi truy vấn danh mục: {e}")
        return []

    finally:
        # 6. Đóng kết nối và cursor
        if 'cursor' in locals() and cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print("Đã đóng kết nối MySQL.")

