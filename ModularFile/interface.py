from PIL import Image, ImageDraw, ImageFont

class interFace:
    #setup display variables
    screenX =  int(1280)
    screenY =  int(720)
    #creating blank image canvas and fonts dat
    datafont = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",20)
    smalltextfont = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",8)
    blankcanvas = Image.new('RGBA',(screenX,screenY))