import hid
import _thread
import threading
import sys
import time



class Potecjostat():
    def __init__(self, VENDOR_ID, PRODUCT_ID):
        self.__VID = VENDOR_ID
        self.__PID = PRODUCT_ID
        self.__isOpen = False
        self.Name = "NONE"
        self.Error = "NONE"
        self.isRuning = False
        self.MainThread = None
        self.ReceiveCallbackProcedure = None
        try:
            self.__device = hid.device()
        except IOError as e:
            self.Error = e



    def RegisterReceiveCallbackProcedure(self, procedureCallback):
        self.ReceiveCallbackProcedure = procedureCallback
        try:
            self.isRuning = True
            #_thread.start_new_thread(self.SerialReadlineThread, ())

            self.MainThread = threading.Thread(target=self.SerialReadlineThread)
            self.MainThread.start()
        except:
            print("Error1: ", sys.exc_info()[0])



    def SerialReadlineThread(self):
        while self.isRuning:
            time.sleep(0.25)
            try:
                if self.__isOpen:
                    data = self.__device.read(100, 2000)
                    dataStr = ';'.join(str(n) for n in data[0:40])
                    if data != None:
                        self.ReceiveCallbackProcedure(data, dataStr)
            except:
                print("Error: ", sys.exc_info()[0])




    def Open(self):
        try:
            self.__device.open(self.__VID, self.__PID)
            self.__isOpen = True
            self.Error = "IsOpen"
        except IOError as e:
            self.Error = e
        self.Name = self.__device.get_product_string()



    def Close(self):
        self.isRuning = False
        time.sleep(0.25)
        self.MainThread.join()
        self.__device.close()




    def Change_Command(self, data):
        try:
            ret = self.__device.write(data)
            # print(ret)
            # print(data[0])
            # print(data[1])
            # print(data[2])
            # print(data[3])
        except IOError as e:
            print(e)










