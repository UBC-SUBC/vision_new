from gpiozero import Button
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

#setup display variables
screenX =  int(800)
screenY =  int(480)
screenFramrate = 30
linegap = int(0.04 * screenY)
linewidth = int(0.01 * screenY)
sliderwidth = int(0.02 * screenY)
lineextra = int(0.05 * screenY)
barcolor = (26, 255, 26,230)
slidercolor = (153,102,255,230)
background = (0,0,0,80)
path = '/media/usb/' #black usb
yawRange = int(45)
pitchRange = int(30)
buttonpin = 2

#initial data values (pre serial)
DataToDisplay = {'yaw':20, 'pitch':10, 'rpm':'100', 'speed':'2','depth':'2.5','battery':True}

#camera Setup
camera = PiCamera()
camera.led =True
camera.resolution = (screenX,screenY)
camera.framerate = screenFramrate
camera.vflip=True
camera.clock_mode='reset'

#serial setup
ser=serial.Serial(
    port='/dev/ttyUSB0',
    baudrate = 9600,
#    parity=serial.PARITY_NONE,
#    stopbits=serial.STOPBITS_ONE,
#    bytesize=serial.EIGHTBITS,
#    timeout=1
)
ser.flush()

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
WarningIM = Image.open("/media/usb/warning.png")
WarningIM = WarningIM.resize([linegap*2,linegap*2])
BatteryIM = Image.open("/media/usb/lowbatt.png")
BatteryIM = BatteryIM.resize([linegap*2,linegap*2])
RaceIM = Image.open("/media/usb/sub.png")
RaceIM = RaceIM.resize([linegap*2,linegap*2])
lightsIM = Image.open("/media/usb/highbeams.png")
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

def SwitchStatus(DataToButton):
    # switches between recording and motors on status to idle and lights on status
    # while status is motors than it also starts the recording and stops it in lights
    # updates the overlay to add the icon to display the correct status
    lights = True
    motors = False
    
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
        indicatorsoverlay.update(indicatorsIM.tobytes())
        statusbutton.wait_for_release()
    
#def SerielOverlay():
    #if ser.in_waiting > 0:
    #collects data from serial into a dict 
    ending = bytes('}', 'utf-8')
    line = ser.read_until(ending).decode('utf-8')
    DataToDisplay = json.loads(line)
    
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
    movingIM.paste(WarningIM,[int(linegap*2),int(screenY-2*linegap)])
    movingIM.paste(BatteryIM,[int(linegap*4),int(screenY-2*linegap)])
    #update the overlay with the new image
    movingOverlay.update(movingIM.tobytes())

#Start Show
camera.start_preview()
#adding stationary and initial status overlays
stationaryoverlay = camera.add_overlay(pitchYawAxisIM.tobytes(),layer=3) 
movingOverlay = camera.add_overlay(movingIM.tobytes(), layer = 4)
indicatorsoverlay = camera.add_overlay(indicatorsIM.tobytes(), layer=4)
timeoverlay = camera.add_overlay(timeIM.tobytes(), layer=4)

while True: 
    #check status on of the button
    SwitchStatus(DataToButton)
    #SerielOverlay()
    #sleep(1)
#    if DataToButton['status']==motors:
#        timetext= camera.timestamp - DataToButton['time']
#    
#        minutes = timetext /(60*10**6)
#        seconds = (timetext % (60*10**6)) /(10**6)
#        timestamptext = str(int(minutes)) + ':' + str(int(seconds)) 
#        
#        timeIM = blankcanvas.copy()
#        draw = ImageDraw.Draw(timeIM)
#        draw.text([screenX*0.9,screenY-linegap*1], timestamptext, front = datafont, fill=slidercolor)
#        timeoverlay.update(timeIM.tobytes())   
#    
#    else:
#        timetext = camera.timestamp
#        timeIM = blankcanvas.copy()
#        timeoverlay.update(timeIM.tobytes())  

#finally:
#    pause()
