# -- Chuong trinh lay tu trang web https://dev.events/it de craw ---
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import json
import pyodbc
from datetime import datetime

def crawl_web1(max_page):
    start_page = 1
    name_temp = []
    place_temp = []
    time_temp = []
    while start_page <= max_page:
        response = requests.get(f'https://dev.events/it?page={start_page}')
        #Loc tu cac thanh tag
        if response.status_code == 200:
            print('start loading ...')
            soup = BeautifulSoup(response.text, 'html.parser')
            conferences = soup.find_all('div', attrs={'class': 'row columns is-mobile'})
            for conference in conferences:
                name = conference.find('h2')
                if name is not None:
                    name = name.get_text().strip() #Ten hoi nghi
                    name_temp.append(name)

                places = conference.find_all('span') #Dia diem
                for place in places:
                    place = place.find('a')
                    if place is not None:
                        place = place.get_text().strip()
                        place_temp.append(place)

                time = conference.find('time', class_='has-text-weight-bold is-size-7-mobile has-text-grey-dark')
                if time is not None: #Thoi gian
                    full_time = time.get_text()
                    span_text = time.find('span').get_text()
                    time = full_time.replace(span_text, '').strip()
                    time_org = time.split('-')[0].strip()
                    time_obj = datetime.strptime(time_org + " 2024", "%b %d %Y")
                    formatted_time = time_obj.strftime("%m/%d/%y")
                    time_temp.append(formatted_time)
            print("...")
        else:
            print("Không thể truy cập trang web. Mã lỗi:", response.status_code)

        start_page += 1
    # Tạo dataframe
    df = pd.DataFrame(list(zip(name_temp, place_temp, time_temp)), columns=['Conference', 'Place', 'Time'])
    return df