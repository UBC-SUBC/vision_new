from datetime import datetime
import pyautogui

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)

im1 = pyautogui.screenshot()
im1.save("/home/pi/Desktop/PyScreen" + current_time + ".png")