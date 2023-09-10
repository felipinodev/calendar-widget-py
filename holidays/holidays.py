import json
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

    for holiday_data in holidays_data["easter_holiday_dymanic"]:
        title = holiday_data["title"].encode("latin-1").decode()
        days_relative_to_easter = holiday_data["days_relative_to_easter"]

        for year in range(start_year, end_year + 1):            
            holiday_date = easter(year) - timedelta(days=int(days_relative_to_easter))
            holidays.append((holiday_date, title))

    return holidays
