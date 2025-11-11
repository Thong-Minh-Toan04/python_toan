import mysql.connector
from mysql.connector import Error

# THÔNG TIN KẾT NỐI (Sử dụng lại cấu hình đã định nghĩa)
DB_CONFIG = {
    "host_name": "localhost",
    "user_name": "root",
    "password": "",
    "db_name": "ql"
}


def xoa_danh_muc(id_danh_muc_can_xoa):
    """
    Xóa một danh mục cụ thể khỏi bảng 'danhmuc' dựa trên ID.
    Tự động kết nối, thực thi và đóng kết nối.

    Tham số:
    - id_danh_muc_can_xoa (int): Mã ID của danh mục cần xóa.

    Trả về:
    - True nếu xóa thành công, False nếu thất bại.
    """
    connection = None
    ten_bang = "danhmuc"
    cot_id = "id_danhmuc"

    try:
        # 1. Tự động thiết lập kết nối
        connection = mysql.connector.connect(
            host=DB_CONFIG["host_name"],
            user=DB_CONFIG["user_name"],
            passwd=DB_CONFIG["password"],
            database=DB_CONFIG["db_name"]
        )

        # 2. Định nghĩa và thực thi lệnh SQL DELETE
        sql_delete = f"DELETE FROM {ten_bang} WHERE {cot_id} = %s"
        data = (id_danh_muc_can_xoa,)

        cursor = connection.cursor()
        cursor.execute(sql_delete, data)
        connection.commit()

        # 3. Kiểm tra kết quả
        if cursor.rowcount > 0:
            print(f"✅ Đã xóa thành công Danh mục với ID = {id_danh_muc_can_xoa}.")
            return True
        else:
            print(f"⚠️ Không tìm thấy Danh mục để xóa với ID = {id_danh_muc_can_xoa}.")
            return False

    except Error as e:
        # Xử lý lỗi khóa ngoại (nếu danh mục còn sản phẩm liên kết)
        if "foreign key constraint" in str(e).lower():
            print(f"❌ LỖI KHÓA NGOẠI: Không thể xóa Danh mục ID={id_danh_muc_can_xoa} vì còn sản phẩm liên kết.")
            print("   -> Vui lòng xóa hết sản phẩm thuộc danh mục này trước.")
        else:
            print(f"❌ Lỗi khi xóa danh mục: {e}")

        if connection:
            connection.rollback()
        return False

    finally:
        # 4. Đóng kết nối
        if connection and connection.is_connected():
            connection.close()
            print("Đã đóng kết nối MySQL.")


