from common.update_danhmuc import cap_nhat_danh_muc

while True:
    # 1. Nhận mã và tên mới
    ma = input("Nhập mã danh mục cần cập nhật: ")
    ten = input("Nhập tên cập nhật: ")

    # Đảm bảo mã (ID) là kiểu số nguyên
    try:
        ma = int(ma)
    except ValueError:
        print("❌ Mã danh mục phải là số nguyên.")
        continue  # Bỏ qua lần lặp này và bắt đầu lại

    # 2. TẠO DICTIONARY ĐỂ TRUYỀN VÀO HÀM
    # Hàm yêu cầu tham số thứ hai là dict: {tên_cột_SQL: giá_trị_mới}
    du_lieu_cap_nhat = {
        "ten_danhmuc": ten
    }

    # 3. Gọi hàm với định dạng tham số đúng
    cap_nhat_danh_muc(ma, du_lieu_cap_nhat)

    # 4. Kiểm tra điều kiện tiếp tục
    con = input("TIẾP TỤC (y), THOÁT THÌ NHẤN BẤT KÍ TỰ BẤT KÌ: ").lower()
    if con != "y":
        break

print("Chương trình cập nhật đã kết thúc.")