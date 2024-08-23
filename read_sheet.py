import tkinter as tk
from tkinter import messagebox
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from gspread_dataframe import set_with_dataframe

import gspread
from oauth2client.service_account import ServiceAccountCredentials

def connect_to_sheet():
    sheet_url = 'https://docs.google.com/spreadsheets/d/13yAWHFNi5g0yXa7GuD3sw7SsMuWf0jJWoMmt3XjpoU8/edit'
    try:
        # Phạm vi quyền truy cập của ứng dụng
        scope = ["https://www.googleapis.com/auth/spreadsheets", 
                 "https://www.googleapis.com/auth/drive"]
        
        # Đường dẫn tới file JSON xác thực
        creds_path = "active-bird-424212-m8-ad9022ac0973.json"
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
        
        # Xác thực và khởi tạo client
        client = gspread.authorize(creds)
        
        # Mở Google Sheet bằng URL
        sheet = client.open_by_url(sheet_url).sheet1
        print("Kết nối thành công đến sheet")
        return sheet
    except Exception as e:
        print(f"Error: {str(e)}")



def write_value_in_sheet():
    return 0
# Hàm để lấy dữ liệu từ Google Sheet
def get_sheet_data(sheet_url):
    try:
        # Xác định phạm vi quyền truy cập của ứng dụng
        scope = ["https://spreadsheets.google.com/feeds"]
                #  , "https://www.googleapis.com/auth/drive"]
        
        # Đường dẫn tới file JSON xác thực
        creds_path = "active-bird-424212-m8-ad9022ac0973.json"
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
        
        # Xác thực và khởi tạo client
        client = gspread.authorize(creds)
        
        # Mở Google Sheet bằng URL
        sheet = connect_to_sheet()
        csv = pd.read_csv('Save_info/2024/8/20/main_version_0.csv')
        print(type(csv))

        print(csv)
        last_row = len(sheet.get_all_values())
        set_with_dataframe(sheet,csv,row= last_row+1,include_column_header = False)
        
        # Đọc tất cả dữ liệu từ sheet
        data = sheet.get_all_records()
        return data
    except Exception as e:
        print(f"error : {e}")






if __name__ == "__main__":
    url = "https://docs.google.com/spreadsheets/d/13yAWHFNi5g0yXa7GuD3sw7SsMuWf0jJWoMmt3XjpoU8/edit?gid=0#gid=0"
    print(get_sheet_data(url))
    