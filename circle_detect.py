# import the opencv library
import cv2
import json
import numpy as np  
import math

'''
This file contains a class with functions for the LED detection pipeline for SUBC's vision system. 
It is currently configured to read in thresholds from a JSON file and can hold one image within itself at any given time.
TODO: It would be a good idea to implement some sort of scoring algorithm to grade our detection performance. This could
exist as a function in the class and could be re-run with different parameters to track improvements in detection over time.
'''

class PIDControllerModule():
    def __init__(self, setpoint, kp, ki, kd, fps):

        self.setpoint = setpoint
        self.kp = kp
        self.ki = ki
        self.kd = kd
        
        self.fps = fps

        self.I_error = 0
        self.P_error = 0
        self.D_error = 0

    def receive_new_process_variables(self, pv):
        last_error = self.P_error
        
        self.P_error = self.setpoint - pv
        self.I_error += self.P_error * (1 / self.fps)

        # Assumption is made that we know the acquiring frame rate, we could also use timestamps with our data
        self.D_error = (self.P_error - last_error) / (1 / self.fps)

        self.PID_result = (self.kp * self.P_error) + (self.ki * self.I_error) + (self.kd * self.D_error)

        print(self.PID_result)



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
        gray = cv2.cvtColor(self.latest_image, cv2.COLOR_BGR2GRAY)
        img_blur = cv2.medianBlur(gray, 3)

        # Create a mask of only the colors within the specified gray scale thresholds
        mask = cv2.inRange(img_blur, self.lower_bound, self.upper_bound)

        lines = cv2.HoughLinesP(mask, 1, np.pi/180, threshold = 100, minLineLength=200, maxLineGap = 3)

        # The below for loop runs till r and theta values
        # are in the range of the 2d array

        if lines is not None:
            theta_list = []

            for points in lines:
                # Extracted points nested in the list
                x1,y1,x2,y2=points[0]

                x_distance = x2 - x1
                y_distance = y2 - y1

                theta = math.atan(x_distance/y_distance)

                theta_list.append(theta)
                # Draw the lines joing the points
                # On the original image
                cv2.line(self.latest_image,(x1,y1),(x2,y2),(0,0,255 ),2)

            self.theta_avg = sum(theta_list)/len(theta_list)
