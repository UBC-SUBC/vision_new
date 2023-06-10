import datetime
import logging
import os
import sys
from pathlib import Path
import time

# Add parent to search path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
print(parent_dir)
sys.path.append(parent_dir)

import cv2
import yappi
from arduinoConnector import ArduinoConnector
from PyQt5 import QtCore
from PyQt5.QtCore import QRect, Qt, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import (QBrush, QColor, QFont, QImage, QPainter, QPalette,
                         QPen, QPixmap, QResizeEvent)
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QHBoxLayout,
                             QLabel, QMainWindow, QMenu, QMessageBox,
                             QScrollArea, QSizePolicy, QWidget, qApp)

from Python_DAQ.imu import IMU_module, IMU_module_dummy
from Python_DAQ.depth_sensor import Depth_Sensor, Dummy_Depth_Sensor


#Experimentation with Yappi - python profiler
yappi.set_clock_type("wall")
yappi.start()

#Path(__file__) - file to the current running program 
#mkdir - new path is created 
#joinpath

# New path is created - parent of the current file running joined \ with "logs"

Path.mkdir(Path(__file__).parent.joinpath("logs"), parents=True, exist_ok=True)

# Basic configuration for the logging system 
logging.basicConfig(level=logging.DEBUG,
                    filename= Path(__file__).parent.joinpath('logs/logs_'+str(datetime.datetime.now().strftime("%Y_%m_%d-%I%M%S_%p"))+'.txt'),
                    filemode='a',
                    format='%(levelname)s - %(asctime)s - %(message)s', datefmt="%d-%b-%y %H:%M:%S")


#Worker thread - Recording
#@TODO make the logs function 
#Recording thread - saves frames for video capture
# class RecordThread(QThread):
#     def run(self):
#         #displays current datetime from datetime module 
#         curr_time = datetime.datetime.now()

#         #sets the directory to the parent of the current directory
#         curr_dir = Path(__file__).parent

#         #sets the output directory of recording thread inside "test_videos" of curr_dir
#         output_dir = os.path.join(curr_dir, "test_videos")
        
        
#         #Test creating a new directory with address output_dir. A pass is executed in the case of an exception. 
#         try:
#             os.mkdir(output_dir)
#         #otherwise, the exception is to pass
#         except:
#             pass


#         #Opens a camera for video capture
#         cap = cv2.VideoCapture(-1)
#         # # test whether or not the camera exists, if not reinstantiate it 
#         # while cap.read()[0] == False or not cap.isOpened() or cap is None:
#         #     cap = cv2.VideoCapture(-1)


#         #cv2.CAP_PROP_BUFFERSIZE refers to a property identifier
#         #value of property is 1
#         #sets capture buffersize to 1 - number of samples (corresponds to the amount of time) it takes to handle i/o
#         cap.set(cv2.CAP_PROP_BUFFERSIZE, 1) #buffersize of 1 is speedy? 
#         width= int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) #Width of the frames in the video stream.
#         height= int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) #Height of the frames in the video stream. 
#             # writer = cv2.VideoWriter(os.path.join(output_dir, 'test_videos.mp4'), cv2.VideoWriter_fourcc(*'H264'), 20, (width,height))
            
            
#         # Get a list of all recordings in the folder
#         recordings = os.listdir(output_dir)

#         # Check if there are more than 12 files in the folder
#         if len(recordings) > 12:
#             # Sort the list of files by creation time
#             recordings.sort(key=lambda x: os.path.getctime(os.path.join(output_dir, x)))
#             # Get the oldest file
#             oldest_file = os.path.join(output_dir, recordings[0])
#             # Delete the oldest file
#             os.remove(oldest_file)
        
        
#         # Define the filename format using strftime()
#         filename_format = "%Y-%m-%d_%H-%M-%S"
#         now = datetime.datetime.now().strftime(filename_format)
#         #videoWriter object used to save video captures, 20 frames per second, (framewidth,frameheight)
#         wrtie_to = os.path.abspath(os.path.join(output_dir, f'test_videos_{now}.avi'))
#         print("Writing to: ", wrtie_to)
#         writer= cv2.VideoWriter(wrtie_to , cv2.VideoWriter_fourcc('M','J','P','G'), 20, (int(cap.get(3)),int(cap.get(4))))

#         #Loops over and saves all the frames in a video sequence
#         while True:

#             #ret is a boolean variable that returns true if the frame is available
#             #frame is an image array vector captured based on the default frames
#                 #per second defined
#             #checks if frame is read correctly
#             ret, frame = cap.read() #cap.read() returns a bool T/F
#             #if the frame is read correctly, ret == 1

#             if ret:
# #                future_time = datetime.datetime.now() #future_time refers to current time
#                 #the difference of current time evaluated and previous time when last frame was processed
#                 #if (future_time - curr_time).seconds <= 20*60:
#                 #if (future_time - curr_time).seconds <= 60:
#                     #write frames into videoWriter object

#                 writer.write(frame)
#                 #else:
#                  #   break


# suspect that the camera feed is linear. 
# Displays the frames from RecordThread to video display 
class Thread(QThread):

    changePixmap = pyqtSignal(QImage)

    def run(self):
        curr_time = datetime.datetime.now()
        curr_dir = Path(__file__).parent
        output_dir = os.path.join(curr_dir, "test_videos")
        try:
            os.mkdir(output_dir)
        except:
            pass

        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        width= int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height= int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


        # Get a list of all recordings in the folder
        recordings = os.listdir(output_dir)

        # Check if there are more than 12 files in the folder
        if len(recordings) > 30:
            # Sort the list of files by creation time
            recordings.sort(key=lambda x: os.path.getctime(os.path.join(output_dir, x)))
            # Get the oldest file
            oldest_file = os.path.join(output_dir, recordings[0])
            # Delete the oldest file
            os.remove(oldest_file)


        # Define the filename format using strftime()
        filename_format = "%Y-%m-%d_%H-%M-%S"
        now = datetime.datetime.now().strftime(filename_format)
        #videoWriter object used to save video captures, 20 frames per second, (framewidth,frameheight)
        wrtie_to = os.path.abspath(os.path.join(output_dir, f'test_videos_{now}.avi'))
        print("Writing to: ", wrtie_to)
        writer= cv2.VideoWriter(wrtie_to , cv2.VideoWriter_fourcc('M','J','P','G'), 33, (int(cap.get(3)),int(cap.get(4))))
        ##Sleep to acheive 60fps
        time.sleep(30/1000)
       
        #Loops through frames and processes to display the video on screen
        while True:
            #Returns if the task running on this thread should be stopped
            if self.isInterruptionRequested():
                return

            #checks if frame is properly read correctly
            ret, frame = cap.read()
            if ret:
                #future_time = datetime.datetime.now()
                #if (future_time - curr_time).seconds <= 60:
                writer.write(frame)
                # https://stackoverflow.com/a/55468544/6622587

            #*colour, image formate conversions*
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #applies colour modification on frame (src)
                h, w, ch = rgbImage.shape 
                bytesPerLine = ch * w

                #processing (converting) to Qt format to display the video on interface
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                #scale dimensions 
                p = convertToQtFormat.scaled(contextPerserver.width, contextPerserver.height)
                self.changePixmap.emit(p)

#initiates a window, app begins using multiple threads 
class App(QMainWindow):
    
    def __init__(self, screensize):
        super().__init__()
        self.title = 'SUBC Vision Feed'
        self.screen = QApplication.primaryScreen() 
        self.windowsize = screensize
        self.videoLabel = videoFeed(self)
        self.videoOverlayStatic = videoOverlayStatic(self)
        self.videoOverlayActive = videoOverlayActive(self)
        self.frame_count = 0
        self.threads = []
        self.initUI()
    
    def keyPressEvent(self, event):
        """Close application from escape key.

        results in QMessageBox dialog from closeEvent, good but how/why?
        """
        if event.key() == Qt.Key_Q:
            self.videoLabel.cap.release()
            yappi.stop()
            yappi.get_func_stats().print_all()
            stats = yappi.get_thread_stats()
            stats.sort("name", "ttot").print_all()
            threads = yappi.get_thread_stats()
            # for thread in self.threads:
            #     thread.join()
            #     thread.requestInterruption()
            print('number of theads: ', len(threads))
            for thread in threads:
                print(
                    "Function stats for (%s) (%d)" % (thread.name, thread.id)
                )  # it is the Thread.__class__.__name__
                yappi.get_func_stats(ctx_id=thread.id).print_all()
            self.close()
           
    def get_main_size(self):
        width = self.frameGeometry().width()
        height = self.frameGeometry().height()
        contextPerserver.width = width
        contextPerserver.height = height
        return width, height
    
    @pyqtSlot(QImage)
    def setImage(self, image):
        self.frame_count +=1
        if self.frame_count == 30:
            logging.info(msg = str(datetime.datetime.now()) + ' Counted 30 frames loaded')
            self.frame_count = 0
        # print(self.frame_count)
        self.videoLabel.setPixmap(QPixmap.fromImage(image))
        # self.videoLabel.update()
        # self.videoLabel.setScaledContents(True)


    def initUI(self):
        self.setFixedSize(self.windowsize)
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.FramelessWindowHint)
        logging.info(msg = str(datetime.datetime.now()) + ' Initializing App UI')
        self.setWindowTitle(self.title)
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()

        # commenting out for testing - Arthur
        #th_write = RecordThread(self)
        #th_write.start()
        
        # self.showMaximized()
        self.get_main_size()
        self.setUpVideoFeedUi()
        self.showFullScreen()
        # self.showMaximized()
        # self.show()
        
        
    # def resizeEvent(self, event) -> None:
    #     self.get_main_size()
    #     self.videoLabel.resize(contextPerserver.width, contextPerserver.height)
    #     return super().resizeEvent(event)
    
    
    def setUpVideoFeedUi(self):
        self.topRect = QRect(0, 0, contextPerserver.width, contextPerserver.height)
        self.videoOverlayStatic.setGeometry(self.topRect)
        self.videoLabel.setGeometry(self.topRect)
        self.videoOverlayActive.setGeometry(self.topRect)

#sets up display for text and image
class videoFeed(QLabel):
    frame_count = int(0)
    
    def __init__(self, parent=None):
        QLabel.__init__(self, parent)
    
    def paintEvent(self, event):
        # self.frame_count += 1
        # if self.frame_count == 30:
        #     logging.info(msg = str(datetime.datetime.now()) + ' Counted 30 frames loaded')
        #     self.frame_count = 0
        QLabel.paintEvent(self,event)
        # painter.fillRect(QRect(right_quarter-15, up_quarter, center_square_width*2, down_quarter-up_quarter), Qt.green)


#NOTE: class videoOverlayStatic(Qlabel) handles non-changing components per frame - boarders, text, icons
# class videoOverlayActive(Qlabel) handles components that are updated from data acquisition components, updated per frame - depth, speed, rpm, pitch, yaw


#Contains all the methods related to the static components (i.e. boarders and icons) of the video feed
class videoOverlayStatic(QLabel):
    def __init__(self, parent=None):
        QLabel.__init__(self, parent)

        #applies scaling for boarders per frame 
        self.height_scale = 0.02
        self.width_scale = 0.99
        self.left_quarter = contextPerserver.width * self.height_scale
        self.right_quarter = contextPerserver.width * self.width_scale
        self.up_quarter = contextPerserver.height * self.height_scale
        self.down_quarter = contextPerserver.height * self.width_scale
        self.top_mid_x = (self.left_quarter + self.right_quarter)/2
        self.right_mid_y = (self.up_quarter + self.down_quarter)/2
        self.center_square_width = 10
        self.center_square_height = 30

        #displays battery and highbeam icons
        self.battery_img = QImage(os.path.join(Path(__file__).parent.joinpath("Images"), "highbatt.png"))
        self.beam_img = QImage(os.path.join(Path(__file__).parent.joinpath("Images"), "highbeams.png"))
        self.imu_image = QImage(os.path.join(Path(__file__).parent.joinpath("Images"), "IMU_Warning.png"))
        self.depth_image = QImage(os.path.join(Path(__file__).parent.joinpath("Images"), "depth_sensor_warning.png"))
        self.imu_status = True
        self.depth_status = True
        # print(os.path.join(Path(__file__).parent.parent, "highbatt.png"), "this is loc")
        try:
            IMU_module()
        except:
            self.imu_status = False
        
        try:
            Depth_Sensor()
        except:
            self.depth_status = False
            
        
        # self.yaw = 0
        # self.pitch = 0
        # self.rpm = "0.0"
        # self.speed = "0.0"
        # self.depth = "0.0"
        self.timeBefore = datetime.datetime.now()
    
    # #reads in data from DAQ via outputDict file 
    # def getImu(self):
    #     outputDict = self.imu.outputDict()
    #     self.yaw,self.pitch = outputDict["euler"][0],outputDict["euler"][1]
    #     self.rpm = "99999"
    #     self.speed = "99999"
    #     self.depth = "99999"
    #     logging.info(msg = str(datetime.datetime.now()) + ' JSON Received from Arduino'+str(outputDict))
        
    #set boarder
    def paintOpaque(self, painter):
        painter.save()
        self.top_height = self.up_quarter*3
        right_x = contextPerserver.width-self.left_quarter*2
        self.bot_height = contextPerserver.height -  self.top_height
        painter.setOpacity(0.6)
        painter.setBrush(QBrush(Qt.black))
        painter.setPen(QPen(Qt.transparent))
        painter.drawRect(QRect(0, 0, contextPerserver.width,self.top_height ))
        painter.drawRect(QRect(right_x, self.top_height, contextPerserver.width, self.bot_height))
        painter.drawRect(QRect(0, self.bot_height, right_x, contextPerserver.height))
        painter.restore()
        
    def updateParams(self):
        self.left_quarter = contextPerserver.width * self.height_scale
        self.right_quarter = contextPerserver.width * self.width_scale
        self.up_quarter = contextPerserver.height * self.height_scale
        self.down_quarter = contextPerserver.height * self.width_scale
        self.top_mid_x = (self.left_quarter + self.right_quarter)/2
        self.right_mid_y = (self.up_quarter + self.down_quarter)/2
    
    def paintLines(self, painter):
        painter.save()
        painter.setPen(QPen(Qt.green, 4))
        painter.drawLine(self.left_quarter, self.up_quarter, self.right_quarter, self.up_quarter)
        painter.drawLine(self.right_quarter, self.up_quarter, self.right_quarter, self.down_quarter)
        painter.restore()
    
    
    def paintMidSquares(self, painter):
        painter.save()
        x_off_set = self.center_square_width * 0.5
        y_off_set = self.center_square_height * 0.5
        painter.setPen(QPen(Qt.green, 4))
        painter.translate(-x_off_set, -y_off_set)
        # painter.fillRect(QRect(top_mid_x,self.up_quarter-(center_square_height/2), center_square_width, center_square_height), Qt.green)
        # painter.fillRect(QRect(self.right_quarter-(center_square_height/2),self.right_mid_y, center_square_height,center_square_width), Qt.green)
        painter.fillRect(QRect(self.top_mid_x,self.up_quarter, self.center_square_width, self.center_square_height), Qt.green)
        painter.resetTransform()
        painter.translate(-y_off_set, -x_off_set)
        painter.fillRect(QRect(self.right_quarter,self.right_mid_y, self.center_square_height,self.center_square_width), Qt.green)
        painter.restore()
    
    # #displays the middle squares located at the top and side (pitch and yaw)
    # def paintMovingSquares(self, painter):
    #     painter.save()
    #     x_off_set = self.center_square_width * 0.5q
    #     y_off_set = self.center_square_height * 0.5
    #     painter.setPen(QPen(Qt.black, 4))
    #     painter.translate(-x_off_set, -y_off_set)
    #     painter.fillRect(QRect(self.top_mid_x + (self.yaw/100 * (self.right_quarter-self.top_mid_x)),self.up_quarter, self.center_square_width, self.center_square_height), Qt.black)
    #     painter.resetTransform()
    #     painter.translate(-y_off_set, -x_off_set)
    #     painter.fillRect(QRect(self.right_quarter,self.right_mid_y + (self.pitch/100 * (self.down_quarter- self.right_mid_y)), self.center_square_height,self.center_square_width), Qt.black)
    #     painter.restore()
        
    #text displayer for the icons     
    # def paintText(self, painter):
    #     painter.save()
    #     painter.setPen(QPen(Qt.green, 4))
    #     font_size = max(contextPerserver.width * contextPerserver.height / 69120, 16)
    #     painter.setFont(QFont("times", font_size))
    #     ###Draw the text
    #     #pitch and yaw displayed on top and right side
    #     painter.drawText(QRect(self.left_quarter, self.up_quarter-5, self.right_quarter-self.left_quarter, self.center_square_height*2), 
    #                      QtCore.Qt.AlignCenter , "yaw")
    #     painter.drawText(QRect(self.right_quarter-45, self.up_quarter, self.center_square_width*2, self.down_quarter-self.up_quarter),
    #                      Qt.AlignCenter, "p\ni\nt\nc\nh")
        
    # #     #displays data drawn from DAQ
    # #     painter.setPen(QPen(Qt.blue,4))
    # #     painter.drawText(QRect(contextPerserver.width*0.4, (contextPerserver.height + self.bot_height)/2 , contextPerserver.width, contextPerserver.height-self.bot_height), Qt.AlignLeft,
    # #                      f"RPM:{self.rpm}rpm     Speed:{self.speed}m/s     Depth:{self.depth}m")

    #     # painter.drawText(QRect(contextPerserver.width*0.6, self.bot_height +10, self.right_quarter-self.left_quarter, self.center_square_height*2), "RPM:31 rpm")
    #     # painter.drawText(QRect(contextPerserver.width*0.8, self.bot_height +10, self.right_quarter-self.left_quarter, self.center_square_height*2), "RPM:31 rpm")
        
    #     painter.restore()
    
    def paintImages(self, painter):
        self.battery_img = self.battery_img.scaled(contextPerserver.width*0.04, self.top_height)
        painter.drawPixmap(contextPerserver.width*0.02,self.bot_height, QPixmap.fromImage(self.battery_img))
        
        self.beam_img = self.beam_img.scaled(contextPerserver.width*0.03, self.top_height)
        painter.drawPixmap(contextPerserver.width*0.08,self.bot_height, QPixmap.fromImage(self.beam_img))

        if not self.imu_status:
            self.imu_image = self.imu_image.scaled(contextPerserver.width*0.06, self.top_height)
            painter.drawPixmap(contextPerserver.width*0.12,self.bot_height, QPixmap.fromImage(self.imu_image))

        if not self.depth_status:
            self.depth_image = self.depth_image.scaled(contextPerserver.width*0.06, self.top_height)
            painter.drawPixmap(contextPerserver.width*0.16,self.bot_height, QPixmap.fromImage(self.depth_image))
    
    def paintEvent(self, event):
        QLabel.paintEvent(self,event)
        painter = QPainter(self)
        self.updateParams()
        self.paintOpaque(painter)
        self.paintLines(painter)
        self.paintImages(painter)
        self.paintMidSquares(painter)
        # self.paintMovingSquares(painter)
        # self.paintText(painter) 

        # print(self.left_quarter, self.right_quarter)
        
        # painter.fillRect(QRect(right_quarter-15, up_quarter, center_square_width*2, down_quarter-up_quarter), Qt.green)

# Contains components that are updated from data acquisition (pitch, yaw, rpm, depth, speed), updated per frame in video feed
class videoOverlayActive(QLabel):
    
    def __init__(self, parent=None):
        QLabel.__init__(self, parent)
        self.height_scale = 0.02
        self.width_scale = 0.99
        self.left_quarter = contextPerserver.width * self.height_scale
        self.right_quarter = contextPerserver.width * self.width_scale
        self.up_quarter = contextPerserver.height * self.height_scale
        self.down_quarter = contextPerserver.height * self.width_scale
        self.top_mid_x = (self.left_quarter + self.right_quarter)/2
        self.right_mid_y = (self.up_quarter + self.down_quarter)/2
        self.top_height = self.up_quarter*3
        self.bot_height = contextPerserver.height -  self.top_height
        self.center_square_width = 10
        self.center_square_height = 30
        self.battery_img = QImage(os.path.join(Path(__file__).parent.parent, "highbatt.png"))
        self.beam_img = QImage(os.path.join(Path(__file__).parent.parent, "highbeams.png"))
        # print(os.path.join(Path(__file__).parent.parent, "highbatt.png"), "this is loc")
        
        ## This try except block is to let you still be able to boot up the UI despite not having circuit python installed
        try:
            self.imu = IMU_module()
        except Exception as e:
            print(e)
            self.imu = IMU_module_dummy()
        
        try:
            self.depth_sensor = Depth_Sensor()
        except Exception as e:
            print(e)
            self.depth_sensor = Dummy_Depth_Sensor()
        
        self.yaw = 0
        self.pitch = 0
        self.rpm = "0.0"
        self.speed = "0.0"
        self.salt_depth = 0
        self.fresh_depth = 0
        # self.timeBefore = datetime.datetime.now()
        self.imu_fetch_counter = 0
    def getImu(self):
        outputDict = self.imu.outputDict()
        self.yaw,self.pitch = outputDict["euler"][0],outputDict["euler"][1]
        print(f"RAW Yaw is {self.yaw}, RAW pitch is {self.pitch}")
        
        ## Convert to plotting size
        ## Range of self.yaw is 0-360 turinig clockwise increases
        if self.yaw is not None:
            ## We want 3rd and 4th quadrant to be negative and 1st and 2nd quadrant to be postitive
            self.yaw = self.yaw - 360 if self.yaw > 180 else self.yaw
            
            ## Only reserve the last 20% for greater than 90 degrees (should be impossible)
            if abs(self.yaw) <= 90:
                self.yaw = self.yaw/90 * 0.8
            else:
                ## Find how my of the 2nd and 3rd quarant yaw fills up, then apply scaling
                self.yaw = self.yaw/2
                self.yaw = self.yaw/90 * 0.2
                self.yaw = 0.8 + self.yaw if self.yaw > 0 else -0.8 + self.yaw
            
        
        ## Covert to pitch plotting size
        ## Range of self.pitch is -180 to 180 increase with inclination
        if self.pitch is not None:
            self.pitch = -self.pitch/90 ## This is assuming we will not go over 90 degrees. Because if we do, we screwed up
        
        ## Don't crash the ui
        self.yaw = 0 if self.yaw is None else self.yaw
        self.pitch = 0 if self.pitch is None else self.pitch
        
        print(f"Yaw is {self.yaw}, pitch is {self.pitch}")
        self.rpm = "9999"
        self.speed = "9999"
        logging.info(msg = str(datetime.datetime.now()) + ' JSON Received from Arduino')
        
    def getDepth(self):
        self.salt_depth , self.fresh_depth = round(self.depth_sensor.outputDict()["salt_depth"],2), round(self.depth_sensor.outputDict()["fresh_depth"],2)
    # def paintOpaque(self, painter):
    #     painter.save()
    #     self.top_height = self.up_quarter*3
    #     right_x = contextPerserver.width-self.left_quarter*2
    #     self.bot_height = contextPerserver.height -  self.top_height
    #     painter.setOpacity(0.3)
    #     painter.setBrush(QBrush(Qt.black))
    #     painter.setPen(QPen(Qt.transparent))
    #     painter.drawRect(QRect(0, 0, contextPerserver.width,self.top_height ))
    #     painter.drawRect(QRect(right_x, self.top_height, contextPerserver.width, self.bot_height))
    #     painter.drawRect(QRect(0, self.bot_height, right_x, contextPerserver.height))
    #     painter.restore()
        
    def updateParams(self):
        self.left_quarter = contextPerserver.width * self.height_scale
        self.right_quarter = contextPerserver.width * self.width_scale
        self.up_quarter = contextPerserver.height * self.height_scale
        self.down_quarter = contextPerserver.height * self.width_scale
        self.top_mid_x = (self.left_quarter + self.right_quarter)/2
        self.right_mid_y = (self.up_quarter + self.down_quarter)/2
        self.top_height = self.up_quarter*3
        self.bot_height = contextPerserver.height -  self.top_height
    # def paintLines(self, painter):
    #     painter.save()
    #     painter.setPen(QPen(Qt.green, 4))
    #     painter.drawLine(self.left_quarter, self.up_quarter, self.right_quarter, self.up_quarter)
    #     painter.drawLine(self.right_quarter, self.up_quarter, self.right_quarter, self.down_quarter)
    #     painter.restore()
    
    # def paintMidSquares(self, painter):
    #     painter.save()
    #     x_off_set = self.center_square_width * 0.5
    #     y_off_set = self.center_square_height * 0.5
    #     painter.setPen(QPen(Qt.green, 4))
    #     painter.translate(-x_off_set, -y_off_set)
    #     # painter.fillRect(QRect(top_mid_x,self.up_quarter-(center_square_height/2), center_square_width, center_square_height), Qt.green)
    #     # painter.fillRect(QRect(self.right_quarter-(center_square_height/2),self.right_mid_y, center_square_height,center_square_width), Qt.green)
    #     painter.fillRect(QRect(self.top_mid_x,self.up_quarter, self.center_square_width, self.center_square_height), Qt.green)
    #     painter.resetTransform()
    #     painter.translate(-y_off_set, -x_off_set)
    #     painter.fillRect(QRect(self.right_quarter,self.right_mid_y, self.center_square_height,self.center_square_width), Qt.green)
    #     painter.restore()
    
    def paintMovingSquares(self, painter):
        painter.save()
        x_off_set = self.center_square_width * 0.5
        y_off_set = self.center_square_height * 0.5
        painter.setPen(QPen(Qt.black, 4))
        painter.translate(-x_off_set, -y_off_set)
        painter.fillRect(QRect(self.top_mid_x + (self.yaw * (self.right_quarter-self.top_mid_x)),self.up_quarter, self.center_square_width, self.center_square_height), Qt.blue)
        painter.resetTransform()
        painter.translate(-y_off_set, -x_off_set)
        painter.fillRect(QRect(self.right_quarter,self.right_mid_y + (self.pitch * (self.down_quarter- self.right_mid_y)), self.center_square_height,self.center_square_width), Qt.blue)
        painter.restore()
        
        
    def paintText(self, painter):
        painter.save()
        painter.setPen(QPen(Qt.green, 4))
        font_size = max(contextPerserver.width * contextPerserver.height / 69120, 16)
        painter.setFont(QFont("times", font_size))
        ###Draw the text
        painter.drawText(QRect(self.left_quarter, self.up_quarter-5, self.right_quarter-self.left_quarter, self.center_square_height*2), 
                         QtCore.Qt.AlignCenter , "yaw")
        painter.drawText(QRect(self.right_quarter-35, self.up_quarter, self.center_square_width*2, self.down_quarter-self.up_quarter),
                         Qt.AlignCenter, "p\ni\nt\nc\nh")
        
        painter.setPen(QPen(Qt.green,4))
        # painter.drawText(QRect(contextPerserver.width*0.4, (contextPerserver.height + self.bot_height)/2 , 
        #                        contextPerserver.width, contextPerserver.height-self.bot_height), Qt.AlignLeft, 
        #                  f"RPM:{self.rpm}rpm     Speed:{self.speed}m/s     Salt depth:{self.salt_depth}m     Fresh depth:{self.fresh_depth}m")
        painter.drawText(QRect(contextPerserver.width*0.25, (contextPerserver.height - 2.1*self.up_quarter) , 
                               contextPerserver.width, contextPerserver.height-self.bot_height), Qt.AlignLeft, 
                         f"RPM:{self.rpm}rpm     Speed:{self.speed}m/s     Salt depth:{self.salt_depth}m     Fresh depth:{self.fresh_depth}m")

        # painter.drawText(QRect(contextPerserver.width*0.6, self.bot_height +10, self.right_quarter-self.left_quarter, self.center_square_height*2), "RPM:31 rpm")
        # painter.drawText(QRect(contextPerserver.width*0.8, self.bot_height +10, self.right_quarter-self.left_quarter, self.center_square_height*2), "RPM:31 rpm")
        
        painter.restore()
    
    def paintImages(self, painter):
        self.battery_img = self.battery_img.scaled(contextPerserver.width*0.04, self.top_height)
        painter.drawPixmap(contextPerserver.width*0.02,self.bot_height, QPixmap.fromImage(self.battery_img))
        
        self.beam_img = self.beam_img.scaled(contextPerserver.width*0.03, self.top_height)
        painter.drawPixmap(contextPerserver.width*0.08,self.bot_height, QPixmap.fromImage(self.beam_img))

    # def checkTime(self):
    #     time_now = datetime.datetime.now()
    #     logging.info(msg = "Time now========" + str(time_now))
    #     logging.info(msg = "seconds" + str( time_now - self.timeBefore))
    #     if (time_now - self.timeBefore).seconds > 1:
    #         print("getting  it")
    #         logging.info(msg = "getting it")
            
    #         self.timeBefore = time_now
    #         return True 
    #     print("Time before========", self.timeBefore)
    #     return False
    
    def paintEvent(self, event):
        # self.frame_count += 1
        # if self.frame_count == 30:
        #     logging.info(msg = str(datetime.datetime.now()) + ' Counted 30 frames loaded')
        #     self.frame_count = 0
        QLabel.paintEvent(self,event)
        painter = QPainter(self)
        # print(self.checkTime(), "curr time========")
        if self.imu_fetch_counter >= 5:
            print(self.imu_fetch_counter)
            self.imu_fetch_counter = 0
            self.getImu()
            self.getDepth()
        self.imu_fetch_counter += 1
        self.updateParams()
        # print("updating")
        # self.paintOpaque(painter)
        # self.paintLines(painter)
        # self.paintImages(painter)
        # self.paintMidSquares(painter)
        self.paintMovingSquares(painter)
        self.paintText(painter) #TODO: fix paintText function

        # print(self.left_quarter, self.right_quarter)
        
        # painter.fillRect(QRect(right_quarter-15, up_quarter, center_square_width*2, down_quarter-up_quarter), Qt.green)

class contextPerserver():
    width = 0
    height = 0

if __name__ == '__main__':
    app = QApplication(sys.argv)
    screensize = app.desktop().availableGeometry().size()

    ex = App(screensize)
    sys.exit(app.exec_())
