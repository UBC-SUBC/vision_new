import serial
import json
from variables import ArduinoVar
import random


class ArduinoConnector:
     ending = bytes('\n', 'utf-8')
    
     def __init__(self) -> None: 
         self.ErrorData = {'yaw':-99999, 'pitch':-99999, 'rpm': "-99999",
             'speed': "-99999", 'depth': "-99999",'battery':False}
        
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
             if self.ser is not None:
                self.ser.close()
                self.ser = None
             DataToDisplay = self.ErrorData
         print(DataToDisplay)
         return DataToDisplay