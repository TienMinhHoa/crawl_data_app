import tkinter as tk
from tkinter import messagebox
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Hàm để lấy dữ liệu từ Google Sheet
def get_sheet_data(sheet_url):
    try:
        # Xác định phạm vi quyền truy cập của ứng dụng
        scope = ["https://spreadsheets.google.com/feeds"]
                #  , "https://www.googleapis.com/auth/drive"]
        
        # Đường dẫn tới file JSON xác thực
        creds_path = "active-bird-424212-m8-a68f6000f729.json"
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
        
        # Xác thực và khởi tạo client
        client = gspread.authorize(creds)
        
        # Mở Google Sheet bằng URL
        sheet = client.open_by_url(sheet_url).sheet1
        
        # Đọc tất cả dữ liệu từ sheet
        data = sheet.get_all_records()
        return data
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return None

# Hàm xử lý sự kiện khi nhấn nút
def on_submit():
    sheet_url = entry.get()
    data = get_sheet_data(sheet_url)
    if data:
        # Hiển thị dữ liệu trong message box (hoặc có thể xử lý và hiển thị theo cách khác)
        text_widget.delete(1.0, tk.END)  # Xóa văn bản cũ
        text_widget.insert(tk.END, str(data))

def app_theme(root):
    root.configure(bg='lightblue')
    
    # Tùy chỉnh cho tất cả các Label widget
    for widget in root.winfo_children():
        if isinstance(widget, tk.Label):
            widget.config(bg='lightblue', fg='darkblue', font=('Helvetica', 12, 'bold'))
        elif isinstance(widget, tk.Button):
            widget.config(bg='darkblue', fg='white', font=('Helvetica', 12, 'bold'))
        elif isinstance(widget, tk.Entry):
            widget.config(bg='white', fg='black', font=('Helvetica', 12))
        elif isinstance(widget, tk.Text):
            widget.config(bg='white', fg='black', font=('Helvetica', 12))
        elif isinstance(widget, tk.Message):
            widget.config(bg='lightblue', fg='darkblue', font=('Helvetica', 12))




if __name__ == "__main__":
#     print(get_sheet_data("https://docs.google.com/spreadsheets/d/13yAWHFNi5g0yXa7GuD3sw7SsMuWf0jJWoMmt3XjpoU8/edit?gid=0#gid=0"))
    root = tk.Tk()
    root.title("Google Sheets Data")

    # Tạo và sắp xếp các widget
    tk.Label(root, text="Google Sheet URL:").pack(pady=5)
    entry = tk.Entry(root, width=50)
    entry.pack(pady=5)
    submit_button = tk.Button(root, text="Fetch Data", command=on_submit)
    submit_button.pack(pady=20)

    text_widget = tk.Text(root, height=500, width=400)
    text_widget.pack(pady=20)
    # Chạy vòng lặp chính của Tkinter
    app_theme(root)
    root.mainloop()
   