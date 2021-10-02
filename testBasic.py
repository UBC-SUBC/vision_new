from picamera import PiCamera
from time import sleep

camera = PiCamera()
#alpha values between 0 - 255, makes preview transparent
camera.start_preview(alpha=200)
sleep(5)
camera.stop_preview()

print("hello")