from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QTextEdit, QPushButton, QVBoxLayout, QApplication, QWidget, QFileDialog, QHBoxLayout)
import sys
import os
import ctypes
import struct
from struct import *
import numpy as np
from HidDevice import Potecjostat
import time
import pywinusb.hid as hid
import math

VID = 0x04D8
PID = 0x003F
device = hid.HidDeviceFilter(vendor_id=0x04D8, product_id=0x003F).get_devices()[0]


class Ui_CA(object):
    def __init__(self):
        self.Data = None
        self.Frame_bytes_series = []
        self.Frame_converted_series = []
        self.Plot_Xseries = []
        self.Plot_Yseries = []
        self.RemoteProcedureForSendFrameToHid = None
        self.__isPlotStart = False

    def RegisterRemoteProcedureForSendFrameToHid(self, remoteHidProc):
        self.RemoteProcedureForSendFrameToHid = remoteHidProc

    def CreateAndSendFrame(self):
        try:
            frame = bytearray()

            OneByteAddStr = self.label_2.text()
            OneByteAddInt = int(OneByteAddStr)
            OneByteAddBytes = OneByteAddInt.to_bytes(1, 'big')
            frame += bytes(OneByteAddBytes)

            SecByteAddStr = self.label_3.text()
            SecByteAddInt = int(SecByteAddStr)
            SecByteAddBytes = SecByteAddInt.to_bytes(1, 'big')
            frame += bytes(SecByteAddBytes)

            RampStartStr = self.Propert_.text()
            RampStartFloat = int(RampStartStr)
            RampStartBytes = bytearray(struct.pack("I", RampStartFloat))
            frame += bytes(RampStartBytes)

            RampStopStr = self.Propert_1.text()
            RampStopFloat = int(RampStopStr)
            RampStopBytes = bytearray(struct.pack("I", RampStopFloat))
            frame += bytes(RampStopBytes)

            VZeroStartStr = self.Propert_2.text()
            VZeroStartFloat = int(VZeroStartStr)
            VZeroStartBytes = bytearray(struct.pack("I", VZeroStartFloat))
            frame += bytes(VZeroStartBytes)

            VZeroStopStr = self.Propert_3.text()
            VZeroStopFloat = int(VZeroStopStr)
            VZeroStopBytes = bytearray(struct.pack("I", VZeroStopFloat))
            frame += bytes(VZeroStopBytes)

            StepNumbStr = self.Propert_4.text()
            StepNumbInt = int(StepNumbStr)
            StepNumbBytes = bytearray(struct.pack("I", StepNumbInt))
            frame += bytes(StepNumbBytes)



        except:
            ctypes.windll.user32.MessageBoxW(0, "Errors in properties data. ", "Eroor", 0)

        self.RemoteProcedureForSendFrameToHid(frame)

    def AddDataToLists(self, DataStr):
        self.Frame_bytes_series.append(DataStr)
        print(DataStr)

        [Pierwsza] = struct.unpack('I', bytes(self.Data[0:4]))
        [Druga] = struct.unpack('f', bytes(self.Data[4:8]))
        [Trzecia] = struct.unpack('I', bytes(self.Data[8:12]))
        [Czwarta] = struct.unpack('I', bytes(self.Data[12:16]))
        [Piata] = struct.unpack('I', bytes(self.Data[16:20]))

        str = "{:.2f};{:.2f};{:.2f};{:.2f};{:.2f}".format(Pierwsza, Druga, Trzecia, Czwarta,
                                                          Piata)
        self.Frame_converted_series.append(str)
        print(str)

        self.Plot_Xseries.append(Pierwsza)
        self.Plot_Yseries.append(Druga)

        if self.__isPlotStart:
            self.plot_graph()

    def setupCA(self, CA, hid):
        def CloseLocalWindow():
            hid.Close()
            self.Frame_bytes_series.clear()
            self.Frame_converted_series.clear()
            CA.close()

        CA.setObjectName("CA")
        CA.resize(1200, 850)
        CA.setMinimumSize(QtCore.QSize(1200, 850))
        CA.setMaximumSize(QtCore.QSize(1200, 850))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        CA.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(CA)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBoxPROPERTIESv2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxPROPERTIESv2.setGeometry(QtCore.QRect(10, 0, 371, 191))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.groupBoxPROPERTIESv2.setFont(font)
        self.groupBoxPROPERTIESv2.setObjectName("groupBoxPROPERTIESv2")
        self.label_SCAN_Ewe = QtWidgets.QLabel(self.groupBoxPROPERTIESv2)
        self.label_SCAN_Ewe.setGeometry(QtCore.QRect(10, 30, 131, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_SCAN_Ewe.setFont(font)
        self.label_SCAN_Ewe.setObjectName("label_SCAN_Ewe")
        self.Propert_ = QtWidgets.QLineEdit(self.groupBoxPROPERTIESv2)
        self.Propert_.setGeometry(QtCore.QRect(170, 30, 61, 22))
        self.Propert_.setObjectName("Propert_")
        self.label_V_vs_2 = QtWidgets.QLabel(self.groupBoxPROPERTIESv2)
        self.label_V_vs_2.setGeometry(QtCore.QRect(240, 30, 55, 21))
        self.label_V_vs_2.setObjectName("label_V_vs_2")
        self.label_REVERSE_SCAN = QtWidgets.QLabel(self.groupBoxPROPERTIESv2)
        self.label_REVERSE_SCAN.setGeometry(QtCore.QRect(10, 90, 101, 20))
        self.label_REVERSE_SCAN.setObjectName("label_REVERSE_SCAN")
        self.label_STEP_DURATION = QtWidgets.QLabel(self.groupBoxPROPERTIESv2)
        self.label_STEP_DURATION.setGeometry(QtCore.QRect(240, 150, 181, 21))
        self.label_STEP_DURATION.setObjectName("label_STEP_DURATION")
        self.label_TO_VERTEX_E1 = QtWidgets.QLabel(self.groupBoxPROPERTIESv2)
        self.label_TO_VERTEX_E1.setGeometry(QtCore.QRect(10, 60, 131, 20))
        self.label_TO_VERTEX_E1.setObjectName("label_TO_VERTEX_E1")
        self.label_REPEAT_nc = QtWidgets.QLabel(self.groupBoxPROPERTIESv2)
        self.label_REPEAT_nc.setGeometry(QtCore.QRect(10, 120, 151, 21))
        self.label_REPEAT_nc.setObjectName("label_REPEAT_nc")
        self.label_REPEAT_TIME = QtWidgets.QLabel(self.groupBoxPROPERTIESv2)
        self.label_REPEAT_TIME.setGeometry(QtCore.QRect(240, 120, 61, 21))
        self.label_REPEAT_TIME.setObjectName("label_REPEAT_TIME")
        self.label_OVER_LAST = QtWidgets.QLabel(self.groupBoxPROPERTIESv2)
        self.label_OVER_LAST.setGeometry(QtCore.QRect(10, 150, 141, 20))
        self.label_OVER_LAST.setObjectName("label_OVER_LAST")
        self.label_V_vs_4 = QtWidgets.QLabel(self.groupBoxPROPERTIESv2)
        self.label_V_vs_4.setGeometry(QtCore.QRect(240, 60, 55, 21))
        self.label_V_vs_4.setObjectName("label_V_vs_4")
        self.label_V_vs_3 = QtWidgets.QLabel(self.groupBoxPROPERTIESv2)
        self.label_V_vs_3.setGeometry(QtCore.QRect(240, 90, 55, 21))
        self.label_V_vs_3.setObjectName("label_V_vs_3")
        self.Propert_1 = QtWidgets.QLineEdit(self.groupBoxPROPERTIESv2)
        self.Propert_1.setGeometry(QtCore.QRect(170, 60, 61, 22))
        self.Propert_1.setObjectName("Propert_1")
        self.Propert_2 = QtWidgets.QLineEdit(self.groupBoxPROPERTIESv2)
        self.Propert_2.setGeometry(QtCore.QRect(170, 90, 61, 22))
        self.Propert_2.setObjectName("Propert_2")
        self.Propert_3 = QtWidgets.QLineEdit(self.groupBoxPROPERTIESv2)
        self.Propert_3.setGeometry(QtCore.QRect(170, 120, 61, 22))
        self.Propert_3.setObjectName("Propert_3")
        self.Propert_4 = QtWidgets.QLineEdit(self.groupBoxPROPERTIESv2)
        self.Propert_4.setGeometry(QtCore.QRect(170, 150, 61, 22))
        self.Propert_4.setObjectName("Propert_4")
        self.pushButton_SAVE = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_SAVE.setGeometry(QtCore.QRect(880, 690, 151, 81))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.pushButton_SAVE.setFont(font)
        self.pushButton_SAVE.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_SAVE.setObjectName("pushButton_SAVE")
        self.pushButton_QUIT = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_QUIT.setGeometry(QtCore.QRect(1040, 690, 151, 81))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.pushButton_QUIT.setFont(font)
        self.pushButton_QUIT.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_QUIT.setObjectName("pushButton_QUIT")
        self.pushButtonCV_START = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonCV_START.setGeometry(QtCore.QRect(390, 690, 171, 81))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.pushButtonCV_START.setFont(font)
        self.pushButtonCV_START.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButtonCV_START.setObjectName("pushButtonCV_START")
        self.pushButton_Open = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Open.setGeometry(QtCore.QRect(560, 730, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.pushButton_Open.setFont(font)
        self.pushButton_Open.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_Open.setObjectName("pushButton_Open")
        self.MplWidget = MplWidget(self.centralwidget)
        self.MplWidget.setGeometry(QtCore.QRect(390, 10, 801, 671))
        self.MplWidget.setObjectName("MplWidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(1100, 790, 47, 13))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(1150, 790, 47, 13))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(1170, 790, 47, 13))
        self.label_3.setObjectName("label_3")
        self.pushButtonCV_Properties = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonCV_Properties.setGeometry(QtCore.QRect(160, 200, 221, 81))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.pushButtonCV_Properties.setFont(font)
        self.pushButtonCV_Properties.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButtonCV_Properties.setObjectName("pushButtonCV_Properties")
        CA.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(CA)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 26))
        self.menubar.setObjectName("menubar")
        CA.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(CA)
        self.statusbar.setObjectName("statusbar")
        CA.setStatusBar(self.statusbar)

        self.retranslateUi(CA)
        self.pushButtonCV_Properties.clicked.connect(self.CreateAndSendFrame)
        self.pushButtonCV_START.clicked.connect(self.plot_graph)
        self.pushButton_Open.clicked.connect(self.StopPlot)
        self.pushButton_SAVE.clicked.connect(self.save_data)
        self.pushButton_QUIT.clicked.connect(CloseLocalWindow)
        QtCore.QMetaObject.connectSlotsByName(CA)

    def Change_Command(self, data):
        def write_to_hid(dev, msg_str):
            byte_str = chr(0x01) + msg_str + chr(0) * max(7 - len(msg_str), 0)
            try:
                num_bytes_written = dev.write(byte_str.encode())
            except IOError as e:
                self.Error = e
                return None

            return num_bytes_written

        data = write_to_hid(self.__device, "any string command")

    def StopPlot(self):
        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.plot(self.Plot_Xseries, self.Plot_Yseries, color='green', linestyle='dashed',
                                        marker='o', markerfacecolor='black', markersize=7)
        self.MplWidget.canvas.axes.legend(['Chronoamperometry'], loc='upper right')
        self.MplWidget.canvas.axes.set_title('Tytuł')
        self.MplWidget.canvas.axes.set_xlabel(str('Oś X'), size=20)
        self.MplWidget.canvas.axes.set_ylabel(str('Oś Y'), size=20)
        self.MplWidget.canvas.axes.grid(True, which='major', axis='both', color='0.9', linestyle='-', linewidth=1)
        self.MplWidget.canvas.draw()
        self.__isPlotStart = False

    def plot_graph(self):
        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.plot(self.Plot_Xseries, self.Plot_Yseries, color='green', linestyle='dashed',
                                        marker='o',
                                        markerfacecolor='black', markersize=7)
        self.MplWidget.canvas.axes.legend(['Chronoamperometry'], loc='upper right')
        self.MplWidget.canvas.axes.set_title('Tytuł')
        self.MplWidget.canvas.axes.set_xlabel(str('Oś X'), size=20)
        self.MplWidget.canvas.axes.set_ylabel(str('Oś Y'), size=20)
        self.MplWidget.canvas.axes.grid(True, which='major', axis='both', color='0.9', linestyle='-', linewidth=1)
        self.MplWidget.canvas.draw()
        self.__isPlotStart = True

    def save_data(self):
        dialog = QtWidgets.QFileDialog.getSaveFileName()

        if dialog[0] != '':
            f = open(dialog[0], "w+")
            for item in self.Frame_converted_series:
                f.write(item + "\n")
            f.close()

    def retranslateUi(self, CA):
        _translate = QtCore.QCoreApplication.translate
        CA.setWindowTitle(_translate("CA", "CA"))
        self.groupBoxPROPERTIESv2.setTitle(_translate("CV", "Properties:"))
        self.label_SCAN_Ewe.setText(_translate("CV", "NumData"))
        self.Propert_.setText(_translate("CV", "50"))
        self.label_V_vs_2.setText(_translate("CV", "[-]"))
        self.label_REVERSE_SCAN.setText(_translate("CV", "SE Voltage"))
        self.label_STEP_DURATION.setText(_translate("CV", "[ms]"))
        self.label_TO_VERTEX_E1.setText(_translate("CV", "RE-SE Voltage"))
        self.label_REPEAT_nc.setText(_translate("CV", "Pulse Amplitude"))
        self.label_REPEAT_TIME.setText(_translate("CV", "[mV]"))
        self.label_OVER_LAST.setText(_translate("CV", "Pulse Lenght"))
        self.label_V_vs_4.setText(_translate("CV", "[mV]"))
        self.label_V_vs_3.setText(_translate("CV", "[mV]"))
        self.Propert_1.setText(_translate("CV", "0"))
        self.Propert_2.setText(_translate("CV", "1100"))
        self.Propert_3.setText(_translate("CV", "500"))
        self.Propert_4.setText(_translate("CV", "500"))
        self.pushButton_SAVE.setText(_translate("CV", "Save data"))
        self.pushButton_QUIT.setText(_translate("CV", "Quit"))
        self.pushButtonCV_START.setText(_translate("CV", "Start plotting"))
        self.pushButton_Open.setText(_translate("CV", "Pause plotting"))
        self.label.setText(_translate("CV", "Version:"))
        self.label_2.setText(_translate("CV", "9"))
        self.label_3.setText(_translate("CV", "2"))
        self.pushButtonCV_Properties.setText(_translate("CV", "Save properties"))

    def Run(self, DataArray, DataStr):
        self.Data = DataArray
        self.AddDataToLists(DataStr)


from mplwidget import MplWidget


def Print(data):
    # print(data)
    return


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    CA = QtWidgets.QMainWindow()
    ui = Ui_CA()

    hid = Potecjostat(VID, PID)
    hid.RegisterReceiveCallbackProcedure(ui.Run)
    ui.RegisterRemoteProcedureForSendFrameToHid(hid.Change_Command)
    ui.setupCA(CA, hid)
    hid.Open()

    CA.show()
    sys.exit(app.exec_())

