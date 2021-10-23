from picamera import PiCamera

class Camera:
    screenX =  int(1280)
    screenY =  int(720) #camera is also recording at this res
    screenFramrate = 30
    cam = PiCamera()
    cam.led = True
    cam.resolution = (screenX, screenY)
    cam.framerate = screenFramrate
    cam.vflip = True
    cam.clock_mode="reset"