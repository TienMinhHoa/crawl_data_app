import pymysql
import datetime
import collections
import pandas as pd
from tqdm import tqdm


class DatabaseConnector:
    def __init__(self,
                 server,
                 database,
                 username,
                 password,
                 port):
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.port = port
        self.connection = None

    def connect(self):
        try:
            self.connection = pymysql.connect(
                host=self.server,
                port=self.port,
                user=self.username,
                password=self.password,
                database=self.database,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            print("Connection established successfully.")
        except pymysql.MySQLError as e:
            print("Error while connecting to MySQL:", e)

    def execute_query(self, query, params=None):
        if self.connection is None:
            print("No connection established. Please connect first.")
            return

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
            self.connection.commit()
            print("Query executed successfully.")
        except pymysql.MySQLError as e:
            print("Error while executing the query:", e)

    def insert_data(self, table_name, **kwargs):
        if not kwargs:
            print("No data provided for insertion.")
            return

        columns = ', '.join(kwargs.keys())
        placeholders = ', '.join(['%s'] * len(kwargs))
        values = tuple(kwargs.values())

        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        try:
            self.execute_query(query, values)
            print(f"Data inserted into table '{table_name}'.")
        except pymysql.MySQLError as e:
            print("Error while inserting data:", e)

    def fetch_all(self, query, params=None):
        if self.connection is None:
            print("No connection established. Please connect first.")
            return None

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                results = cursor.fetchall()
            return results
        except pymysql.MySQLError as e:
            print("Error while fetching data:", e)
            return None

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Connection closed.")
