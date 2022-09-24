# import the opencv library
import cv2
import json
import numpy as np  


'''

This file contains a class with functions for the LED detection pipeline for SUBC's vision system. 
It is currently configured to read in thresholds from a JSON file and can hold one image within itself at any given time.
TODO: It would be a good idea to implement some sort of scoring algorithm to grade our detection performance. This could
exist as a function in the class and could be re-run with different parameters to track improvements in detection over time.

'''

class ComputerVisionModule():
    lower_bound = int
    upper_bound = int

    latest_image = cv2.Mat
    keypoints = [cv2.KeyPoint]
    line = [float]
    # Constructor for the computer vision module of the code. 
    # Currently set up to take its parameters from a specified JSON file for simple testing of different configurations
    def __init__(self, json_path: str):

        # Load Json file from specified path
        params_json = json.load(open(json_path, 'r'))


        # Define thresholds and parameters relevant to our computer vision pipeline for detecting LEDs
        self.lower_bound = int(params_json['LowerBound'])
        self.upper_bound = int(params_json['UpperBound'])

        self.params = cv2.SimpleBlobDetector_Params()

        self.params.minDistBetweenBlobs = int(params_json['MinDistBetweenBlobs'])
        self.params.filterByInertia = (params_json['FilterByInertia'] == 'True')
        self.params.filterByConvexity = (params_json['FilterByConvexity'] == 'True')
        self.params.filterByColor = (params_json['FilterByColor'] == 'True')
        self.params.filterByCircularity = (params_json['FilterByCircularity'] == 'True')
        self.params.filterByArea = (params_json['FilterByArea'] == 'True')
        self.params.minArea = float(params_json['MinArea'])
        self.params.maxArea = float(params_json['MaxArea'])

    # Loads a new image into the object and over writes the previous one
    def load_new_image(self, image = cv2.Mat):
        self.latest_image = image

    # This function takes a BGR image as its inputs
    # The function returns the location of the detected LEDs and a linear fit of their locations (slope and intercept)
    # TODO: Improve this function by testing it in various lighting situations, this will be the core of our detection pipeline
    def find_LEDs(self):
        self.gray = cv2.cvtColor(self.latest_image, cv2.COLOR_BGR2GRAY)
        self.img_blur = cv2.medianBlur(self.gray, 5)

        # Create a mask of only the colors within the specified gray scale thresholds
        self.mask = cv2.inRange(self.img_blur, self.lower_bound, self.upper_bound)
        self.mask = cv2.bitwise_not(self.mask)

        detector = cv2.SimpleBlobDetector_create(self.params) 
        
        self.keypoints = detector.detect(self.mask)

        self.line = np.polyfit([x.pt[0] for x in self.keypoints], [y.pt[1] for y in self.keypoints], 1)

    def display_image(self):

        # Draw detected blobs as red circles.
        # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
        self.im_with_keypoints = cv2.drawKeypoints(self.latest_image, self.keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        self.im_with_line = cv2.line(self.im_with_keypoints, (int(self.keypoints[0].pt[0]), int(self.keypoints[0].pt[1])),  (int(self.keypoints[len(self.keypoints) - 1].pt[0]), int(self.keypoints[len(self.keypoints) - 1].pt[1])),  (0, 0, 255), 3)
  
         self.im_with_keypoints_rgb = cv2.cvtColor(self.im_with_keypoints, cv2.COLOR_BGR2RGB)     # Show keypoints
        cv2.imshow("Keypoints", self.im_with_line)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

# The following code is commented out so that it can be used when debugging, it creates an instance of the ComputerVisionModule class 
# and runs a single instance of the detection pipeline
# img_processor = ComputerVisionModule(json_path='./JSON/ComputerVision.json')
# img_processor.load_new_image(cv2.imread('./images/IMG_20220912_210543108.jpg'))
# img_processor.find_LEDs()
# img_processor.display_image()