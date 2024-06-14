# -- Update from Dataframe to MS SQL --
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import json
import pyodbc
from datetime import datetime
import Web1_Crawl

def convert_df_to_json(df, json_file):
    result = df.to_json(orient='records')

    parsed = json.loads(result)

    with open(json_file, 'w') as f:
        json.dump(parsed, f, indent=4)


def Json_to_MSSQL(json_file):
    # #---------------Thêm data từ file JSON vào DB---------------------------------
    data = pd.read_json(json_file)
    server = r'LAPTOP-073BBS08\SQLEXPRESS' #thêm r để thành raw string do co \S
    database = 'ITconferences' #ten database
    username = ''
    password = ''
    connector_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes'


    # Thiết lập kết nối đến SQL Server
    conn = pyodbc.connect(connector_string)

    # Tạo cursor object
    cursor = conn.cursor()

    # Xóa các dữ liệu các hội nghị cũ
    cursor.execute("TRUNCATE TABLE Conferences")

    # Chèn dữ liệu vào bảng
    for index, row in data.iterrows():
        cursor.execute("INSERT INTO Conferences (ID_Conference, Name_Conference, Place, Time) VALUES (?, ?, ?, ?)",
                       row['ID_Conference'], row['Conference'], row['Place'], row['Time'])
        conn.commit()

    # Đóng kết nối
    cursor.close()
    conn.close()