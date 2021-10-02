import picamera
from PIL import Image, ImageDraw
from time import sleep
import datetime as dt


camera = picamera.PiCamera()
camera.resolution = (1280, 720)
camera.framerate = 24


# # ---Add single image as overlay
# # Load the arbitrarily sized image
# img = Image.open('overlay.png')
# # Create an image padded to the required size with
# # mode 'RGB'
# pad = Image.new('RGBA', (
#     ((img.size[0] + 31) // 32) * 32,
#     ((img.size[1] + 15) // 16) * 16,
#     ))
# # Paste the original image into the padded one
# pad.paste(img, (20, 20))
#
# # Add the overlay with the padded image as the source,
# # but the original image's dimensions
# o = camera.add_overlay(pad.tobytes(), size=img.size)
# # By default, the overlay is in layer 0, beneath the
# # preview (which defaults to layer 2). Here we make
# # the new overlay semi-transparent, then move it above
# # the preview
#
# o.alpha = 128
# o.layer = 3
#
# # ---Add single image as overlay
background = (250,250,250,80)
screenX = int(800)
screenY = int(480)
blankcanvas = Image.new('RGBA',(screenX,screenY), (255,255,255,50))
pitchYawAxisIM = blankcanvas
draw = ImageDraw.Draw(pitchYawAxisIM)
draw.rectangle([0,0,screenX,2*2.5],fill=background)
draw.ellipse((20, 20, 180, 180), fill = background, outline ='blue')
draw.ellipse((20, 20, 180, 180), fill = background, outline ='blue')

camera.start_preview()

stationaryoverlay = camera.add_overlay(pitchYawAxisIM.tobytes(),layer=5, format='rgba')

start_time = dt.datetime.now()


# Wait indefinitely until the user terminates the script
while True:
    camera.annotate_text = "Hello world   " + dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')      # updates to current time






    sleep(1)