# import opencv library
import cv2
import json
import numpy as np

'''

'''


class LineDetect:
    def __int__(self):
        pass

    @staticmethod
    def detect(self, frame):
        # convert to greyscale
        img_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        img_blur = cv2.GaussianBlur(img_grey, (3, 3), 0)
        # apply Otsu thresholding to highlight black as white
        ret, thresh1 = cv2.threshold(img_blur,81, 255, cv2.THRESH_BINARY_INV)
        # apply Canny for edge detection
        cv2.imshow('test', thresh1)
        cv2.waitKey(0)


src = cv2.imread("pool_test.png", cv2.IMREAD_COLOR)
obj1 = LineDetect()
obj1.detect(obj1, src)