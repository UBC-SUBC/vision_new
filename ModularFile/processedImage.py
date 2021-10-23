from .mainSwitch import Screen
from PIL import Image
import os
from pathlib import Path

class ProcessedImage:
    imagePath = "Images"
    linegap = int(0.04 * Screen.screenY)
    
    
    def __init__(pathToImage) -> None:
        path