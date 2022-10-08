import serial
import json
from variables import ArduinoVar
import random
from ..protobuf.generated import SUBC_pb2 as messaging


class ArduinoConnector:
     ending = bytes('\n', 'utf-8')
    
     def getErrorData(self):
        return {'yaw':-random.randint(0,10), 'pitch':-random.randint(0,10), 'rpm': str(-random.randint(0,10)),
             'speed': "-99999", 'depth': "-99999",'battery':False}
    
     def __init__(self) -> None: 
         self.ErrorData = {'yaw':-99999, 'pitch':-99999, 'rpm': "-99999",
             'speed': "-99999", 'depth': "-99999",'battery':False}
        
         self.message = messaging.FromDAQ()

         #serial setup
         try:
             self.ser=serial.Serial(
             port= ArduinoVar.serialPiPort,
             baudrate = 115200,
                 parity=serial.PARITY_NONE,
                 stopbits=serial.STOPBITS_ONE,
                 bytesize=serial.EIGHTBITS,
                 timeout=1
             )
             self.ser.flush()
         except:
             self.ser = None
             print('No DAQ board detected')   
    
     # Read serial data from the daq system. All values are passed as a JSON
     def readJsonFromArduino(self):
         # we try to create a new serial object if one is not currently available in order to recover our connection
         if self.ser is None:
             try:
                 self.ser=serial.Serial(
                 port= ArduinoVar.serialPiPort,
                 baudrate = 115200,
                     parity=serial.PARITY_NONE,
                     stopbits=serial.STOPBITS_ONE,
                     bytesize=serial.EIGHTBITS,
                     timeout=1
                 )
                 self.ser.flush()
             except:
                 self.ser = None
                 print('No DAQ board detected try reconnecting')   
         try:             
             line = self.ser.readline().decode('utf-8')
             line.replace('\n', '')
             line.replace('\r', '')
             DataToDisplay = json.loads(line)
         except:
             print("failed again display error data")
             if self.ser is not None:
                self.ser.close()
                self.ser = None
            #  DataToDisplay = self.ErrorData
             DataToDisplay = self.getErrorData()
         print(DataToDisplay)
         return DataToDisplay
         
     def readProtobufFromDAQ(self):
         try:
            line = self.ser.readline()
            self.message.ParseFromString(line)
            print('Decoded object:\n', self.message)
            return self.message
         except:
            self.message.yaw = -1
            self.message.pitch = -1
            self.message.rpm = -1
            self.message.depth = -1
            self.message.speed = -1
            self.message.battery = False
            print('Failed to read a message from the DAQ')
         
         return self.message
         
