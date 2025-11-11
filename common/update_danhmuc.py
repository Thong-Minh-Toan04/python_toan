import mysql.connector
from mysql.connector import Error

# THÔNG TIN KẾT NỐI (Cần được định nghĩa hoặc import từ file cấu hình)
DB_CONFIG = {
    "host_name": "localhost",
    "user_name": "root",
    "password": "",
    "db_name": "ql"
}


def cap_nhat_danh_muc(id_danh_muc_can_cap_nhat, du_lieu_cap_nhat):
    """
    Cập nhật dữ liệu cho một danh mục trong bảng 'danhmuc'.
    Tự động kết nối, thực thi và đóng kết nối.

    Tham số:
    - id_danh_muc_can_cap_nhat (int): ID của danh mục cần cập nhật.
    - du_lieu_cap_nhat (dict): Dictionary chứa {ten_cot: gia_tri_moi}
      (ví dụ: {"ten_danhmuc": "Hot Deal Mới"}).

    Trả về:
    - True nếu cập nhật thành công, False nếu thất bại.
    """
    connection = None
    ten_bang = "danhmuc"
    cot_id = "id_danhmuc"

    # 1. Chuẩn bị câu lệnh SQL
    set_clauses = [f"{col} = %s" for col in du_lieu_cap_nhat.keys()]
    sql_set = ", ".join(set_clauses)

    # Giá trị dữ liệu (theo thứ tự các cột) + ID
    data = list(du_lieu_cap_nhat.values()) + [id_danh_muc_can_cap_nhat]

    # Câu lệnh SQL UPDATE hoàn chỉnh
    sql_update = f"UPDATE {ten_bang} SET {sql_set} WHERE {cot_id} = %s"

    try:
        # 2. Tự động thiết lập kết nối
        connection = mysql.connector.connect(
            host=DB_CONFIG["host_name"],
            user=DB_CONFIG["user_name"],
            passwd=DB_CONFIG["password"],
            database=DB_CONFIG["db_name"]
        )

        # 3. Thực thi
        cursor = connection.cursor()
        cursor.execute(sql_update, data)
        connection.commit()

        # 4. Kiểm tra kết quả
        if cursor.rowcount > 0:
            print(f"✅ Đã cập nhật thành công Danh mục Mã {id_danh_muc_can_cap_nhat}.")
            return True
        else:
            print(f"⚠️ Không tìm thấy Danh mục Mã {id_danh_muc_can_cap_nhat} để cập nhật.")
            return False

    except Error as e:
        print(f"❌ Lỗi khi cập nhật danh mục: {e}")
        if connection:
            connection.rollback()
        return False

    finally:
        # 5. Đóng kết nối
        if connection and connection.is_connected():
            connection.close()
            print("Đã đóng kết nối MySQL.")


