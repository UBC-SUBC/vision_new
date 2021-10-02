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
import time

# changing variables based on raspi
path = '/media/usb3/'  # usb path to save files
serialPiPort = '/dev/ttyACM0'
imagePath = "/home/pi/Desktop/vision/"  # images path on pi

# setup display variables
screenX = int(1280)
screenY = int(720)  # camera is also recording at this res
screenFramrate = 30
linegap = int(0.04 * screenY)
linewidth = int(0.01 * screenY)
sliderwidth = int(0.02 * screenY)
lineextra = int(0.05 * screenY)
barcolor = (26, 255, 26, 230)
slidercolor = (153, 102, 255, 230)
background = (0, 0, 0, 80)
yawRange = int(90)
pitchRange = int(30)
buttonGPIO2 = 2  # GPIO 2, PIN 3, Button enables recording in 3 min intervals
buttonGPIO3 = 3  # GPIO 2, PIN 5, Button enables recording in continuous intervals

# initial data values (pre serial)
jsonLine = {'yaw': 20, 'pitch': 10, 'rpm': '100', 'speed': '2', 'depth': '2.5', 'battery': True}
staticJsonLine = jsonLine

# camera Setup
camera = PiCamera()
camera.led = True
camera.resolution = (screenX, screenY)
camera.framerate = screenFramrate
camera.vflip = True
camera.clock_mode = 'reset'


# serial setup
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
ser = serial.Serial(
	port='/dev/ttyACM0',
	baudrate=9600
	#    parity=serial.PARITY_NONE,
	#    stopbits=serial.STOPBITS_ONE,
	#    bytesize=serial.EIGHTBITS,
	#    timeout=1
)

# creating blank image canvas and fonts data
blankCanvas = Image.new('RGBA', (screenX, screenY))
datafont = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSansBold.ttf", 20)
smalltextfont = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSansBold.ttf", 8)

# creaitng images for indicators --- currently unused
WarningIM = Image.open(imagePath + "warning.png")
WarningIM = WarningIM.resize([linegap * 2, linegap * 2])
BatteryIM = Image.open(imagePath + "lowbatt.png")
BatteryIM = BatteryIM.resize([linegap * 2, linegap * 2])
RaceIM = Image.open(imagePath + "sub.png")
RaceIM = RaceIM.resize([linegap * 2, linegap * 2])
lightsIM = Image.open(imagePath + "highbeams.png")
lightsIM = lightsIM.resize([linegap * 2, linegap * 2])


# Effect: Create stationary image for bars/backgrounds on overlay then adds overlay to camera
def paintStationaryOverlay():
	pitchYawAxisIM = Image.new('RGBA', (screenX, screenY))
	draw = ImageDraw.Draw(pitchYawAxisIM)
	draw.rectangle([0, 0, screenX, linegap * 2.5], fill=background)
	draw.rectangle([screenX - linegap * 2.5, 0, screenX, screenY], fill=background)
	draw.rectangle([screenX * 0, screenY - linegap * 2, screenX * 1, screenY], fill=background)
	draw.line([linegap + lineextra, linegap, screenX - (linegap + lineextra), linegap], fill=barcolor, width=linewidth)
	draw.line([screenX - (linegap), linegap + lineextra, screenX - (linegap), screenY - linegap - lineextra],
			  fill=barcolor, width=linewidth)
	draw.line([screenX / 2, linegap * 0.5, screenX / 2, linegap * 1.5], fill=barcolor, width=linewidth)
	draw.line([screenX - linegap * 1.5, screenY / 2, screenX - linegap * 0.5, screenY / 2], fill=barcolor,
			  width=linewidth)
	draw.text([screenX * 0.5 - 8 * 1, linegap * 2], "yaw", fill=barcolor, font=smalltextfont)
	draw.text([screenX - linegap * 2, screenY * 0.5 - 9 * 2], "p", font=smalltextfont, fill=barcolor)
	draw.text([screenX - linegap * 2, screenY * 0.5 - 9 * 1], "i", font=smalltextfont, fill=barcolor)
	draw.text([screenX - linegap * 2, screenY * 0.5], "t", font=smalltextfont, fill=barcolor)
	draw.text([screenX - linegap * 2, screenY * 0.5 + 9], "c", font=smalltextfont, fill=barcolor)
	draw.text([screenX - linegap * 2, screenY * 0.5 + 9 * 2], "h", font=smalltextfont, fill=barcolor)
	draw.text([screenX - linegap * 2, linegap * 2], str(pitchRange), font=smalltextfont, fill=barcolor)
	draw.text([screenX - linegap * 2, screenY - linegap * 2], "-" + str(pitchRange), font=smalltextfont, fill=barcolor)

	camera.add_overlay(pitchYawAxisIM.tobytes(), layer=3)


# Effect: Reads serial data and returns a python class object of the data
def readSerialData():
	ending = bytes('}', 'utf-8')
	line = ser.read_until(ending)
	try:
		jsonLine = json.loads(line)
		# print(jsonLine)
		try:
			global dataLine
			dataLine = DataLine(jsonLine)
			return dataLine
		except KeyError:
			print("KeyError", "Dictionary key incorrect from serial data")
	# print(dataLine.__dict__)
	except json.decoder.JSONDecodeError:
		print("json.decoder.JSONDecodeError")
	except UnicodeDecodeError:
		print("UnicodeDecodeError")

def getTimeElapsed():
	TimeElapsedInSeconds = (datetime.now() - startDateTime).total_seconds()
	days = divmod(TimeElapsedInSeconds, 86400)  # Get days (without [0]!)
	hours = divmod(days[1], 3600)  # Use remainder of days to calc hours
	minutes = divmod(hours[1], 60)  # Use remainder of hours to calc minutes
	seconds = divmod(minutes[1], 1)  # Use remainder of minutes to calc seconds
	return days[0], hours[0], minutes[0], seconds[0]


def getCheckpointTimeElapsed(lastCheckpointDateTime):
	TimeElapsedInSeconds = (datetime.now() - lastCheckpointDateTime).total_seconds()
	days = divmod(TimeElapsedInSeconds, 86400)  # Get days (without [0]!)
	hours = divmod(days[1], 3600)  # Use remainder of days to calc hours
	minutes = divmod(hours[1], 60)  # Use remainder of hours to calc minutes
	seconds = divmod(minutes[1], 1)  # Use remainder of minutes to calc seconds
	return days[0], hours[0], minutes[0], seconds[0]

# Effect: Creates moving indicators on bars on overlay then adds overlay to camera
def paintMovingDisplay(dataLine):
	# configure data Values to display
	ValuesText = "RPM: {:02d} rpm    Speed: {:02d} m/s    Depth: {:02d} m".format(dataLine.rpm, dataLine.speed, dataLine.depth)
	# -------------Print current time and time elapse--------------
	PiTime = "Pi " + datetime.now().strftime("%H:%M")
	days, hours, minutes, seconds = getTimeElapsed()
	TimeElapsed = "Elapsed {:02.0f}:{:02.0f}".format(minutes,seconds)
	# -------------Print current time and time elapse--------------


	pitchAjust = (dataLine.pitch + pitchRange) / (pitchRange * 2)
	yawAjust = (dataLine.yaw + yawRange) / (yawRange * 2)

	# creating changing data images for serial canvas
	movingIM = Image.new('RGBA', (screenX, screenY))
	draw = ImageDraw.Draw(movingIM)
	draw.line([yawAjust * screenX, linegap * 0.5, yawAjust * screenX, linegap * 1.5], fill=slidercolor,
			  width=sliderwidth)
	draw.line([screenX - linegap * 1.5, screenY * pitchAjust, screenX - linegap * 0.5, screenY * pitchAjust],
			  fill=slidercolor, width=sliderwidth)
	draw.text([screenX * 0.3, screenY - linegap * 1.5], ValuesText, fill=slidercolor, font=datafont, alin="center")

	# -------------Print current time and time elapse--------------
	draw.text([screenX * 0.8, screenY - linegap * 1.5], PiTime, fill=slidercolor, font=datafont, alin="center")
	draw.text([screenX * 0.88, screenY - linegap * 1.5], TimeElapsed, fill=slidercolor, font=datafont, alin="center")
	# -------------Print current time and time elapse--------------

	# ----Print DAQ serial status
	draw.text([screenX * 0.7, screenY - linegap * 1.5], serialStatus, fill=slidercolor, font=datafont, alin="center")
	# ----Print DAQ serial status


	# if DataToDisplay['warning'] == True:
	# movingIM.paste(WarningIM,[int(linegap*2),int(screenY-2*linegap)])
	if dataLine.battery == True:
		movingIM.paste(BatteryIM, [int(linegap * 4), int(screenY - 2 * linegap)])

	# update the overlay with the new image

	global movingOverlay
	global movingOverlayPrev

	# 1. New overlay is added and reference is held
	movingOverlay = camera.add_overlay(movingIM.tobytes(), layer=4)

	# 2. Previous overlay is removed
	if movingOverlayPrev is None:
		print("Prev is None")
	else:
		camera.remove_overlay(movingOverlayPrev)

	# 3. Current overlay is set as the Previous overlay
	movingOverlayPrev = movingOverlay


# Previous .update method
# movingOverlay.update(movingIM.tobytes())

# Button Setup
buttonGPIO2Status = Button(buttonGPIO2)
buttonGPIO3Status = Button(buttonGPIO3)

# Record
SAVE_FILE_PATH = '/media/usb3/recordedOverlayVideos'
INTERVALLENGTH = 3 # in seconds
startDateTime = datetime.now()
lastCheckpointDateTime = datetime.now()

# Effect: Starts recording
def cameraRecordStart():
	create_directory()
	days, hours, minutes, seconds = getTimeElapsed()
	camera.start_recording(SAVE_FILE_PATH + "/Elapsed_{:002.0f}".format(seconds) + ".h264")
	print(SAVE_FILE_PATH + "/Elapsed_{:002.0f}".format(seconds) + ".h264")


# Effect: Stops camera recording
def cameraRecordStopAndSave():
	camera.stop_recording()


# Effect: Creates directory
def create_directory():
	PATH = SAVE_FILE_PATH

	if os.path.exists(PATH):
		print("File directory exists")
	else:
		print("File director does not exist, Attempting to create directory")
		try:
			os.mkdir(PATH)
		except OSError:
			print("Creation of the directory %s failed" % PATH)
		else:
			print("Successfully created the directory %s " % PATH)


# Effect: Enable record in x second intervals
def startRecordingIntervals(lengthPerInterval):
	cameraRecordStart()



# TODO: save video and start next video iteration
def timerStart():
	global startTime
	startTime = time.time()


def timerCheck(seconds):
	if time.time() - startTime > seconds * 10 ** 6:
		cameraRecordStopAndSave()


def sufficientTimePassed(lastCheckpointDateTime):
	d,h,m,seconds = getCheckpointTimeElapsed(lastCheckpointDateTime)
	if (seconds > INTERVALLENGTH):
		return True


global serialStatus
serialStatus = ""
print("Start Serial Read")
camera.start_preview()
paintStationaryOverlay()

# cameraRecordStart()

movingOverlayPrev = None
# Grabs the static json
dataLine = DataLine(jsonLine)

recordIntervalFlag = 0
recordContinuousFlag = 0
isRecordingFlag = 0

while True:
	while True:
		try:
			dataLine = readSerialData()
			# ^need to invoke to trigger possible AttributeError
			dataLine.__dict__
			break
		except AttributeError:
			print("AttributeError")
	# print to check values of each line
	# print(dataLine.__dict__)
	# textString = dataLine.__dict__

	# -----Annotated Text functionality (Current decision: Remove)
	# print(str(textString))
	# camera.annotate_text = str(textString)
	# -----Annotated Text functionality (Current decision: Remove)

	paintMovingDisplay(dataLine)


	print("GPIO2 Status is: ", buttonGPIO2Status.value)
	if buttonGPIO2Status.value == 1:
		print("GPIO2 pressed")
		recordIntervalFlag = 1

	print("GPIO3 Status is: ", buttonGPIO2Status.value)
	if buttonGPIO3Status.value == 1:
		print("GPIO3 pressed")
		recordContinuousFlag = 1

	if recordIntervalFlag == 1 and sufficientTimePassed(lastCheckpointDateTime):
		lastCheckpointDateTime = datetime.now()
		try:
			cameraRecordStopAndSave()
		except picamera.exc.PiCameraNotRecording:
			print("no recording exists")
		print("new recording")
		startRecordingIntervals(INTERVALLENGTH)

	if recordContinuousFlag == 1 and isRecordingFlag == 0 and not buttonGPIO3Status.value == 1:
		cameraRecordStart()
		print("Started continuous recording")
		isRecordingFlag = 1
		# recordContinuousFlagPressed = 0

	if recordContinuousFlag == 1 and isRecordingFlag == 1 and not buttonGPIO3Status.value == 1:
		cameraRecordStopAndSave()
		recordContinuousFlag = 0
		isRecordingFlag = 0
