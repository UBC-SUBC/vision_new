from PIL import Image, ImageDraw, ImageFont
from .variables import DisplayVar

class Display:
    
    def __init__(self) -> None:
        canvas = Image.new('RGBA', (DisplayVar.screenX, DisplayVar.screenY))
        datafont = ImageFont.truetype(Display.datafontStyleLoc,
                                            DisplayVar.datafontSize)
        smalltextFont = ImageFont.truetype(DisplayVar.smalltextfontStyle,
                                           DisplayVar.smalltextfontSize)
        draw = ImageDraw.Draw(canvas)
    
    def drawRectangle(self, x0, y0, x1, y1, fill):
        self.draw.rectangle([x0,y0, x1, y1], fill=fill)
    
        
    def drawLine(self, x0, y0, x1, y1, fill, width):
        self.draw.line([x0,y0, x1, y1], fill=fill, width=width)
    
    
    def drawText(self, x0, y0, x1, y1, font, fill):
        self.draw.text([x0, y0, x1, y1], font=font, fill=fill)
        
        
    
        
        