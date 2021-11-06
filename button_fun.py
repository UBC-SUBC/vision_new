import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(25, GPIO.IN)


while True:
	if GPIO.input(25):
	    print("Pin 22 is HIGH")
	else:
	    print("Pin 22 is LOW")