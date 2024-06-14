from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import json
import pyodbc
from datetime import datetime
import Update_SQL
import Web1_Crawl as w1
import Web2_Crawl as w2
import Web_create as web
import Combine2DF

def main():
    server = 'LAPTOP-073BBS08\\SQLEXPRESS' #Dien ten server, Server dekstop khong can tao mat khau
    database = 'ITconferences' #Ten cua database
    no_page_crawled_web1 = 3 #số lượng page của web1 sẽ craw
    json_file = 'Output.json'

    # craw từ 2 web và lọc, tao thanh dataframe
    df1 = w1.crawl_web1(no_page_crawled_web1)
    df2 = w2.crawl_web2()
    df = Combine2DF.combine_df(df1,df2)

    #Tạo file JSon de quan ly
    Update_SQL.convert_df_to_json(df, json_file)

    #Update vao database
    Update_SQL.Json_to_MSSQL(json_file)

    #Khoi chay trinh duyet
    web.start_the_web()

if __name__ == "__main__":
    main()



