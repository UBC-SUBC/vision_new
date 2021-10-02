from picamera import PiCamera
from time import sleep
import os

RECORD_DURATION = 3  # seconds
LOOP_AMOUNT = 3
SAVE_FILE_PATH = '/media/usb3/recordedVideos'
ALT_SAVE_FILE_PATH = '/home/pi/Desktop/video.h264'

camera = PiCamera()


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


def camera_record_once(num):
    camera.start_preview()
    camera.start_recording(SAVE_FILE_PATH + '/video' + str(num) + '.h264')
    sleep(RECORD_DURATION)
    camera.stop_recording()
    camera.stop_preview()


create_directory()
for x in range(LOOP_AMOUNT):
    camera_record_once(x)


