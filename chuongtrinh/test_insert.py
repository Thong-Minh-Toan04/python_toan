from common.insertdanhmuc import insert_danhmuc_tu_ket_noi
while True:
    ten=input("Nhập vào tên danh mục: ")
    insert_danhmuc_tu_ket_noi(ten)
    con=input("TIẾP TỤC y, THOÁT THÌ NHẤN BẤT KÍ TỰ BẤT KÌ")
    if con!="y":
        break