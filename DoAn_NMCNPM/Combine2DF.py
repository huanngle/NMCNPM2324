from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import json
import pyodbc
from datetime import datetime
import Web2_Crawl as w2
import Web1_Crawl as w1
import Update_SQL as up
ID_conference = []

def combine_df(df_web1, df_web2):
    df_combine = pd.concat([df_web1, df_web2])

    # Tạo cột ID
    for i in range(1, len(df_combine) + 1):
        ID_num = f"IDC{i:03}"
        ID_conference.append(ID_num)

    df_combine.insert(0, 'ID_Conference', ID_conference)

    return df_combine
