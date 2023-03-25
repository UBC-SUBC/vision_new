# import the opencv library
import cv2
import numpy as np  

#Draws a vertical line across the center of an image
#Draws additional vertical lines across areas with streaks
#of bright light
def create_line(img):
    blur = make_gray(img)

    #Apply Canny edge detection to the blurred image:
    edges = cv2.Canny(blur, 50, 150, apertureSize=3)

    #Draw a vertical line across the center of the grayscale image
    height, width = blur.shape
    pos = int(width/2)
    cv2.line(blur, (pos, 0), (pos, height), (0, 0, 0), 2)


    #Apply the Hough transform to the edge-detected image. 
    #Set the theta parameter to 0 degrees to limit the detection 
    #to horizontal lines. You can also experiment with 
    #the minLineLength and maxLineGap parameters to control 
    #the minimum length and gap between lines to be detected:
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, minLineLength=50, maxLineGap=10)

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            if abs(y2 - y1) > abs(x2 - x1):
                cv2.line(blur, (x1, y1), (x2, y2), (0, 255, 0), 2)

    #Return resulting image
    return blur

#Turns the given image into grayscale
def make_gray(img):
     #Convert the image to grayscale:
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img_gray

def calculate_angle(img):
    #Apply edge detection to the grayscale image. 
    #You can use the Canny edge detection 
    #algorithm for this:
    edges = cv2.Canny(img, 50, 150, apertureSize=3)
    
    #Apply the Hough transform to the edge-detected 
    #image to detect the lines:
    lines = cv2.HoughLines(edges, 1, np.pi/180, 200)

    #Find the largest deviation from the vertical angle
    #####However, it only compares the angle between two random lines as of now
    angle_max = 0
    if lines is not None:
        for line in lines:
            for line in lines:
                rho, theta = line[0]
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                x1 = int(x0 + 1000*(-b))
                y1 = int(y0 + 1000*(a))
                x2 = int(x0 - 1000*(-b))
                y2 = int(y0 - 1000*(a))
                cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
    
                # Calculate angle between two lines
                angle_degrees = abs(theta * 180/np.pi)
                
                if angle_degrees % 90 > angle_max % 90:
                    angle_max = angle_degrees
    # Add text to the image with the angle value
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, f"Angle: {angle_max:.2f} deg", (10, 30),
        font, 0.8, (255, 0, 0), 2, cv2.LINE_AA)
    return img

# define a video capture object
vid = cv2.VideoCapture("videoplayback.mp4")
  
while(True):
      
    # Capture the video frame
    # by frame
    ret, frame = vid.read()

    img = create_line(frame)
    angled_img = calculate_angle(img)
    cv2.imshow('Image with Lines and Angle', angled_img)
    
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) == ord('q'):
        break
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
