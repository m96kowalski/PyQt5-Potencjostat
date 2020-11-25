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

class Ui_EIS(object):
    def __init__(self):
        self.Data = None
        self.Frame_bytes_series = []
        self.Frame_converted_series = []
        self.NYQ_Xseries = []
        self.NYQ_Yseries = []
        self.BODE_Xseries = []
        self.BODE_Yseries = []
        self.BODE_Y2series = []
        self.RemoteProcedureForSendFrameToHid = None
        self.__isPlotStart = False
        self.__isNyq = False

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

            PierwszaStr = self.lineEdit_SET_Ewe.text()
            PierwszaStr = PierwszaStr.replace(",", ".")
            PierwszaFloat = float(PierwszaStr)
            PierwszaBytes = bytearray(struct.pack("f", PierwszaFloat))
            frame += bytes(PierwszaBytes)

            DrugaStr = self.lineEdit_HOURS.text()
            DrugaStr = DrugaStr.replace(",", ".")
            DrugaFloat = float(DrugaStr)
            DrugaBytes = bytearray(struct.pack("f", DrugaFloat))
            frame += bytes(DrugaBytes)

            TrzeciaStr = self.lineEdit_REC_ECVERY.text()
            TrzeciaInt = int(TrzeciaStr)
            TrzeciaBytes = bytearray(struct.pack("I", TrzeciaInt))
            frame += bytes(TrzeciaBytes)

            CzwartaStr = self.lineEdit_REC_ECVERY_3.text()
            CzwartaInt = int(CzwartaStr)
            CzwartaBytes = bytearray(struct.pack("I", CzwartaInt))
            frame += bytes(CzwartaBytes)

            PiataStr = self.lineEdit_REC_ECVERY_2.text()
            PiataInt = int(PiataStr)
            PiataBytes = bytearray(struct.pack("i", PiataInt))
            frame += bytes(PiataBytes)

            SzostaStr = self.lineEdit_REC_ECVERY_4.text()
            SzostaStr = SzostaStr.replace(",", ".")
            SzostaFloat = float(SzostaStr)
            SzostaBytes = bytearray(struct.pack("f", SzostaFloat))
            frame += bytes(SzostaBytes)

            SiedemStr = self.lineEdit_REC_ECVERY_5.text()
            SiedemStr = SiedemStr.replace(",", ".")
            SiedemFloat = float(SiedemStr)
            SiedemBytes = bytearray(struct.pack("f", SiedemFloat))
            frame += bytes(SiedemBytes)

            # print(struct.unpack('f', frame[2:6]))
        except:
            ctypes.windll.user32.MessageBoxW(0, "Errors in properties data. ", "Eroor", 0)

        self.RemoteProcedureForSendFrameToHid(frame)


    def AddDataToLists(self, DataStr):
        self.Frame_bytes_series.append(DataStr)
        # print(DataStr)

        [Pierwsza] = struct.unpack('f', bytes(self.Data[0:4]))  # Freq
        [Druga] = struct.unpack('f', bytes(self.Data[4:8]))     # Real
        [Trzecia] = struct.unpack('f', bytes(self.Data[8:12]))  # Imag
        [Czwarta] = struct.unpack('f', bytes(self.Data[12:16])) # modul impedanci
        [Piata] = struct.unpack('f', bytes(self.Data[16:20]))   # kat fazowy


        str = "{:.2f};   {:.2f};   {:.2f};   {:.2f};   {:.2f}".format(Pierwsza, Druga, Trzecia, Czwarta, Piata)
        self.Frame_converted_series.append(str)
        print(str)

        self.NYQ_Xseries.append(Druga)
        self.NYQ_Yseries.append(Trzecia)

        self.BODE_Xseries.append(math.log10(Pierwsza))
        self.BODE_Y2series.append(math.log10(Czwarta))
        self.BODE_Yseries.append(Piata)


        if self.__isPlotStart:
            if self.__isNyq:
                self.plot_graph()
            else:
                self.plot_graph2()

    def setupEIS(self, EIS, hid):
        def CloseLocalWindow():
            hid.Close()
            self.Frame_bytes_series.clear()
            self.Frame_converted_series.clear()
            EIS.close()
        EIS.setObjectName("EIS")
        EIS.resize(1200, 850)
        EIS.setMinimumSize(QtCore.QSize(1200, 850))
        EIS.setMaximumSize(QtCore.QSize(1200, 850))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        EIS.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(EIS)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButtonEIS_QUIT = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonEIS_QUIT.setGeometry(QtCore.QRect(1040, 690, 151, 81))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.pushButtonEIS_QUIT.setFont(font)
        self.pushButtonEIS_QUIT.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButtonEIS_QUIT.setObjectName("pushButtonEIS_QUIT")
        self.pushButtonEIS_Open = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonEIS_Open.setGeometry(QtCore.QRect(90, 510, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.pushButtonEIS_Open.setFont(font)
        self.pushButtonEIS_Open.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButtonEIS_Open.setObjectName("pushButtonEIS_Open")
        self.pushButtonEIS_SAVE = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonEIS_SAVE.setGeometry(QtCore.QRect(880, 690, 151, 81))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.pushButtonEIS_SAVE.setFont(font)
        self.pushButtonEIS_SAVE.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButtonEIS_SAVE.setObjectName("pushButtonEIS_SAVE")
        self.groupBoxPROPERTIESv1 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxPROPERTIESv1.setGeometry(QtCore.QRect(10, 0, 371, 261))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.groupBoxPROPERTIESv1.setFont(font)
        self.groupBoxPROPERTIESv1.setObjectName("groupBoxPROPERTIESv1")
        self.label_SET_E = QtWidgets.QLabel(self.groupBoxPROPERTIESv1)
        self.label_SET_E.setGeometry(QtCore.QRect(10, 30, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_SET_E.setFont(font)
        self.label_SET_E.setObjectName("label_SET_E")
        self.label_FOR_tE = QtWidgets.QLabel(self.groupBoxPROPERTIESv1)
        self.label_FOR_tE.setGeometry(QtCore.QRect(10, 60, 91, 20))
        self.label_FOR_tE.setObjectName("label_FOR_tE")
        self.label_REC_EVERY = QtWidgets.QLabel(self.groupBoxPROPERTIESv1)
        self.label_REC_EVERY.setGeometry(QtCore.QRect(10, 90, 121, 21))
        self.label_REC_EVERY.setObjectName("label_REC_EVERY")
        self.label_V_vs = QtWidgets.QLabel(self.groupBoxPROPERTIESv1)
        self.label_V_vs.setGeometry(QtCore.QRect(210, 30, 55, 21))
        self.label_V_vs.setObjectName("label_V_vs")
        self.lineEdit_SET_Ewe = QtWidgets.QLineEdit(self.groupBoxPROPERTIESv1)
        self.lineEdit_SET_Ewe.setGeometry(QtCore.QRect(140, 30, 61, 22))
        self.lineEdit_SET_Ewe.setObjectName("lineEdit_SET_Ewe")
        self.lineEdit_HOURS = QtWidgets.QLineEdit(self.groupBoxPROPERTIESv1)
        self.lineEdit_HOURS.setGeometry(QtCore.QRect(140, 60, 61, 22))
        self.lineEdit_HOURS.setObjectName("lineEdit_HOURS")
        self.lineEdit_REC_ECVERY = QtWidgets.QLineEdit(self.groupBoxPROPERTIESv1)
        self.lineEdit_REC_ECVERY.setGeometry(QtCore.QRect(140, 90, 61, 22))
        self.lineEdit_REC_ECVERY.setObjectName("lineEdit_REC_ECVERY")
        self.label_V_vs_2 = QtWidgets.QLabel(self.groupBoxPROPERTIESv1)
        self.label_V_vs_2.setGeometry(QtCore.QRect(210, 60, 55, 21))
        self.label_V_vs_2.setObjectName("label_V_vs_2")
        self.label_V_vs_3 = QtWidgets.QLabel(self.groupBoxPROPERTIESv1)
        self.label_V_vs_3.setGeometry(QtCore.QRect(210, 90, 55, 21))
        self.label_V_vs_3.setObjectName("label_V_vs_3")
        self.label_REC_EVERY_2 = QtWidgets.QLabel(self.groupBoxPROPERTIESv1)
        self.label_REC_EVERY_2.setGeometry(QtCore.QRect(10, 120, 121, 21))
        self.label_REC_EVERY_2.setObjectName("label_REC_EVERY_2")
        self.label_V_vs_4 = QtWidgets.QLabel(self.groupBoxPROPERTIESv1)
        self.label_V_vs_4.setGeometry(QtCore.QRect(210, 120, 151, 21))
        self.label_V_vs_4.setObjectName("label_V_vs_4")
        self.label_V_vs_5 = QtWidgets.QLabel(self.groupBoxPROPERTIESv1)
        self.label_V_vs_5.setGeometry(QtCore.QRect(210, 140, 151, 21))
        self.label_V_vs_5.setObjectName("label_V_vs_5")
        self.lineEdit_REC_ECVERY_3 = QtWidgets.QLineEdit(self.groupBoxPROPERTIESv1)
        self.lineEdit_REC_ECVERY_3.setGeometry(QtCore.QRect(140, 120, 61, 22))
        self.lineEdit_REC_ECVERY_3.setObjectName("lineEdit_REC_ECVERY_3")
        self.label_REC_EVERY_3 = QtWidgets.QLabel(self.groupBoxPROPERTIESv1)
        self.label_REC_EVERY_3.setGeometry(QtCore.QRect(10, 170, 121, 21))
        self.label_REC_EVERY_3.setObjectName("label_REC_EVERY_3")
        self.label_V_vs_6 = QtWidgets.QLabel(self.groupBoxPROPERTIESv1)
        self.label_V_vs_6.setGeometry(QtCore.QRect(210, 170, 55, 21))
        self.label_V_vs_6.setObjectName("label_V_vs_6")
        self.label_V_vs_7 = QtWidgets.QLabel(self.groupBoxPROPERTIESv1)
        self.label_V_vs_7.setGeometry(QtCore.QRect(270, 30, 55, 21))
        self.label_V_vs_7.setText("")
        self.label_V_vs_7.setObjectName("label_V_vs_7")
        self.lineEdit_REC_ECVERY_2 = QtWidgets.QLineEdit(self.groupBoxPROPERTIESv1)
        self.lineEdit_REC_ECVERY_2.setGeometry(QtCore.QRect(140, 170, 61, 22))
        self.lineEdit_REC_ECVERY_2.setObjectName("lineEdit_REC_ECVERY_2")
        self.lineEdit_REC_ECVERY_4 = QtWidgets.QLineEdit(self.groupBoxPROPERTIESv1)
        self.lineEdit_REC_ECVERY_4.setGeometry(QtCore.QRect(140, 200, 61, 22))
        self.lineEdit_REC_ECVERY_4.setObjectName("lineEdit_REC_ECVERY_4")
        self.label_REC_EVERY_4 = QtWidgets.QLabel(self.groupBoxPROPERTIESv1)
        self.label_REC_EVERY_4.setGeometry(QtCore.QRect(10, 200, 121, 21))
        self.label_REC_EVERY_4.setObjectName("label_REC_EVERY_4")
        self.label_REC_EVERY_5 = QtWidgets.QLabel(self.groupBoxPROPERTIESv1)
        self.label_REC_EVERY_5.setGeometry(QtCore.QRect(10, 230, 121, 21))
        self.label_REC_EVERY_5.setObjectName("label_REC_EVERY_5")
        self.lineEdit_REC_ECVERY_5 = QtWidgets.QLineEdit(self.groupBoxPROPERTIESv1)
        self.lineEdit_REC_ECVERY_5.setGeometry(QtCore.QRect(140, 230, 61, 22))
        self.lineEdit_REC_ECVERY_5.setObjectName("lineEdit_REC_ECVERY_5")
        self.label_V_vs_8 = QtWidgets.QLabel(self.groupBoxPROPERTIESv1)
        self.label_V_vs_8.setGeometry(QtCore.QRect(210, 200, 55, 21))
        self.label_V_vs_8.setObjectName("label_V_vs_8")
        self.label_V_vs_9 = QtWidgets.QLabel(self.groupBoxPROPERTIESv1)
        self.label_V_vs_9.setGeometry(QtCore.QRect(210, 230, 55, 21))
        self.label_V_vs_9.setObjectName("label_V_vs_9")
        self.pushButtonEIS_START = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonEIS_START.setGeometry(QtCore.QRect(10, 430, 171, 81))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.pushButtonEIS_START.setFont(font)
        self.pushButtonEIS_START.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButtonEIS_START.setObjectName("pushButtonEIS_START")
        self.MplWidget = MplWidget(self.centralwidget)
        self.MplWidget.setGeometry(QtCore.QRect(390, 10, 801, 671))
        self.MplWidget.setObjectName("MplWidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(1110, 790, 47, 13))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(1160, 790, 47, 13))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(1180, 790, 47, 13))
        self.label_3.setObjectName("label_3")
        self.pushButtonEIS_Properties = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonEIS_Properties.setGeometry(QtCore.QRect(160, 270, 221, 81))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.pushButtonEIS_Properties.setFont(font)
        self.pushButtonEIS_Properties.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButtonEIS_Properties.setObjectName("pushButtonEIS_Properties")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(140, 380, 181, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.pushButtonEIS_START_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonEIS_START_2.setGeometry(QtCore.QRect(210, 430, 171, 81))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.pushButtonEIS_START_2.setFont(font)
        self.pushButtonEIS_START_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButtonEIS_START_2.setObjectName("pushButtonEIS_START_2")
        self.pushButtonEIS_Open_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonEIS_Open_2.setGeometry(QtCore.QRect(290, 510, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.pushButtonEIS_Open_2.setFont(font)
        self.pushButtonEIS_Open_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButtonEIS_Open_2.setObjectName("pushButtonEIS_Open_2")
        EIS.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(EIS)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 26))
        self.menubar.setObjectName("menubar")
        EIS.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(EIS)
        self.statusbar.setObjectName("statusbar")
        EIS.setStatusBar(self.statusbar)


        self.retranslateUi(EIS)
        self.pushButtonEIS_START.clicked.connect(self.plot_graph)
        self.pushButtonEIS_START_2.clicked.connect(self.plot_graph2)
        self.pushButtonEIS_Properties.clicked.connect(self.CreateAndSendFrame)
        self.pushButtonEIS_SAVE.clicked.connect(self.save_data)
        self.pushButtonEIS_Open.clicked.connect(self.StopNyq)
        self.pushButtonEIS_Open_2.clicked.connect(self.StopBode)
        self.pushButtonEIS_QUIT.clicked.connect(CloseLocalWindow)
        QtCore.QMetaObject.connectSlotsByName(EIS)



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


    def StopNyq(self):
        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.plot(self.NYQ_Xseries, self.NYQ_Yseries, color='blue', linestyle='dashed',
                                                                    marker='o', markerfacecolor='cyan', markersize=7)
        self.MplWidget.canvas.axes.legend(['Nyquist'], loc='upper right')
        self.MplWidget.canvas.axes.set_title('ZRe / - ZIm')
        self.MplWidget.canvas.axes.set_xlabel(str('ZRe / Ω'), size=20)
        self.MplWidget.canvas.axes.set_ylabel(str('-ZIm / Ω'), size=20)
        self.MplWidget.canvas.axes.grid(True, which='major', axis='both', color='0.9', linestyle='-', linewidth=1)
        self.MplWidget.canvas.draw()
        self.__isPlotStart = False
        self.__isNyq = False

    def StopBode(self):
        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.plot(self.BODE_Xseries, self.BODE_Yseries, color='red', linestyle='dashed', marker='o',
                                                                                    markerfacecolor='magenta', markersize=7)
        self.MplWidget.canvas.axes.legend(['Bode'], loc='upper right')
        self.MplWidget.canvas.axes.set_title('log(Freq) / log(|Z|)')
        self.MplWidget.canvas.axes.set_xlabel(str('OŚ X'), size=20)
        self.MplWidget.canvas.axes.set_ylabel(str('OŚ Y'), size=20)
        self.MplWidget.canvas.axes.grid(True, which='major', axis='both', color='0.9', linestyle='-', linewidth=1)
        self.MplWidget.canvas.draw()
        self.__isPlotStart = False
        self.__isNyq = True

    def plot_graph(self):
        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.plot(self.NYQ_Xseries, self.NYQ_Yseries, color='blue', linestyle='dashed', marker='o',
                                                                                    markerfacecolor='cyan', markersize=7)
        self.MplWidget.canvas.axes.legend(['Nyquist'], loc='upper right')
        self.MplWidget.canvas.axes.set_title('ZRe / - ZIm')
        self.MplWidget.canvas.axes.set_xlabel(str('ZRe / Ω'), size=20)
        self.MplWidget.canvas.axes.set_ylabel(str('-ZIm / Ω'), size=20)
        self.MplWidget.canvas.axes.grid(True, which='major', axis='both', color='0.9', linestyle='-', linewidth=1)
        self.MplWidget.canvas.draw()
        self.__isPlotStart = True
        self.__isNyq = True

    def plot_graph2(self):
        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.plot(self.BODE_Xseries, self.BODE_Yseries, color='red', linestyle='dashed', marker='o',
                                                                                    markerfacecolor='magenta', markersize=7)
        self.MplWidget.canvas.axes.legend(['Bode'], loc='upper right')
        self.MplWidget.canvas.axes.set_title('log(Freq) / log(|Z|)')
        self.MplWidget.canvas.axes.set_xlabel(str('OŚ X'), size=20)
        self.MplWidget.canvas.axes.set_ylabel(str('OŚ Y'), size=20)
        self.MplWidget.canvas.axes.grid(True, which='major', axis='both', color='0.9', linestyle='-', linewidth=1)
        self.MplWidget.canvas.draw()
        self.__isPlotStart = True
        self.__isNyq = False


    def save_data(self):
        dialog = QtWidgets.QFileDialog.getSaveFileName()

        if dialog[0] != '':
            f = open(dialog[0], "w+")
            for item in self.Frame_converted_series:
                f.write(item+"\n")
            f.close()


    def retranslateUi(self, EIS):
        _translate = QtCore.QCoreApplication.translate
        EIS.setWindowTitle(_translate("EIS", "EIS"))
        self.pushButtonEIS_QUIT.setText(_translate("EIS", "Quit"))
        self.pushButtonEIS_Open.setText(_translate("EIS", "Pause Nyquist \n"
                                                          "plot"))
        self.pushButtonEIS_SAVE.setText(_translate("EIS", "Save data"))
        self.groupBoxPROPERTIESv1.setTitle(_translate("EIS", "Properties:"))
        self.label_SET_E.setText(_translate("EIS", "Start Freq"))
        self.label_FOR_tE.setText(_translate("EIS", "Stop Freq"))
        self.label_REC_EVERY.setText(_translate("EIS", "Points Number"))
        self.label_V_vs.setText(_translate("EIS", "[Hz] "))
        self.lineEdit_SET_Ewe.setText(_translate("EIS", "150000"))
        self.lineEdit_HOURS.setText(_translate("EIS", "0,2"))
        self.lineEdit_REC_ECVERY.setText(_translate("EIS", "200"))
        self.label_V_vs_2.setText(_translate("EIS", "[Hz] "))
        self.label_V_vs_3.setText(_translate("EIS", "[-]"))
        self.label_REC_EVERY_2.setText(_translate("EIS", "Arrangement"))
        self.label_V_vs_4.setText(_translate("EIS", "0 - when linear"))
        self.label_V_vs_5.setText(_translate("EIS", "1 - when logarithmic"))
        self.lineEdit_REC_ECVERY_3.setText(_translate("EIS", "1"))
        self.label_REC_EVERY_3.setText(_translate("EIS", "NumData"))
        self.label_V_vs_6.setText(_translate("EIS", "[-]"))
        self.lineEdit_REC_ECVERY_2.setText(_translate("EIS", "200"))
        self.lineEdit_REC_ECVERY_4.setText(_translate("EIS", "0,000"))
        self.label_REC_EVERY_4.setText(_translate("EIS", "Amplitude P2P"))
        self.label_REC_EVERY_5.setText(_translate("EIS", "DC Signal"))
        self.lineEdit_REC_ECVERY_5.setText(_translate("EIS", "0,000"))
        self.label_V_vs_8.setText(_translate("EIS", "[mV] "))
        self.label_V_vs_9.setText(_translate("EIS", "[mV] "))
        self.pushButtonEIS_START.setText(_translate("EIS", "Nyquist"))
        self.label.setText(_translate("EIS", "Version:"))
        self.label_2.setText(_translate("EIS", "7"))
        self.label_3.setText(_translate("EIS", "7"))
        self.pushButtonEIS_Properties.setText(_translate("EIS", "Save properties"))
        self.label_4.setText(_translate("EIS", "Plotting"))
        self.pushButtonEIS_START_2.setText(_translate("EIS", "Bode"))
        self.pushButtonEIS_Open_2.setText(_translate("EIS", "Pause Bode \n"
                                                            "plot"))
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
    EIS = QtWidgets.QMainWindow()
    ui = Ui_EIS()

    hid = Potecjostat(VID, PID)
    hid.RegisterReceiveCallbackProcedure(ui.Run)
    ui.RegisterRemoteProcedureForSendFrameToHid(hid.Change_Command)
    ui.setupEIS(EIS, hid)
    hid.Open()

    EIS.show()
    sys.exit(app.exec_())
