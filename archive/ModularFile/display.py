from PIL import Image, ImageDraw, ImageFont
from variables import DisplayVar

class Display:
    
    canvas = Image.new('RGBA', (DisplayVar.screenX, DisplayVar.screenY))
    datafont = ImageFont.truetype(DisplayVar.datafontStyleLoc,
                                        DisplayVar.datafontSize)
    smalltextFont = ImageFont.truetype(DisplayVar.smalltextfontStyle,
                                        DisplayVar.smalltextfontSize)
    draw = ImageDraw.Draw(canvas)
       
    def drawRectangle(self, x0, y0, x1, y1, fill):
        self.draw.rectangle([x0,y0, x1, y1], fill=fill)

    def drawLine(self, x0, y0, x1, y1, fill, width):
        self.draw.line([x0,y0, x1, y1], fill=fill, width=width)
    
    
    def drawSmallText(self, x0, y0, value, fill):
        self.draw.text([x0, y0], value, font=self.smalltextFont, fill=fill)
        
    def drawDataText(self, x0, y0, value):
        self.draw.text([x0, y0], value, font=self.datafont,
                       fill=DisplayVar.slidercolor, alin="center")
        
    def drawDataLine(self, x0, y0, x1, y1):
        self.draw.line([x0, y0, x1, y1],
                       fill=DisplayVar.slidercolor,
                       width=DisplayVar.sliderwidth)
    
    def paste(self, img, location):
        self.canvas.paste(img, location)

    def tobytes(self):
        return self.canvas.tobytes()
