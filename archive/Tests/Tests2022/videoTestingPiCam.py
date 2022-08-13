from pathlib import Path
import os
import picamera
import datetime

curr_dir = Path(__file__).parent

output_dir = os.path.join(curr_dir, "test_videos")

try:
    os.mkdir(output_dir)
except:
    pass


curr_time = datetime.datetime.now()
with picamera.PiCamera() as camera:
    camera.resolution = (640,480)
    camera.start_preview()
    camera.start_recording(os.path.join(output_dir, "test_vid.h264"))
    camera.wait_recording(10)
    camera.stop_recording()
    camera.stop_preview()



#while True:
 #   if (future_time - curr_time).seconds >= 20*60:
  #      break
   # ret,frame = cap.read()

    #writer.write(frame)

    #cv2.imshow('frame', frame)

    #if cv2.waitKey(1) & 0xFF == 27:
     #   break


#cap.release()
#writer.release()
#cv2.destroyAllWindows()
