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
        cv2.imshow('test', img_grey)
        cv2.waitKey(0)


src = cv2.imread("edgetest.jpg", cv2.IMREAD_COLOR)
obj1 = LineDetect()
obj1.detect(obj1, src)