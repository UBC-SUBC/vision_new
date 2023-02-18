# import the opencv library
import cv2
import numpy as np  

def canny(frame):

    # Blur the image for better edge detection

    img_blur = cv2.GaussianBlur(frame, (3,3), 0)       
    # Convert to graycsale
    img_gray = cv2.cvtColor(img_blur, cv2.COLOR_BGR2GRAY)
    #threshold grayscale image to extract glare
    mask1 = cv2.threshold(img_gray, 220, 255, cv2.THRESH_BINARY)[1]
    #inpainting
    result_1 = cv2.inpaint(img_gray, mask1, 21, cv2.INPAINT_TELEA)
    
    max_value = np.max(result_1)
    threshold_value = int(max_value * 0.8)
    mask = cv2.threshold(result_1, threshold_value, 255, cv2.THRESH_BINARY)[1]
    result_2 = cv2.bitwise_and(result_1, result_1, mask=mask)

    # Display Canny Edge Detection Image
    cv2.imshow('Canny Edge Detection',result_2)

# define a video capture object
vid = cv2.VideoCapture("videoplayback.mp4")
  
while(True):
      
    # Capture the video frame
    # by frame
    ret, frame = vid.read()

    canny(frame)
    
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
