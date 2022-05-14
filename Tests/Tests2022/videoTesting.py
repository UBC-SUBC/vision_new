from pathlib import Path
import os
import cv2
import datetime

curr_dir = Path(__file__).parent

output_dir = os.path.join(curr_dir, "test_videos")

try:
    os.mkdir(output_dir)
except:
    pass
cap= cv2.VideoCapture(0)

width= int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height= int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# writer= cv2.VideoWriter(os.path.join(output_dir, 'test_videos.mp4'), cv2.VideoWriter_fourcc(*'DIVX'), 20, (width,height))
writer= cv2.VideoWriter(os.path.join(output_dir, 'test_videos.avi'), cv2.VideoWriter_fourcc('M','J','P','G'), 20, (int(cap.get(3)),int(cap.get(4))))

curr_time = datetime.datetime.now()

while True:
    future_time = datetime.datetime.now()
    if (future_time - curr_time).seconds >= 20*60:
        break
    ret,frame = cap.read()

    writer.write(frame)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break


cap.release()
writer.release()
cv2.destroyAllWindows()
