import picamera
from PIL import Image, ImageDraw
from time import sleep


with picamera.PiCamera() as camera:
    camera.resolution = (1280, 720)
    camera.framerate = 24
    camera.start_preview()

    # Load the arbitrarily sized image
    img = Image.open('overlay.png')
    # Create an image padded to the required size with
    # mode 'RGB'
    pad = Image.new('RGBA', (
        ((img.size[0] + 31) // 32) * 32,
        ((img.size[1] + 15) // 16) * 16,
        ))
    # Paste the original image into the padded one
    pad.paste(img, (0, 0))

    draw = ImageDraw.Draw(pad)
    draw.rectangle([10,10,200,5*2.5],fill='blue')

    # Add the overlay with the padded image as the source,
    # but the original image's dimensions
    o = camera.add_overlay(pad.tobytes(), size=img.size)
    # By default, the overlay is in layer 0, beneath the
    # preview (which defaults to layer 2). Here we make
    # the new overlay semi-transparent, then move it above
    # the preview
    o.alpha = 128
    o.layer = 3

    # Wait indefinitely until the user terminates the script
#try:
    while True:
        sleep(1)
#runs overlay until keyboard interrup occurs, ctrl+c
#except KeyboardInterrupt:
#    pass
