import cv2
import numpy as np  

# Open the video file
cap = cv2.VideoCapture('videoplayback.mp4')

# Loop through each frame in the video
while cap.isOpened():
    ret, frame = cap.read()

    # If the video has ended, break the loop
    if not ret:
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    max_value = np.max(gray)
    thres_val = int(max_value*0.75)
    # Apply a threshold to the image
    ret, thresh = cv2.threshold(gray, thres_val, max_value, cv2.THRESH_BINARY)
    #Threshold is set to 200 - Anything below thres will be set to 0
    #Any pixel above 200 will be eset to max_value

    # Display the resulting image
    cv2.imshow('Threshold', thresh)
    delay = 30
    # Wait for a key press to move to the next frame
    if cv2.waitKey(delay) & 0xFF == ord('q'):
        break
# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
