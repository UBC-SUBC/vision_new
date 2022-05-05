#import serial
#import json
#from variables import ArduinoVar
import random


class ArduinoConnector:
     ending = bytes('}', 'utf-8')
    
   #  def __init__(self) -> None: 
   #      self.ErrorData = {'yaw':-99999, 'pitch':-99999, 'rpm': "-99999",
   #          'speed': "-99999", 'depth': "-99999",'battery':False}
   #     
   #      #serial setup
   #      ser=serial.Serial(
   #      port=ArduinoVar.serialPiPort,
   #      baudrate = 115200,
   #         parity=serial.PARITY_NONE,
   #         stopbits=serial.STOPBITS_ONE,
   #         bytesize=serial.EIGHTBITS,
   #         timeout=1
   #      )
   #      ser.flush()

     def readJsonFromArduino(self):
        ErrorData = {'yaw':random.randint(-100, 100), 'pitch':random.randint(-100, 100), 'rpm': str(random.randint(-100, 100)),
            'speed': str(random.randint(-100, 100)), 'depth': str(random.randint(-100, 100)),'battery':False}
        return ErrorData
    
   #  def readJsonFromArduino(self):
   #      try:
   #          line = self.ser.read_until(self.ending)
   #          DataToDisplay = json.loads(line)
   #      except:
   #          DataToDisplay = ArduinoVar.ErrorData
   #      return DataToDisplay
        
        

