from gpiozero import Button
import time
import RPi.GPIO as GPIO
from time import sleep
import picamera
from picamera import PiCamera
from datetime import datetime
from signal import pause
import os
import serial
import numpy as np
import string
from PIL import Image, ImageDraw, ImageFont
import json


# changing variables based on raspi
path = '/media/usb3/'  # usb path to save files
#serialPiPort = '/dev/ttyACM0'
serialPiPort = '/dev/ttyUSB0'
imagePath = "/home/pi/Desktop/vision/"  # images path on pi

#setup display variables
screenX =  int(1280)
screenY =  int(720) #camera is also recording at this res
screenFramrate = 30
linegap = int(0.04 * screenY)
linewidth = int(0.01 * screenY)
sliderwidth = int(0.02 * screenY)
lineextra = int(0.05 * screenY)
barcolor = (26, 255, 26,230)
slidercolor = (153,102,255,230)
background = (0,0,0,80)
yawRange = int(90)
pitchRange = int(30)
buttonpin = 2


#initial data values (pre serial)
DataToDisplay = {'yaw':20, 'pitch':10, 'rpm':'100', 'speed':'2','depth':'2.5','battery':True}
ErrorData = {'yaw':-1, 'pitch':-1, 'rpm':'-1', 'speed':'-1', 'depth':'-1','battery':False}
#camera Setup
camera = PiCamera()
camera.led =True
camera.resolution = (screenX,screenY)
camera.framerate = screenFramrate
camera.vflip=True
camera.clock_mode='reset'

#serial setup
try:
    ser=serial.Serial(
    port=serialPiPort,
    baudrate = 9600,
#    parity=serial.PARITY_NONE,
#    stopbits=serial.STOPBITS_ONE,
#    bytesize=serial.EIGHTBITS,
#    timeout=1
    )
    ser.flush()
except:
    ser = None

#button setup
statusbutton = Button(buttonpin)
DataToButton = {'status':True, 'time':0}
lights = True
motors = False
#turnoffbutton = Button(buttonpin,hold_time = 3)

#creating blank image canvas and fonts data
blankcanvas = Image.new('RGBA',(screenX,screenY))
datafont = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",20)
smalltextfont = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",8)

#creaitng images for indicators
WarningIM = Image.open(imagePath+"warning.png")
WarningIM = WarningIM.resize([linegap*2,linegap*2])
BatteryIM = Image.open(imagePath+"lowbatt.png")
BatteryIM = BatteryIM.resize([linegap*2,linegap*2])
RaceIM = Image.open(imagePath + "sub.png")
RaceIM = RaceIM.resize([linegap*2,linegap*2])
lightsIM = Image.open(imagePath+"highbeams.png")
lightsIM = lightsIM.resize([linegap*2,linegap*2])

#creating stationary image for bars and backgroungs
pitchYawAxisIM = blankcanvas.copy()
draw = ImageDraw.Draw(pitchYawAxisIM)
draw.rectangle([0,0,screenX,linegap*2.5],fill=background)
draw.rectangle([screenX-linegap*2.5,0,screenX,screenY],fill=background)
draw.rectangle([screenX*0,screenY-linegap*2,screenX*1,screenY],fill=background)
draw.line([linegap+lineextra,linegap,screenX-(linegap+lineextra),linegap],fill=barcolor,width=linewidth)
draw.line([screenX-(linegap),linegap+lineextra,screenX-(linegap),screenY-linegap-lineextra],fill=barcolor,width=linewidth)
draw.line([screenX/2,linegap*0.5,screenX/2,linegap*1.5],fill=barcolor,width=linewidth)
draw.line([screenX-linegap*1.5,screenY/2,screenX-linegap*0.5,screenY/2],fill=barcolor,width=linewidth)
draw.text([screenX*0.5-8*1,linegap*2],"yaw",fill=barcolor,font=smalltextfont)
draw.text([screenX-linegap*2,screenY*0.5-9*2],"p",font=smalltextfont , fill=barcolor)
draw.text([screenX-linegap*2,screenY*0.5-9*1],"i",font=smalltextfont , fill=barcolor)
draw.text([screenX-linegap*2,screenY*0.5],"t",font=smalltextfont , fill=barcolor)
draw.text([screenX-linegap*2,screenY*0.5+9],"c",font=smalltextfont , fill=barcolor)
draw.text([screenX-linegap*2,screenY*0.5+9*2],"h",font=smalltextfont , fill=barcolor)
draw.text([screenX-linegap*2,linegap*2],str(pitchRange),font=smalltextfont , fill=barcolor)
draw.text([screenX-linegap*2,screenY-linegap*2],"-"+str(pitchRange),font=smalltextfont , fill=barcolor)


#creating blank overlays for updating overlays
movingIM = blankcanvas.copy()
indicatorsIM = blankcanvas.copy()
timeIM = blankcanvas.copy()

#Start Show
camera.start_preview()
#adding stationary and initial status overlays
stationaryoverlay = camera.add_overlay(pitchYawAxisIM.tobytes(),layer=3) 
movingOverlay = camera.add_overlay(movingIM.tobytes(), layer = 4)
indicatorsoverlay = camera.add_overlay(indicatorsIM.tobytes(), layer=4)
timeoverlay = camera.add_overlay(timeIM.tobytes(), layer=4)

def SwitchStatus():
    # switches between recording and motors on status to idle and lights on status
    # while status is motors than it also starts the recording and stops it in lights
    # updates the overlay to add the icon to display the correct status
    lights = True
    motors = False
    global DataToButton
    if statusbutton.is_pressed:
        indicatorsIM = blankcanvas.copy()
        if DataToButton['status'] == lights:
            #change overlay status
            DataToButton['status'] = motors
            indicatorsIM.paste(RaceIM,[int(linegap*8),int(screenY-2*linegap)])
            #start recording and creat recording file
            timestamp = datetime.now().strftime("%Y-%m-%d_%H_%M_%p")
            print("Start Recording")
            camera.start_recording(path+timestamp+'.h264')
            camera.led=False
            #save the time the recording starts
            DataToButton['time']=int(camera.timestamp)
        else: 
            #change overlay status
            DataToButton['status'] = lights
            indicatorsIM.paste(lightsIM,[int(linegap*8),int(screenY-2*linegap)])
            #recoring stop
            camera.stop_recording()
            print("Stop Recording")
            camera.led=True
            #clear the timestamp
            DataToButton['time']=int(camera.timestamp)

        #update overlay
        global indicatorsoverlay
        camera.remove_overlay(indicatorsoverlay)
        indicatorsoverlay=camera.add_overlay(indicatorsIM.tobytes(), layer=4)
        statusbutton.wait_for_release()
    
def SerielOverlay():
    global DataToDisplay
    #if ser.in_waiting > 0:
    #collects data from serial into a dict
    ending = bytes('}', 'utf-8')
    flag = 0
    while flag < 1:
        try:
            line = ser.read_until(ending)
            DataToDisplay = json.loads(line)
        except:
            DataToDisplay = ErrorData
    
        # configure data Values to display
        ValuesText = "RPM:" + str(DataToDisplay['rpm']) + " rpm    Speed:" + str(
        DataToDisplay['speed']) + " m/s     Depth:" + str(DataToDisplay['depth']) + "m"
        pitchAjust = (DataToDisplay['pitch'] + pitchRange) / (pitchRange * 2)
        yawAjust = (DataToDisplay['yaw'] + yawRange) / (yawRange * 2)
        flag = 1
            

    

    # line = ser.read_until(ending).decode('utf-8')
    # try:
    #     DataToDisplay = json.loads(line)
    # except:
    #     print("didn't load json")
    
    #configure data Values to display
    ValuesText = "RPM:"+str(DataToDisplay['rpm']) +" rpm    Speed:"+str(DataToDisplay['speed']) + " m/s     Depth:"+str(DataToDisplay['depth'])+"m"
    pitchAjust = (DataToDisplay['pitch']+pitchRange)/(pitchRange*2)
    yawAjust = (DataToDisplay['yaw']+yawRange)/(yawRange*2)

    #creating changing data images for serial canvas
    movingIM = blankcanvas.copy()
    draw = ImageDraw.Draw(movingIM)
    draw.line([yawAjust*screenX,linegap*0.5,yawAjust*screenX,linegap*1.5],fill = slidercolor, width=sliderwidth)
    draw.line([screenX-linegap*1.5,screenY*pitchAjust,screenX-linegap*0.5,screenY*pitchAjust],fill = slidercolor, width=sliderwidth)
    draw.text([screenX*0.3,screenY-linegap*1.5],ValuesText,fill=slidercolor,font=datafont,alin="center")
    #if DataToDisplay['warning'] == True:
        #movingIM.paste(WarningIM,[int(linegap*2),int(screenY-2*linegap)])
    if DataToDisplay['battery'] == True: 
        movingIM.paste(BatteryIM,[int(linegap*4),int(screenY-2*linegap)])

    #update the overlay with the new image
    global movingOverlay
    #camera.remove_overlay(movingoverlay)
    #movingOverlay = camera.add_overlay(movingIM.tobytes(),layer = 4)
    movingOverlay.update(movingIM.tobytes())
    time.sleep(0.1)

try:
    while True: 
        #check status on of the button
        SwitchStatus()
        SerielOverlay()
#break when key pressed
except KeyboardInterrupt:
    pass

