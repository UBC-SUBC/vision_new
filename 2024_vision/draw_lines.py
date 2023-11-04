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

        edges = cv2.Canny(thresh1,50,150,apertureSize = 7)

        #apply hough line transformation 
        lines = cv2.HoughLinesP(edges,1,np.pi/60,100,minLineLength=100,maxLineGap=200)

        #sort 3d array of lines ( very slow ): )
        lines = [x.tolist() for x in lines]
        sorted_lines = sorted(lines, key=lambda x: x[0][1])

        for index, line in enumerate(sorted_lines):
            print(index,line)
            if index == len(sorted_lines)-1:
                break;
            
            refx1,refx2,refy1,refy2 = line[0]
            
            cv2.line(frame, (refx1, refy2), (refx2, refy2), (0, 0, 255), 4)


            x1 = sorted_lines[index][0][0] 
            x2 = sorted_lines[index+1][0][2]
            y1 = sorted_lines[index][0][1]
            y2 = sorted_lines[index+1][0][3]
            


            if abs(y1 - y2) < 10:
                cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 4)
            if abs(x1 - x2) < 10:
                cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 4)

        cv2.imshow('test', frame)
        cv2.waitKey(0)


src = cv2.imread("pool_test.png", cv2.IMREAD_COLOR)
obj1 = LineDetect()
obj1.detect(obj1, src)