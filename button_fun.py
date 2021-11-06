import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(25, GPIO.IN)
GPIO.add_event_detect(25, GPIO.RISING, callback=change_step, bouncetime=300)  

step = 1
channel = 25;
count = 0;

def change_step (channel=channel):
	if (step == 1) step = 2
	else step = 1


while True:
	count = count + step
	print(count + "\n")
	time.sleep(1)