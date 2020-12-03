from PyQt5 import QtCore, QtGui, QtWidgets
import usb.util

from EISwindow import *
from CVwindow import *
from AMPEROwindow import *
from CVzFalaKwadratwindow import *
from LSVwindow import *
from CHRONOwindow import *


# urzadzenie
VID = 0x04D8
PID = 0x003F
device = hid.HidDeviceFilter(vendor_id=0x04D8, product_id=0x003F).get_devices()[0]


class Ui_MicroPot(object):
    def setupUi(self, MicroPot):
        MicroPot.setObjectName("MicroPot")
        MicroPot.resize(600, 800)
        MicroPot.setMinimumSize(QtCore.QSize(600, 800))
        MicroPot.setMaximumSize(QtCore.QSize(600, 800))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MicroPot.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MicroPot)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButtonEIS = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonEIS.setGeometry(QtCore.QRect(20, 270, 271, 75))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButtonEIS.setFont(font)
        self.pushButtonEIS.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButtonEIS.setObjectName("pushButtonEIS")
        self.calendarWidget_CALENDER = QtWidgets.QCalendarWidget(self.centralwidget)
        self.calendarWidget_CALENDER.setGeometry(QtCore.QRect(21, 20, 551, 236))
        self.calendarWidget_CALENDER.setObjectName("calendarWidget_CALENDER")
        self.pushButtonCV = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonCV.setGeometry(QtCore.QRect(300, 270, 271, 75))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButtonCV.setFont(font)
        self.pushButtonCV.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButtonCV.setObjectName("pushButtonCV")
        self.pushButtonQUIT = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonQUIT.setGeometry(QtCore.QRect(420, 630, 150, 100))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.pushButtonQUIT.setFont(font)
        self.pushButtonQUIT.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButtonQUIT.setObjectName("pushButtonQUIT")
        self.pushButton_connect = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_connect.setGeometry(QtCore.QRect(10, 630, 191, 61))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.pushButton_connect.setFont(font)
        self.pushButton_connect.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_connect.setObjectName("pushButton_connect")
        self.progressBar_connect = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar_connect.setGeometry(QtCore.QRect(10, 700, 191, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.progressBar_connect.setFont(font)
        self.progressBar_connect.setProperty("value", 0)
        self.progressBar_connect.setObjectName("progressBar_connect")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(500, 740, 47, 13))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(550, 740, 47, 13))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(560, 740, 47, 13))
        self.label_3.setObjectName("label_3")
        self.pushButtonCA = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonCA.setGeometry(QtCore.QRect(20, 350, 271, 75))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButtonCA.setFont(font)
        self.pushButtonCA.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButtonCA.setObjectName("pushButtonCA")
        self.pushButtonAMPERO = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonAMPERO.setGeometry(QtCore.QRect(20, 430, 271, 75))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButtonAMPERO.setFont(font)
        self.pushButtonAMPERO.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButtonAMPERO.setObjectName("pushButtonAMPERO")
        self.pushButtonLSV = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonLSV.setGeometry(QtCore.QRect(300, 350, 271, 75))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButtonLSV.setFont(font)
        self.pushButtonLSV.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButtonLSV.setObjectName("pushButtonLSV")
        self.pushButtonSWV = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSWV.setGeometry(QtCore.QRect(300, 430, 271, 75))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButtonSWV.setFont(font)
        self.pushButtonSWV.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButtonSWV.setObjectName("pushButtonSWV")
        MicroPot.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MicroPot)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 26))
        self.menubar.setObjectName("menubar")
        MicroPot.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MicroPot)
        self.statusbar.setObjectName("statusbar")
        MicroPot.setStatusBar(self.statusbar)

        self.retranslateUi(MicroPot)
        self.pushButtonQUIT.clicked.connect(MicroPot.close)
        self.pushButtonEIS.clicked.connect(self.EIS)
        self.pushButtonCV.clicked.connect(self.CV)
        self.pushButtonAMPERO.clicked.connect(self.AMPERO)
        self.pushButtonCA.clicked.connect(self.CA)
        self.pushButtonLSV.clicked.connect(self.LSV)
        self.pushButtonSWV.clicked.connect(self.SWV)
        self.pushButton_connect.clicked.connect(self.potentiostat_progress_click)
        QtCore.QMetaObject.connectSlotsByName(MicroPot)


    def potentiostat_progress_click(self):
        dev = usb.core.find(idVendor=VID, idProduct=PID)
        if not dev:
            print("Nie znaleziono urzadzenia")
            self.pushButton_connect.setText("Can't connect")
        else:
            self.completed = 0
            while self.completed <100:
                self.completed += 0.000025
                self.progressBar_connect.setValue(self.completed)

            print("Znaleziono urzadzenie")
            self.pushButton_connect.setText("Connected")



    def EIS(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_EIS()
        hid = Potecjostat(VID, PID)
        self.ui.setupEIS(self.window, hid)
        hid.RegisterReceiveCallbackProcedure(ui.ui.Run)
        ui.ui.RegisterRemoteProcedureForSendFrameToHid(hid.Change_Command)
        hid.Open()
        self.window.show()


    def CV(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_CV()
        hid = Potecjostat(VID, PID)
        self.ui.setupCV(self.window, hid)
        hid.RegisterReceiveCallbackProcedure(ui.ui.Run)
        ui.ui.RegisterRemoteProcedureForSendFrameToHid(hid.Change_Command)
        hid.Open()
        self.window.show()

    def AMPERO(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_AMPERO()
        hid = Potecjostat(VID, PID)
        self.ui.setupAMPERO(self.window, hid)
        hid.RegisterReceiveCallbackProcedure(ui.ui.Run)
        ui.ui.RegisterRemoteProcedureForSendFrameToHid(hid.Change_Command)
        hid.Open()
        self.window.show()

    def CA(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_CA()
        hid = Potecjostat(VID, PID)
        self.ui.setupCA(self.window, hid)
        hid.RegisterReceiveCallbackProcedure(ui.ui.Run)
        ui.ui.RegisterRemoteProcedureForSendFrameToHid(hid.Change_Command)
        hid.Open()
        self.window.show()

    def SWV(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_SWV()
        hid = Potecjostat(VID, PID)
        self.ui.setupSWV(self.window, hid)
        hid.RegisterReceiveCallbackProcedure(ui.ui.Run)
        ui.ui.RegisterRemoteProcedureForSendFrameToHid(hid.Change_Command)
        hid.Open()
        self.window.show()

    def LSV(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_LSV()
        hid = Potecjostat(VID, PID)
        self.ui.setupLSV(self.window, hid)
        hid.RegisterReceiveCallbackProcedure(ui.ui.Run)
        ui.ui.RegisterRemoteProcedureForSendFrameToHid(hid.Change_Command)
        hid.Open()
        self.window.show()



    def retranslateUi(self, MicroPot):
        _translate = QtCore.QCoreApplication.translate
        MicroPot.setWindowTitle(_translate("MicroPot", "MicroPot"))
        self.pushButtonEIS.setText(_translate("MicroPot", "Electrochemical Impedance \n"
                                                                    "Spectroscopy [ EIS ] "))
        self.pushButtonCV.setText(_translate("MicroPot", "Cyclic Voltammetry [ CV ]"))
        self.pushButtonQUIT.setText(_translate("MicroPot", "Quit"))
        self.pushButton_connect.setText(_translate("MicroPot", "Connect"))
        self.label.setText(_translate("MicroPot", "Version:"))
        self.label_2.setText(_translate("MicroPot", "0"))
        self.label_3.setText(_translate("MicroPot", "1"))
        self.pushButtonCA.setText(_translate("MicroPot", "Chronoamperometry [ CA ] "))
        self.pushButtonAMPERO.setText(_translate("MicroPot", "Amperometry [ AA ] "))
        self.pushButtonLSV.setText(_translate("MicroPot", "Linear Sweep \n"
                                                                    "Voltammetry [ LSV ]"))
        self.pushButtonSWV.setText(_translate("MicroPot", "Square Wave \n"
                                                                    "Voltammetry [ SWV ]"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MicroPot = QtWidgets.QMainWindow()
    ui = Ui_MicroPot()
    ui.setupUi(MicroPot)
    MicroPot.show()
    sys.exit(app.exec_())
