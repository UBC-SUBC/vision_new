from PIL import Image
import os
from pathlib import Path
from .variables import ImageVar

class ProcessedImage:
    
    def __init__(self, pathToImage) -> None:
        self.image = Image.open(os.path.join(ImageVar.imagePath, pathToImage))
        self.image.resize(ImageVar.linegap*2, ImageVar.linegap*2.5)
    