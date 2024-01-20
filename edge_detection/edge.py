# import the opencv library
import cv2
import numpy as np
import cv2 as cv2

def canny(frame):
    # Convert to graycsale
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Blur the image for better edge detection
    img_blur = cv2.GaussianBlur(img_gray, (3,3), 0)

    #Applys Laplacian on image 
    img_laplace = cv2.Laplacian(img_blur,ddepth=-1,scale=1,delta=0,borderType=cv2.BORDER_DEFAULT)

    # Canny Edge Detection
    sigma = np.std(img_laplace)
    mean = np.mean(img_laplace)
    lower = int(max(0, (mean - sigma)))
    upper = int(min(255, (mean + sigma)))

    edges = cv2.Canny(image=img_blur, threshold1=lower, threshold2=upper) # Canny Edge Detection
    edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)  #convert canny image to bgr
    #edges *= np.array((0,0,1),np.uint8)
    #cv2.line(edges, (50, 100), (150, 100), (255,255,255), 1)
    #add_weight = cv2.addWeighted( frame, 0.5, edges, 0.5, 0.0) # blend src image with canny image
    new_image = cv2.add(frame, edges) # add src image with canny image

#Experimentation: add special filters
#Add a Laplacian Filter to enhance edge detection
    img_test = cv2.Laplacian(new_image,ksize=3, ddepth=-1)

    # Display Canny Edge Detection Image
    cv2.imshow('Canny Edge Detection',img_test)

# define a video capture object
# vid = cv2.VideoCapture("videoplayback.mp4")
  
# while(True):
      
#     # Capture the video frame
#     # by frame
#     ret, frame = vid.read()
  
#     # Display the resulting frame
#     cv2.imshow('frame', frame)

#     canny(frame)
    
#     # the 'q' button is set as the
#     # quitting button you may use any
#     # desired button of your choice
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
  
# # After the loop release the cap object
# vid.release()
# # Destroy all the windows
# cv2.destroyAllWindows()

src = cv2.imread("pooltest.jpg", cv2.IMREAD_COLOR)

img_grey = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

#contrast
alpha = 1.5 # Contrast control (1.0-3.0)
beta = 0 # Brightness control (0-100)

adjusted = cv2.convertScaleAbs(img_grey, alpha=alpha, beta=beta)

(T, threshInv) = cv2.threshold(adjusted, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
cv2.imshow("Threshold", threshInv)
print("[INFO] otsu's thresholding value: {}".format(T))
# visualize only the masked regions in the image
# masked = cv2.bitwise_and(frame, frame, mask=threshInv)

cv2.imshow('Original' , src)
cv2.waitKey(0)

canny(src)
cv2.imshow('Canny' , src)
cv2.waitKey(0)
