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

        
        

        # Add a button to load Excel file
        self.load_button = tk.Button(top_frame, text="Load Excel File", command=self.load_excel)
        self.load_button.pack(side='left', padx=5)

        # Add a button to save content with styling
        self.save_button = tk.Button(top_frame, text="Lưu", command=self.save_content, 
                                     font=('Arial', 12, 'bold'), bg='blue', fg='white', width=15)
        

        # Add an Entry to display and edit search content
        self.search_content_var = tk.StringVar(value="Tuyển dụng")
        self.search_content_entry = tk.Entry(top_frame, textvariable=self.search_content_var, width=20)
        self.search_content_entry.pack(side='right', padx=5)

        # Add a label for the search content
        self.save_button.pack(side='right', padx=5)
        search_label = tk.Label(top_frame, text="Nội dung tìm kiếm")
        search_label.pack(side='right', padx=5)

        # Create a Combobox to select sheets
        self.sheet_selector = ttk.Combobox(top_frame)
        self.sheet_selector.pack(side='right', padx=5)
        self.sheet_selector.bind("<<ComboboxSelected>>", self.display_sheet)

        # Add a label for the sheet selection
        sheet_label = tk.Label(top_frame, text="Sheet:")
        sheet_label.pack(side='right', padx=5)

        # Frame to hold the column buttons and Treeview
        self.table_frame = tk.Frame(root)
        self.table_frame.pack(expand=1, fill='both')

        # Add an instruction label
        self.instruction_label = tk.Label(self.table_frame, text="Vui lòng chọn cột chứa link",font=('Arial',12,'bold'),fg= 'red')
        self.instruction_label.pack(side='top', pady=5)

        self.column_buttons_frame = tk.Frame(self.table_frame)
        self.column_buttons_frame.pack(side='top', fill='x')

        self.status_label = tk.Label(root, text="", fg="red")
        self.status_label.pack(pady=20)

        self.tree_frame = tk.Frame(self.table_frame)
        self.tree_frame.pack(expand=1, fill='both')

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

        # Get the first ten rows of the sheet
        first_ten_rows = self.df.head(10)

        # Clear previous content
        for widget in self.column_buttons_frame.winfo_children():
            widget.destroy()

        if self.tree:
            self.tree.destroy()

        # Create a Treeview widget to display the data
        self.tree = ttk.Treeview(self.tree_frame, columns=list(first_ten_rows.columns), show='headings',
                                 yscrollcommand=self.tree_scroll_y.set,
                                 xscrollcommand=self.tree_scroll_x.set)
        self.tree.pack(expand=1, fill='both')

        # Attach scrollbars to the treeview
        self.tree_scroll_y.config(command=self.tree.yview)
        self.tree_scroll_x.config(command=self.tree.xview)

        # Set up the treeview columns and create buttons for column names
        for col in first_ten_rows.columns:
            self.tree.heading(col, text=col)
            col_width = max(first_ten_rows[col].astype(str).map(len).max(), len(col)) * 10
            self.tree.column(col, anchor='center', width=col_width)
            btn = tk.Button(self.column_buttons_frame, text=col, command=lambda c=col: self.column_action(c), width=col_width // 10)
            btn.pack(side='left')

        # Insert the data into the treeview
        for row in first_ten_rows.itertuples(index=False):
            self.tree.insert("", "end", values=row)
    def show_waiting_message(self):
        self.status_label.config(text="Processing, please wait...")
        self.root.update_idletasks()
    def hide_waiting_message(self):
        self.status_label.config(text="")
        self.root.update_idletasks()

    def column_action(self, column_name):
        self.show_waiting_message()
        column_data = self.df[column_name].dropna().tolist()  # Get column data and drop NaN values
    
        print(self.selected_column_data,"\n")
        for site in column_data:
            res_js = CustomSearch.make_querry(self.search_content_entry.get(),site)
            for i in range(len(res_js["items"])):
                title = res_js["items"][i]["title"]
                link = res_js["items"][i]["link"]
                self.selected_column_data[column_name] = [title,link]  # Store column data in dictionary
        print(self.selected_column_data[column_name])        
        self.hide_waiting_message()
        messagebox.showinfo("Column Selected", f"Column '{column_name}' has been selected for saving.")

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
