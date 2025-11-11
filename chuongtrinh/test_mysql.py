from ketnoidb.ketnoi_mysql import ket_noi_mysql

# Ví dụ sửa lỗi: Thêm tên cơ sở dữ liệu (ví dụ: 'an_khang_db')
ket_noi_mysql(
    host_name="localhost",
    user_name="root",
    password="",
    db_name="" # <--- THÊM TÊN DATABASE CỦA BẠN VÀO ĐÂY
)