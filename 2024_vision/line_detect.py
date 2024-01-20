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

        #contrast
        alpha = 1.5 # Contrast control (1.0-3.0)
        beta = 0 # Brightness control (0-100)

        adjusted = cv2.convertScaleAbs(img_grey, alpha=alpha, beta=beta)

        (T, threshInv) = cv2.threshold(adjusted, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
        cv2.imshow("Threshold", threshInv)
        print("[INFO] otsu's thresholding value: {}".format(T))
        # visualize only the masked regions in the image
        # masked = cv2.bitwise_and(frame, frame, mask=threshInv)

        cv2.imshow('Original' , frame)
        cv2.waitKey(0)

src = cv2.imread("pooltest.jpg", cv2.IMREAD_COLOR)
obj1 = LineDetect()
obj1.detect(obj1, src)

