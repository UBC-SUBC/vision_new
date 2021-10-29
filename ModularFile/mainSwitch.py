from .processedImage import ProcessedImage
from .display import Display
from .variables import DisplayVar


def stationaryLayer() -> Display:
    """Create the layer that is staionary. Contains info about
    yaw pitch, rpm, speed, depth, and all that
    """
    stationaryLayer = Display()
    



def main():
    
    ##Images that we will use
    images = ["warning.png", "lowbatt.png", 
              "sub.png", "highbeams.png"]
    ##Init images and store in dict
    imagesDict = {img.split("", 1)[0]: ProcessedImage(img) for img in images}
    
    pitchYawAxisIM = Display()
    pitchYawAxisIM.drawRectangle(0,0, DisplayVar.screenX, DisplayVar.linegap*2.5,
                                 DisplayVar.background)
    pitchYawAxisIM.drawRectangle
    
    