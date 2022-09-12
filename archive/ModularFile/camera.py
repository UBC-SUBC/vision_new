from picamera import PiCamera
from variables import CameraVar


class Camera:
    cam = PiCamera()
    def __init__(self) -> None:
        self.initCam()
        
    def initCam(self):
        self.getCam().led = CameraVar.led
        self.getCam().resolution = CameraVar.resolution
        self.getCam().framerate = CameraVar.framerate
        self.getCam().vflip = CameraVar.vflip
        self.getCam().clock_mode = CameraVar.clock_mode
    
    
    def getCam(self):
        return self.cam

    def changeLedStatus(self, led):
        self.getCam().led = led
