# crud_danhmuc.py

from mysql.connector import Error
from db_connector import connect_mysql  # Import hàm kết nối từ file db_connector


# Lấy danh sách (READ)
def get_all_danhmuc():
    connection = connect_mysql()
    if connection is None: return []
    try:
        cursor = connection.cursor(dictionary=True)
        sql = "SELECT id_danhmuc, ten_danhmuc, slug_danhmuc FROM danhmuc ORDER BY id_danhmuc"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"❌ Lỗi truy vấn: {e}")
        return []
    finally:
        if connection and connection.is_connected(): connection.close()


# Thêm (CREATE)
def insert_danhmuc(ten):
    connection = connect_mysql()
    if connection is None: return False
    try:
        cursor = connection.cursor()
        sql_insert = "INSERT INTO danhmuc (ten_danhmuc) VALUES (%s)"
        cursor.execute(sql_insert, (ten,))
        connection.commit()
        return True
    except Error as e:
        connection.rollback()
        print(f"❌ Lỗi thêm danh mục: {e}")
        return False
    finally:
        if connection and connection.is_connected(): connection.close()


# Cập nhật (UPDATE)
def cap_nhat_danh_muc(ma, data):
    connection = connect_mysql()
    if connection is None: return False
    try:
        cot_id = "id_danhmuc"
        set_clauses = [f"{col} = %s" for col in data.keys()]
        sql_set = ", ".join(set_clauses)
        sql_update = f"UPDATE danhmuc SET {sql_set} WHERE {cot_id} = %s"

        data_tuple = list(data.values()) + [ma]

        cursor = connection.cursor()
        cursor.execute(sql_update, data_tuple)
        connection.commit()
        return cursor.rowcount > 0
    except Error as e:
        connection.rollback()
        print(f"❌ Lỗi cập nhật: {e}")
        return False
    finally:
        if connection and connection.is_connected(): connection.close()


# Xóa (DELETE)
def xoa_danh_muc(ma):
    connection = connect_mysql()
    if connection is None: return False
    try:
        cursor = connection.cursor()
        sql_delete = "DELETE FROM danhmuc WHERE id_danhmuc = %s"
        cursor.execute(sql_delete, (ma,))
        connection.commit()
        return cursor.rowcount > 0
    except Error as e:
        connection.rollback()
        print(f"❌ Lỗi xóa: {e}")
        return False
    finally:
        if connection and connection.is_connected(): connection.close()