from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy, QSizeGrip, QMenu
from PyQt5.QtCore import Qt, QPoint, QEvent
from PyQt5.QtGui import QColor, QTextCharFormat, QIcon
import sys
from interface.interface import Ui_MainWindow
from holidays.holidays import set_holidays, get_holidays
import json
import time
import datetime
import threading

def save_window_position(x, y):
    try:
        with open('./data/window_position.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    if 'x' not in data or 'y' not in data:
        data['x'] = x
        data['y'] = y
        with open('./data/window_position.json', 'w') as file:
            json.dump(data, file)
    else:
        x = data['x']
        y = data['y']

    return x, y

def update_window_position(x, y):
    data = {'x': x, 'y': y}
    with open('./data/window_position.json', 'w') as file:
        json.dump(data, file)

def save_window_size(width, height):
    try:
        with open('data/window_size.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    if 'width' not in data or 'height' not in data:
        data['width'] = width
        data['height'] = height
        with open('data/window_size.json', 'w') as file:
            json.dump(data, file)
    else:
        width = data['width']
        height = data['height']

    return width, height

def update_window_size(width, height):
    data = {'width': width, 'height': height}
    with open('./data/window_size.json', 'w') as file:
        json.dump(data, file)

class DesktopWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnBottomHint | Qt.Tool )
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.draggable = True
        self.offset = QPoint()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        size_grip_bottom_right = QSizeGrip(self.ui.centralwidget)
        layout = self.ui.verticalLayout
        layout.addWidget(size_grip_bottom_right, 0, Qt.AlignBottom | Qt.AlignRight)

        x, y = save_window_position(self.x(), self.y())
        self.move(x, y)

        width, height = save_window_size(self.width(), self.height())
        self.resize(width, height)

    def change_weekend_colors(self):
        weekend_format = QTextCharFormat()
        weekend_format.setForeground(QColor("#fff"))

        saturday = Qt.Saturday
        sunday = Qt.Sunday

        self.ui.calendarWidget.setWeekdayTextFormat(saturday, weekend_format)
        self.ui.calendarWidget.setWeekdayTextFormat(sunday, weekend_format)

    def change_current_day_color(self):
        current_day_format = QTextCharFormat()
        current_day_format.setBackground(QColor("#f00"))
        current_day_format.setForeground(QColor("#fff"))

        old_day_format = QTextCharFormat()
        old_day_format.clearBackground()
        old_day_format.clearForeground()

        current_date = datetime.datetime.now().date()
        self.ui.calendarWidget.setDateTextFormat(current_date, current_day_format)

        while True:
            new_current_date = datetime.datetime.now().date()
            if current_date != new_current_date:
                self.ui.calendarWidget.setDateTextFormat(current_date, old_day_format)
                self.change_current_day_color()

            time.sleep(1)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.draggable:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.draggable:
            if self.offset:
                self.move(self.pos() + event.pos() - self.offset)
                update_window_position(self.x(), self.y())
                update_window_size(self.width(), self.height())

    def eventFilter(self, obj, event):
        if obj == self and event.type() == QEvent.Resize:
            self.offset = QPoint()
            return True
        return super().eventFilter(obj, event)
    
    def contextMenuEvent(self, event):
        menu = QMenu(self)
        menu.setStyleSheet("QMenu { background-color: #333; color: #fff }")
        
        exit_action = menu.addAction("Fechar")
        
        def exit_application():
            QApplication.quit()

        exit_action.triggered.connect(exit_application)

        menu.exec_(event.globalPos())

def main():
    app = QApplication(sys.argv)
    app_icon = QIcon("./assets/icon.ico")
    app.setWindowIcon(app_icon)
    widget = DesktopWidget()
    widget.installEventFilter(widget)
    set_holidays(widget.ui.calendarWidget, get_holidays())
    widget.change_weekend_colors()
    thread = threading.Thread(target=widget.change_current_day_color)
    thread.daemon = True
    thread.start()
    widget.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
