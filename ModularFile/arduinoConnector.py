import serial
import json
from .variables import ArduinoVar


class ArduinoConnector():
    def __init__(self) -> None: 
        #serial setup
        ser=serial.Serial(
        port=ArduinoVar.serialPiPort,
        baudrate = 9600,
        #    parity=serial.PARITY_NONE,
        #    stopbits=serial.STOPBITS_ONE,
        #    bytesize=serial.EIGHTBITS,
        #    timeout=1
        )
        ser.flush()
        
    def readJsonFromArduino(self):
        try:
            line = self.ser.read_until(self.ending)
            DataToDisplay = json.loads(line)
        except:
            DataToDisplay = ArduinoVar.ErrorData
        return DataToDisplay
        

