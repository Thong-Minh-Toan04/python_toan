from common.delete_danhmuc import xoa_danh_muc

while True:
    ma=input("Nhập mã danh mục cần xóa: ")
    xoa_danh_muc(ma)
    con=input("TIẾP TỤC y, THOÁT THÌ NHẤN BẤT KÍ TỰ BẤT KÌ")
    if con!="y":
        break
# Demo
