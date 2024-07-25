import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import CustomSearch

class ExcelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Excel Data Processor")

        # Add a frame for the top section
        top_frame = tk.Frame(root)
        top_frame.pack(pady=10, fill='x')

        # Label cho người dùng hiểu combobox là để chọn bắt đầu
        start_label = tk.Label(top_frame, text="Start Cell:")
        start_label.grid(row=0, column=0, padx=5)

        # Combobox chọn ô bắt đầu
        self.start_combobox = ttk.Combobox(top_frame)
        self.start_combobox.grid(row=0, column=1, padx=5)

        # Label cho người dùng hiểu combobox là để chọn kết thúc
        end_label = tk.Label(top_frame, text="End Cell:")
        end_label.grid(row=0, column=2, padx=5)

        # Combobox chọn ô kết thúc
        self.end_combobox = ttk.Combobox(top_frame)
        self.end_combobox.grid(row=0, column=3, padx=5)

        # Add a button to load Excel file
        self.load_button = tk.Button(top_frame, text="Load Excel File", command=self.load_excel)
        self.load_button.grid(row=0, column=4, padx=5)

        # Add a label for the search content
        search_label = tk.Label(top_frame, text="Nội dung tìm kiếm")
        search_label.grid(row=0, column=5, padx=5)

        # Add an Entry to display and edit search content
        self.search_content_var = tk.StringVar(value="Tuyển dụng 2024")
        self.search_content_entry = tk.Entry(top_frame, textvariable=self.search_content_var, width=20)
        self.search_content_entry.grid(row=0, column=6, padx=5)

        # Add a button to save content with styling
        self.save_button = tk.Button(top_frame, text="Run", command=self.run_action, 
                                     font=('Arial', 12, 'bold'), bg='blue', fg='white', width=15)
        self.save_button.grid(row=0, column=9, padx=5)

        # Add a label for the sheet selection
        sheet_label = tk.Label(top_frame, text="Sheet:")
        sheet_label.grid(row=0, column=7, padx=5)

        # Create a Combobox to select sheets
        self.sheet_selector = ttk.Combobox(top_frame)
        self.sheet_selector.grid(row=0, column=8, padx=5)
        self.sheet_selector.bind("<<ComboboxSelected>>", self.display_sheet)

        # Add a checkbox to select whether to save the file
        self.save_file_var = tk.BooleanVar()
        save_file_check = tk.Checkbutton(top_frame, text="Xuất file", variable=self.save_file_var)
        save_file_check.grid(row=0, column=10, padx=5)

        # Frame to hold the column buttons and Treeview
        self.table_frame = tk.Frame(root)
        self.table_frame.pack(padx=10, pady=10, fill='both', expand=True)

        self.status_label = tk.Label(root, text="", fg="red")
        self.status_label.pack(pady=20)

        self.tree_frame = tk.Frame(self.table_frame)
        self.tree_frame.pack(fill='both', expand=True)

        # Scrollbars
        self.tree_scroll_y = ttk.Scrollbar(self.tree_frame, orient='vertical')
        self.tree_scroll_x = ttk.Scrollbar(self.tree_frame, orient='horizontal')
        self.tree_scroll_y.pack(side='right', fill='y')
        self.tree_scroll_x.pack(side='bottom', fill='x')

        self.tree = None
        self.excel_file = None
        self.df = None
        self.selected_column_data = {}  # Dictionary to store selected column data
    
    def load_excel(self):
        # Open a file dialog to select an Excel file
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
        
        if not file_path:
            return
        
        # Read the Excel file using Pandas to get sheet names
        try:
            self.excel_file = pd.ExcelFile(file_path)
            sheet_names = self.excel_file.sheet_names
            self.sheet_selector['values'] = sheet_names
            self.sheet_selector.current(0)  # Select the first sheet by default
            self.display_sheet()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read Excel file: {e}")
    
    def display_sheet(self, event=None):
        sheet_name = self.sheet_selector.get()
        self.df = pd.read_excel(self.excel_file, sheet_name=sheet_name)
        self.update_treeview()
        self.update_comboboxes()

    def show_waiting_message(self):
        self.status_label.config(text="Processing, please wait...")
        self.root.update_idletasks()
    def hide_waiting_message(self):
        self.status_label.config(text="")
        self.root.update_idletasks()

    def update_treeview(self):
        if self.tree:
            self.tree.destroy()

        self.tree = ttk.Treeview(self.tree_frame, columns=self.df.columns.tolist(), show='headings', yscrollcommand=self.tree_scroll_y.set, xscrollcommand=self.tree_scroll_x.set)
        self.tree_scroll_y.config(command=self.tree.yview)
        self.tree_scroll_x.config(command=self.tree.xview)
        
        for col in self.df.columns:
            self.tree.heading(col, text=col, command=lambda _col=col: self.column_action(_col))
            self.tree.column(col, width=100)

        for row in self.df.itertuples(index=False):
            self.tree.insert('', 'end', values=row)
        
        self.tree.pack(fill='both', expand=True)

    def update_comboboxes(self):
        columns = self.df.columns.tolist()
        rows = self.df.index.tolist()
        values = [f"{col}{row+1}" for col in columns for row in rows]
        values = [i for i in range(len(self.df["ID"]))]
        self.start_combobox['values'] = values
        self.end_combobox['values'] = values

    def run_action(self,start = 1,end = 3,export = True):
        export = self.save_file_var.get()
        print(export)
        print(self.search_content_entry.get(),"\n",self.start_combobox.get(),self.end_combobox.get())
        if self.start_combobox.get():
            start = int(self.start_combobox.get())
        if self.end_combobox.get():
            end = int(self.end_combobox.get())
        print(start, "\t", end)
        from datetime import datetime
        self.show_waiting_message()
        all_result = {}
        for i, row in self.df.iterrows():
            try:
                if i >= start-1 and i <= end:
                    department = row['ID']
                    link = row['Website']
                    res = CustomSearch.make_querry(content = self.search_content_entry.get(),
                                                site = link)
                    all_result[department] = res
                    if export:
                        CustomSearch.export_csv(name = department,data = res)

            except Exception as e:
                with open("log_error.txt","a") as file:
                    file.write(f"{datetime.now()}: {e} \n")
        print(all_result)
        self.hide_waiting_message()
        messagebox.showinfo("status","crawl success")
        return all_result   
        # column_data = self.df[column_name].dropna().tolist() # Get column data and drop NaN values    
        # # print(self.selected_column_data,"\n")
        # for site in column_data:
        #     res_js = CustomSearch.make_querry(self.search_content_entry.get(),site)
        #     for i in range(len(res_js["items"])):
        #         title = res_js["items"][i]["title"]
        #         link = res_js["items"][i]["link"]
        #         self.selected_column_data[column_name] = [title,link]  # Store column data in dictionary
        # # print(self.selected_column_data[column_name])   
             


    def save_content(self):
        if not self.selected_column_data:
            messagebox.showwarning("No Data", "No column data selected to save.")
            return
        
        # file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv")])
        file_path = 'link_web.txt'
        if file_path:
            # Save column data to the selected file
            with open(file_path, 'w', encoding='utf-8') as file:
                if file_path.endswith('.txt'):
                    for col_name, col_data in self.selected_column_data.items():
                        file.write(f"{col_name}:\n")
                        for item in col_data:
                            file.write(f"{item}\n")
                        file.write("\n")
                elif file_path.endswith('.csv'):
                    for col_name, col_data in self.selected_column_data.items():
                        file.write(f"{col_name},\n")
                        pd.Series(col_data).to_csv(file, index=False, header=False)
                        file.write("\n")
            
            messagebox.showinfo("Success", f"Selected column data saved to {file_path}")
            self.selected_column_data.clear()  # Clear the dictionary after saving

if __name__ == "__main__":
    root = tk.Tk()
    app = ExcelApp(root)
    root.mainloop()
