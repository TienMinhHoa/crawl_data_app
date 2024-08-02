import tkinter as tk
from tkinter import ttk

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Ví dụ về ttk.Treeview trong ttk.Notebook")

# Tạo Notebook
notebook = ttk.Notebook(root)

# Tạo các khung để thêm vào Notebook
khung1 = ttk.Frame(notebook, width=400, height=280)
khung2 = ttk.Frame(notebook, width=400, height=280)

# Thêm các khung vào Notebook với tiêu đề tương ứng
notebook.add(khung1, text='Tab 1')
notebook.add(khung2, text='Tab 2')

# Đặt Notebook trong cửa sổ chính
notebook.pack(expand=True, fill='both')

# Tạo Treeview trong khung1 để hiển thị danh sách dài
tree = ttk.Treeview(khung1, columns=("Name", "Age"), show='headings')
tree.heading("Name", text="Tên")
tree.heading("Age", text="Tuổi")

# Thêm dữ liệu vào Treeview
data = [
    ("Nguyễn Văn A", 28),
    ("Trần Thị B", 22),
    ("Lê Văn C", 35),
    ("Phạm Thị D", 45),
    ("Hoàng Văn E", 29),
    # Thêm nhiều dữ liệu hơn nếu cần
]

for item in data:
    tree.insert('', tk.END, values=item)

# Đặt Treeview vào khung1
tree.pack(expand=True, fill='both')

# Chạy vòng lặp chính
root.mainloop()
