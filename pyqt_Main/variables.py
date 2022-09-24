class ArduinoVar:
    usbPath = '/media/usb3/'
    serialPiPort = '/dev/ttyACM0'
    #serialPiPort = '/dev/ttyUSB0'
    DataToDisplay = {'yaw':20, 'pitch':10, 'rpm':'100', 
                    'speed':'2','depth':'2.5','battery':True}
    ErrorData = {'yaw':-1, 'pitch':-1, 'rpm':'-1', 
                'speed':'-1', 'depth':'-1','battery':False}
    ending = bytes('}', 'utf-8')
    
class CameraVar:
    screenX =  int(1280)
    screenY =  int(720) #camera is also recording at this res
    screenFramrate = 30
    ## Sets the state of the camera’s LED via GPIO.
    led = True
    resolution = (screenX, screenY)
    framerate = screenFramrate
    vflip = True
    clock_mode="reset"
    
    
class DisplayVar:
    #setup display variables
    screenX =  CameraVar.screenX
    screenY =  CameraVar.screenY #camera is also recording at this res
    screenFramrate = CameraVar.framerate
    linegap = int(0.04 * screenY)
    linewidth = int(0.01 * screenY)
    sliderwidth = int(0.02 * screenY)
    lineextra = int(0.05 * screenY)
    barcolor = (26, 255, 26,230)
    slidercolor = (153,102,255,230)
    background = (0,0,0,80)
    yawRange = int(90)
    pitchRange = int(30)
    datafontStyleLoc = "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"
    datafontSize = 20
    smalltextfontStyle = "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"
    smalltextfontSize = 8

    
class ImageVar:
    imagePath = "Images"
    linegap = int(0.04 * CameraVar.screenY)
 
    
class ButtonVar:
    lights = True
    motors = False
    buttonpin = 2
    
