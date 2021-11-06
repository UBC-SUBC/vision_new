import RPi.GPIO as GPIO
import time

step = 1
channel = 25
count = 0


GPIO.setmode(GPIO.BCM)

GPIO.setup(25, GPIO.IN)

def change_step (channel=channel):
	global step
	print("Entered callback")
	if (step == 1): step = 2
	elif (step == 2): step = 1
	else: step = step


GPIO.add_event_detect(25, GPIO.RISING, callback=change_step, bouncetime=300)  


while True:
	count = count + step
	print(str(count) + "\n")
	time.sleep(1)