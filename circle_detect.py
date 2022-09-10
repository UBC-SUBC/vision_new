# import the opencv library
import cv2
import numpy as np  
image  = cv2.imread('org_image.jpg')
output = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
img_blur = cv2.medianBlur(gray, 5)
 # define range of white color in HSV
lower_white = 200
upper_white = 255
 
# Create the mask
mask = cv2.inRange(img_blur, lower_white, upper_white)
mask = cv2.bitwise_not(mask)

detector = cv2.SimpleBlobDetector_create()
# Detect blobs.
keypoints = detector.detect(mask)
# keypoints = reversed(keypoints)

line = np.polyfit([x.pt[0] for x in keypoints], [y.pt[1] for y in keypoints], 1)
print(line)
# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
im_with_keypoints = cv2.drawKeypoints(mask, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
# Show keypoints
cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey(0)
