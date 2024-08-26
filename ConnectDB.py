import pyodbc
import collections
import pandas as pd
from tqdm import tqdm
class DatabaseConnector:
    def __init__(self, server, database, username=None, password=None, use_windows_auth=True):
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.use_windows_auth = use_windows_auth
        self.connection = None

    def connect(self):
        try:
            if self.use_windows_auth:
                connection_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};Trusted_Connection=yes;"
            else:
                connection_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password};"

            self.connection = pyodbc.connect(connection_str)
            print("Connection established successfully.")
        except pyodbc.Error as e:
            print("Error while connecting to SQL Server:", e)

    def execute_query(self, query, params=None):
        if self.connection is None:
            print("No connection established. Please connect first.")
            return

        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            print("Query executed successfully.")
        except pyodbc.Error as e:
            print("Error while executing the query:", e)
    def insert_data(self, table_name, **kwargs):
        if not kwargs:
            print("No data provided for insertion.")
            return

        columns = ', '.join(kwargs.keys())
        placeholders = ', '.join('?' for _ in kwargs)
        values = tuple(kwargs.values())

        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        try:
            self.execute_query(query, values)
            print(f"Data inserted into table '{table_name}'.")
        except pyodbc.Error as e:
            print("Error while inserting data:", e)

    def fetch_all(self, query, params=None):
        if self.connection is None:
            print("No connection established. Please connect first.")
            return None

        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            results = cursor.fetchall()
            return results
        except pyodbc.Error as e:
            print("Error while fetching data:", e)
            return None

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Connection closed.")

# Sử dụng lớp DatabaseConnector
# if __name__ == "__main__":
#     db = DatabaseConnector(server="Admin", database="CrawlDB",username="sa",password="utequyen2372004",use_windows_auth=False)
#     db.connect()

#     # Kiểm tra các bảng trong cơ sở dữ liệu
#     tables = db.fetch_all("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE';")
#     if tables:
#         print("Tables in the database:")
#         for table in tables:
#             print(table.TABLE_NAME)

#     # Thêm một dòng dữ liệu vào bảng 'domain'
#     # insert_query = "INSERT INTO domain (name_id, url_domain) VALUES (?, ?)"
#     # db.execute_query(insert_query, ('example_id', 'http://example.com'))
#     my_dict = collections.defaultdict(list)
#     df = pd.read_excel("backend_data/data.xlsx")
#     for i,row in tqdm(df.iterrows()):
#         db.insert_data("Domains",id = row['ID'],name_id = row['NAME'],url_domain = row['Website'])
#     # print(df)
#     # db.insert_data("Domains",id = 91003,name_id = "Bo ngoai giao",url_domain="https://mofa.gov.vn/")

#     # Ngắt kết nối
#     db.disconnect()
