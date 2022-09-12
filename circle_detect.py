# import the opencv library
import cv2
import numpy as np  


class ComputerVisionModule():
    lower_bound = int
    upper_bound = int

    latest_image = cv2.Mat

    keypoints = [cv2.KeyPoint]
    line = [float]

    def __init__(self, lower_bound, upper_bound):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound


    def load_new_image(self, image = cv2.Mat):
        self.latest_image = image

    # This function takes a BGR image as its inputs
    # The function returns the location of the detected LEDs and a linear fit of their locations (slope and intercept)
    # TODO: Improve this function by testing it in various lighting situations, this will be the core of our detection pipeline
    def find_LEDs(self):
        gray = cv2.cvtColor(self.latest_image, cv2.COLOR_BGR2GRAY)
        img_blur = cv2.medianBlur(gray, 5)
        
        # Create the mask
        mask = cv2.inRange(img_blur, self.lower_bound, self.upper_bound)
        mask = cv2.bitwise_not(mask)

        detector = cv2.SimpleBlobDetector_create()

        # Detect blobs.
        self.keypoints = detector.detect(mask)

        self.line = np.polyfit([x.pt[0] for x in self.keypoints], [y.pt[1] for y in self.keypoints], 1)

    def display_image(self):

        # Draw detected blobs as red circles.
        # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
        im_with_keypoints = cv2.drawKeypoints(self.latest_image, self.keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        im_with_line = cv2.line(im_with_keypoints, (int(self.keypoints[0].pt[0]), int(self.keypoints[0].pt[1])),  (int(self.keypoints[len(self.keypoints) - 1].pt[0]), int(self.keypoints[len(self.keypoints) - 1].pt[1])),  (0, 0, 255), 3)

        # Show keypoints
        cv2.imshow("Keypoints", im_with_line)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

# The following code is commented out so that it can be used when debugging, it creates an instance of the ComputerVisionModule class 
# and runs a single instance of the detection pipeline

# img_processor = ComputerVisionModule(lower_bound=200, upper_bound=255)
# img_processor.load_new_image(cv2.imread('org_image.jpg'))
# img_processor.find_LEDs()
# img_processor.display_image()