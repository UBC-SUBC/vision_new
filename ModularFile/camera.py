from picamera import PiCamera
from .variables import CameraVar


class Camera:
    
    def __init__(self) -> None:
        cam = PiCamera()
        self.initCam()
        
    def initCam(self):
        self.cam.led = CameraVar.led
        self.cam.resolution = CameraVar.resolution
        self.cam.framerate = CameraVar.framerate
        self.cam.vflip = CameraVar.vflip
        self.clock_mode = CameraVar.clock_mode

    def getCam(self):
        return self.cam

    def changeLedStatus(self, led):
        self.cam.led = led
