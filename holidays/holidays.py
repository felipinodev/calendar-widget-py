import json
import os
import hashlib
import requests
from datetime import timedelta
from dateutil.easter import easter
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QTextCharFormat, QColor

def set_holidays(calendar, holidays):
    text_format = QTextCharFormat()
    text_format.setForeground(QColor("#FF4500"))
    
    for holiday_date, holiday_title in holidays:
        text_format.setToolTip(holiday_title)
        calendar.setDateTextFormat(holiday_date, text_format)

def get_holidays():
    current_year = QDate.currentDate().year()
    start_year = current_year - 10
    end_year = current_year + 10
    json_file_path = "./data/holidays.json"

    url_Hodilays_db = "https://raw.githubusercontent.com/felipinodev/calendar-widget-py/refs/heads/master/data/holidays_db.json"
    responseWeb = requests.get(url_Hodilays_db)

    # Compare hash
    def get_file_hash(file_path):
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except FileNotFoundError:
            return None

    if responseWeb.status_code == 200:
        local_hash = None
        if os.path.exists(json_file_path):
            local_hash = get_file_hash(json_file_path)

        web_hash = hashlib.md5(responseWeb.content).hexdigest()

        if local_hash != web_hash:

            # Different files download
            with open(json_file_path, "wb") as file:
                file.write(responseWeb.content)
    else:
        print(f"Error accessing the URL. Status Code: {responseWeb.status_code}")


    with open(json_file_path, "r") as file:
        holidays_data = json.load(file)

    holidays = []

    for holiday_data in holidays_data["holiday_static"]:
        month = holiday_data["month"]
        day = holiday_data["day"]
        title = holiday_data["title"].encode("latin-1").decode()

        for year in range(start_year, end_year + 1):
            holiday_date = QDate(year, month, day)
            holidays.append((holiday_date, title))

    for holiday_data in holidays_data["holiday_dinamic"]:
        month = holiday_data["month"]
        day = holiday_data["day"]
        year = holiday_data["year"]
        title = holiday_data["title"].encode("latin-1").decode()

        holiday_date = QDate(year, month, day)
        holidays.append((holiday_date, title))


    return holidays
