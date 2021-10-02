import serial
import json


class DataLine:
    def __init__(self, jsonLine):
        self.yaw = jsonLine['yaw']
        self.pitch = jsonLine['pitch']
        self.rpm = jsonLine['rpm']
        self.speed = jsonLine['speed']
        self.depth = jsonLine['depth']
        self.battery = jsonLine['battery']


print("Serial Setup")
ending = bytes('}', 'utf-8')
# serial setup
ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=9600,
    #    parity=serial.PARITY_NONE,
    #    stopbits=serial.STOPBITS_ONE,
    #    bytesize=serial.EIGHTBITS,
    #    timeout=1
)

while True:
    ending = bytes('}', 'utf-8')
    # while number of bytes in input buffer is greater than 0
    while ser.in_waiting > 0:
        line = ser.read_until(ending)
        try:
            jsonLine = json.loads(line)
            print(jsonLine)
            try:
                dataLine = DataLine(jsonLine)
            except KeyError:
                print("KeyError", "Dictionary key incorrect from serial data")
            print(dataLine.__dict__)

            # configure data Values to display
            # ValuesText = "RPM:" + str(DataToDisplay['rpm']) + " rpm    Speed:" + str(
            #     DataToDisplay['speed']) + " m/s     Depth:" + str(DataToDisplay['depth']) + "m"
            # pitchAjust = (DataToDisplay['pitch'] + pitchRange) / (pitchRange * 2)
            # yawAjust = (DataToDisplay['yaw'] + yawRange) / (yawRange * 2)
        except json.decoder.JSONDecodeError:
            print("json.decoder.JSONDecodeError")
        except UnicodeDecodeError:
            print("UnicodeDecodeError")
