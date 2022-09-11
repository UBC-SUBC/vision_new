# import the opencv library
import cv2
import numpy as np  

# This function takes a BGR image as its inputs
# The function returns the location of the detected LEDs and a linear fit of their locations (slope and intercept)
# TODO: Improve this function by testing it in various lighting situations, this will be the core of our detection pipeline
def find_LEDs(image = cv2.Mat, lower_bound = int, upper_bound = int):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.medianBlur(gray, 5)
    
    # Create the mask
    mask = cv2.inRange(img_blur, lower_bound, upper_bound)
    mask = cv2.bitwise_not(mask)

    detector = cv2.SimpleBlobDetector_create()

    # Detect blobs.
    keypoints = detector.detect(mask)

    line = np.polyfit([x.pt[0] for x in keypoints], [y.pt[1] for y in keypoints], 1)

    return keypoints, line

# # Example use case for the find_LEDs function (uncomment the code to see the function in action): 
# image  = cv2.imread('org_image.jpg')

# keypoints, line = find_LEDs(image, 200, 255)

# # Draw detected blobs as red circles.
# # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
# im_with_keypoints = cv2.drawKeypoints(image, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# im_with_line = cv2.line(im_with_keypoints, (int(keypoints[0].pt[0]), int(keypoints[0].pt[1])),  (int(keypoints[len(keypoints) - 1].pt[0]), int(keypoints[len(keypoints) - 1].pt[1])),  (0, 0, 255), 3)

# # Show keypoints
# cv2.imshow("Keypoints", im_with_line)
# cv2.waitKey(0)
# cv2.destroyAllWindows()