#--Craw du lieu tu trang web https://www.techrepublic.com/article/top-tech-conferences-events/
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import json
import pyodbc
from datetime import datetime
import re
def crawl_web2():
    name_temp = []
    place_temp = []
    time_temp = []

    response = requests.get('https://www.techrepublic.com/article/top-tech-conferences-events/')
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        alltables = soup.find_all('tbody',class_ = 'row-hover')
        for table in alltables:
            conferences = table.find_all('td', class_ = 'column-1')
            for conference in conferences:
                time = conference.find('strong') #Thoi Gian
                if time is not None:
                    time = time.get_text().strip()
                    formatted_time = convert_date_format(time)
                    time_temp.append(formatted_time)

                name = conference.find('a') # Ten hoi nghi
                if name is not None:
                    name = name.get_text().strip()
                    name_temp.append(name)

                place = conference.get_text().strip() #Dia diem
                place = extract_location(place)
                place_temp.append(place)

    else:
        print("Không thể truy cập trang web. Mã lỗi:", response.status_code)

    df = pd.DataFrame(list(zip(name_temp, place_temp, time_temp)), columns=['Conference', 'Place', 'Time'])
    print('Finish!')
    return df

#Hàm Loc va dinh dang lai du lieu ngày
def convert_date_format(date_string, year="2024"):
    cleaned_string = re.sub(r'[\.:]', '', date_string)
    cleaned_string = re.sub(r'\bSept\b', 'Sep', cleaned_string) #Thang 9 co dinh dang o web khac voi mong muon
    match = re.search(r'(\w+)\s+(\d+)(?:-\d+)?', cleaned_string)
    if match:
        month_name = ''.join([char for char in match.group(1) if char.isalpha()])
        day = match.group(2)
        try:
            try:
                date_parsed = datetime.strptime(f"{month_name} {day} {year}", "%b %d %Y")
            except ValueError:
                # Do ten cua tháng khong day du, xet truong hop viet tat khác
                date_parsed = datetime.strptime(f"{month_name} {day} {year}", "%B %d %Y")
            # Return formatted date string
            return date_parsed.strftime("%m/%d/%Y")
        except ValueError:
            # trong Truong hop error tra ve NULL
            return None
    else:
        return None

# Hàm Loc va tach, dinh dang lai du lieu địa điểm
def extract_location(text):
    location_pattern = re.compile(r'\bin\b\s+([\w\s,]+)')
    match = location_pattern.search(text)
    if match:
        location = re.sub(r'\s*\[.*?\]$', '', match.group(1).strip())
        return location
    else:
        return None
