from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 300)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.calendarWidget = QtWidgets.QCalendarWidget(self.centralwidget)
        self.calendarWidget.setTabletTracking(False)
        self.calendarWidget.setStyleSheet("QCalendarWidget QWidget { background-color: #111; color: #fff; alternate-background-color: #5b5b5b; selection-background-color: #0ff; font: 10pt \"Square721 BT\"; text-transform: uppercase; } QCalendarWidget QToolButton { font-size: 18px; } QCalendarWidget QAbstractItemView:disabled  { color: #808080; } #qt_calendar_prevmonth { icon-size: 20px; qproperty-icon: url('./assets/prevmonth.svg'); margin:5px; } #qt_calendar_nextmonth { icon-size: 20px; qproperty-icon: url('./assets/nextmonth.svg'); margin:5px; }")
        self.calendarWidget.setGridVisible(True)
        self.calendarWidget.setSelectionMode(QtWidgets.QCalendarWidget.SingleSelection)
        self.calendarWidget.setHorizontalHeaderFormat(QtWidgets.QCalendarWidget.ShortDayNames)
        self.calendarWidget.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.NoVerticalHeader)
        self.calendarWidget.setNavigationBarVisible(True)
        self.calendarWidget.setDateEditEnabled(True)
        self.calendarWidget.setObjectName("calendarWidget")

        opacity_effect = QtWidgets.QGraphicsOpacityEffect()
        opacity_effect.setOpacity(0.9)
        self.calendarWidget.setGraphicsEffect(opacity_effect)

        self.verticalLayout.addWidget(self.calendarWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
