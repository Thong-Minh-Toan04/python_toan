# app_gui.py

import tkinter as tk
from tkinter import ttk, messagebox

# Import tất cả các hàm CRUD từ file xử lý dữ liệu
from crud_danhmuc import get_all_danhmuc, insert_danhmuc, cap_nhat_danh_muc, xoa_danh_muc


class QuanLyDanhMucApp:
    def __init__(self, master):
        self.master = master
        master.title("Quản lý Danh mục Sản phẩm")
        master.geometry("700x500")
        master.resizable(False, False)

        # --- Variables ---
        self.ma_dm = tk.StringVar()
        self.ten_dm = tk.StringVar()
        self.slug_dm = tk.StringVar()  # Biến cho trường Mô tả/Slug

        # --- Cấu trúc Layout ---
        self.frame_input = ttk.LabelFrame(master, text="Thông tin danh mục", padding=(10, 5))
        self.frame_input.pack(fill='x', padx=10, pady=5)

        self.frame_buttons = ttk.Frame(master, padding="10")
        self.frame_buttons.pack(fill='x', padx=10, pady=5)

        self.frame_tree = ttk.Frame(master, padding="10")
        self.frame_tree.pack(fill='both', expand=True)

        self._tao_form_nhap_lieu()
        self._tao_cac_nut_chuc_nang()
        self._tao_bang_hien_thi()

        self.load_danh_muc()  # Tải dữ liệu ban đầu

    def _tao_form_nhap_lieu(self):
        # Mã Danh mục (ID) - Cho phép nhập theo yêu cầu sau cùng của bạn
        ttk.Label(self.frame_input, text="Mã DM (ID):").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.entry_ma = ttk.Entry(self.frame_input, textvariable=self.ma_dm, state='normal')
        self.entry_ma.grid(row=0, column=1, padx=5, pady=5, sticky='we')

        # Tên Danh mục
        ttk.Label(self.frame_input, text="Tên Danh mục:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(self.frame_input, textvariable=self.ten_dm, width=40).grid(row=1, column=1, padx=5, pady=5,
                                                                             sticky='we')

        # Mô tả/Slug
        ttk.Label(self.frame_input, text="Mô tả/Slug:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(self.frame_input, textvariable=self.slug_dm, width=40).grid(row=2, column=1, padx=5, pady=5,
                                                                              sticky='we')

        self.frame_input.grid_columnconfigure(1, weight=1)

    def _tao_cac_nut_chuc_nang(self):
        ttk.Button(self.frame_buttons, text="➕ Thêm", command=self.them_danh_muc).grid(row=0, column=0, padx=5, pady=5,
                                                                                       sticky='we')
        ttk.Button(self.frame_buttons, text="✏️ Sửa", command=self.sua_danh_muc).grid(row=0, column=1, padx=5, pady=5,
                                                                                      sticky='we')
        ttk.Button(self.frame_buttons, text="🗑️ Xóa", command=self.xoa_danh_muc_ui).grid(row=0, column=2, padx=5,
                                                                                         pady=5, sticky='we')
        ttk.Button(self.frame_buttons, text="🔄 Tải lại", command=self.load_danh_muc).grid(row=0, column=3, padx=5,
                                                                                          pady=5, sticky='we')

        for i in range(4):
            self.frame_buttons.grid_columnconfigure(i, weight=1)

    def _tao_bang_hien_thi(self):
        self.tree = ttk.Treeview(self.frame_tree, columns=("ID", "TenDM", "Slug"), show='headings')
        self.tree.heading("ID", text="Mã DM")
        self.tree.heading("TenDM", text="Tên Danh mục")
        self.tree.heading("Slug", text="Mô tả/Slug")

        self.tree.column("ID", width=50, anchor='center')
        self.tree.column("TenDM", width=250)
        self.tree.column("Slug", width=150)

        vsb = ttk.Scrollbar(self.frame_tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')

        self.frame_tree.grid_rowconfigure(0, weight=1)
        self.frame_tree.grid_columnconfigure(0, weight=1)

        self.tree.bind('<<TreeviewSelect>>', self.select_item)

    # --- LOGIC XỬ LÝ SỰ KIỆN GỌI HÀM CRUD ---

    def load_danh_muc(self):
        """Tải dữ liệu từ DB (crud_danhmuc.py) và hiển thị lên Treeview."""
        for i in self.tree.get_children():
            self.tree.delete(i)

        data = get_all_danhmuc()  # GỌI HÀM SELECT

        if data:
            for dm in data:
                self.tree.insert('', tk.END, values=(
                    dm['id_danhmuc'],
                    dm['ten_danhmuc'],
                    dm.get('slug_danhmuc', '')
                ))

        self.lam_moi_form()

    def select_item(self, event):
        """Điền dữ liệu từ dòng được chọn lên form."""
        selected_item = self.tree.focus()
        if selected_item:
            values = self.tree.item(selected_item, 'values')
            self.ma_dm.set(values[0])  # ID
            self.ten_dm.set(values[1])  # Tên
            self.slug_dm.set(values[2])  # Slug
        else:
            self.lam_moi_form()

    def lam_moi_form(self):
        """Xóa nội dung trên form nhập liệu."""
        self.ma_dm.set("")
        self.ten_dm.set("")
        self.slug_dm.set("")

    def them_danh_muc(self):
        """Xử lý chức năng Thêm (CREATE)."""
        ten = self.ten_dm.get().strip()

        # Bỏ qua ID nhập vào vì dùng AUTO_INCREMENT
        if not ten:
            messagebox.showerror("Lỗi", "Tên danh mục không được để trống!")
            return

        if insert_danhmuc(ten):
            messagebox.showinfo("Thành công", f"Đã thêm danh mục '{ten}'!")
            self.load_danh_muc()
        else:
            messagebox.showerror("Lỗi", "Thêm danh mục thất bại!")

    def sua_danh_muc(self):
        """Xử lý chức năng Sửa (UPDATE)."""
        ma_str = self.ma_dm.get().strip()
        ten = self.ten_dm.get().strip()
        slug = self.slug_dm.get().strip()

        if not ma_str:
            messagebox.showerror("Lỗi", "Vui lòng nhập Mã ID hoặc chọn danh mục cần sửa!")
            return

        try:
            ma = int(ma_str)
        except ValueError:
            messagebox.showerror("Lỗi", "Mã ID phải là số nguyên hợp lệ!")
            return

        # Chỉ cập nhật Tên và Slug
        data_update = {"ten_danhmuc": ten, "slug_danhmuc": slug}

        if cap_nhat_danh_muc(ma, data_update):
            messagebox.showinfo("Thành công", f"Đã cập nhật Danh mục ID {ma}!")
            self.load_danh_muc()
        else:
            messagebox.showerror("Lỗi Sửa", "Cập nhật danh mục thất bại!")

    def xoa_danh_muc_ui(self):
        """Xử lý chức năng Xóa (DELETE)."""
        ma_str = self.ma_dm.get().strip()

        if not ma_str:
            messagebox.showerror("Lỗi", "Vui lòng nhập Mã ID hoặc chọn danh mục cần xóa!")
            return

        try:
            ma = int(ma_str)
        except ValueError:
            messagebox.showerror("Lỗi", "Mã ID phải là số nguyên hợp lệ!")
            return

        if messagebox.askyesno("Xác nhận Xóa", f"Bạn có chắc chắn muốn xóa danh mục ID: {ma} không?"):
            if xoa_danh_muc(ma):
                messagebox.showinfo("Thành công", f"Đã xóa Danh mục ID {ma}!")
                self.load_danh_muc()
            else:
                messagebox.showerror("Lỗi Xóa", "Xóa danh mục thất bại (Kiểm tra khóa ngoại)!")


if __name__ == '__main__':
    root = tk.Tk()
    app = QuanLyDanhMucApp(root)
    root.mainloop()