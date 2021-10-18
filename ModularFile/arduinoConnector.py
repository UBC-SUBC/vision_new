import serial
import json

class ArduinoConnector():
    #serialPiPort = '/dev/ttyACM0'
    serialPiPort = '/dev/ttyUSB0'
    DataToDisplay = {'yaw':20, 'pitch':10, 'rpm':'100', 
                    'speed':'2','depth':'2.5','battery':True}
    ErrorData = {'yaw':-1, 'pitch':-1, 'rpm':'-1', 
                'speed':'-1', 'depth':'-1','battery':False}
    ending = bytes('}', 'utf-8')
    def __init__(self) -> None: 
        #serial setup
        ser=serial.Serial(
        port=self.serialPiPort,
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
            DataToDisplay = self.ErrorData
        return DataToDisplay
        

