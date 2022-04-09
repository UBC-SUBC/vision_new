import cv2
import sys
from PyQt5.QtWidgets import QWidget, QLabel, QApplication
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot, QRect
from PyQt5 import QtCore
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap, QPalette, QPainter, QPen, QFont,QResizeEvent, QBrush, QColor
from PyQt5.QtWidgets import QLabel, QSizePolicy, QScrollArea, QMessageBox, QMainWindow, QMenu, QAction, \
    qApp, QFileDialog, QHBoxLayout
import logging
from pathlib import Path
import os
from arduinoConnector import ArduinoConnector
import datetime

Path.mkdir(Path(__file__).parent.joinpath("logs"), parents=True, exist_ok=True)
logging.basicConfig(level=logging.DEBUG,
                    filename= Path(__file__).parent.joinpath('logs/logs_'+str(datetime.datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p"))+'.txt'),
                    filemode='a',
                    format='%(levelname)s - %(asctime)s - %(message)s', datefmt="%d-%b-%y %H:%M:%S")
#@TODO make the logs function


class RecordThread(QThread):
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
        # writer = cv2.VideoWriter(os.path.join(output_dir, 'test_videos.mp4'), cv2.VideoWriter_fourcc(*'H264'), 20, (width,height))
        writer= cv2.VideoWriter(os.path.join(output_dir, 'test_videos.avi'), cv2.VideoWriter_fourcc('M','J','P','G'), 20, (int(cap.get(3)),int(cap.get(4))))
        
        while True:
            ret, frame = cap.read()
            if ret:
                future_time = datetime.datetime.now()
                if (future_time - curr_time).seconds <= 20*60:
                    writer.write(frame)
                else:
                    break

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    
    # def __init__(self, app):
    #     super(QThread, self).__init__()
    #     self.app = app
        
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
        # writer = cv2.VideoWriter(os.path.join(output_dir, 'test_videos.mp4'), cv2.VideoWriter_fourcc(*'H264'), 20, (width,height))
        writer= cv2.VideoWriter(os.path.join(output_dir, 'test_videos.avi'), cv2.VideoWriter_fourcc('M','J','P','G'), 20, (int(cap.get(3)),int(cap.get(4))))
        
        while True:
            ret, frame = cap.read()
            if ret:
                future_time = datetime.datetime.now()
                if (future_time - curr_time).seconds <= 20*60:
                    writer.write(frame)
                # https://stackoverflow.com/a/55468544/6622587
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                # print(contextPerserver.width, contextPerserver.height)
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(contextPerserver.width, contextPerserver.height)
                # writer.write(frame)
                self.changePixmap.emit(p)
                
                    
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
        self.initUI()
    
    def keyPressEvent(self, event):
        """Close application from escape key.

        results in QMessageBox dialog from closeEvent, good but how/why?
        """
        if event.key() == Qt.Key_Q:
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
        
        th_write = RecordThread(self)
        th_write.start()
        
        # self.showMaximized()
        self.get_main_size()
        self.setUpVideoFeedUi()
        self.show()
        
        
    # def resizeEvent(self, event) -> None:
    #     self.get_main_size()
    #     self.videoLabel.resize(contextPerserver.width, contextPerserver.height)
    #     return super().resizeEvent(event)
    
    def setUpVideoFeedUi(self):
        self.topRect = QRect(0, 0, contextPerserver.width, contextPerserver.height)
        self.videoOverlayStatic.setGeometry(self.topRect)
        self.videoLabel.setGeometry(self.topRect)
        self.videoOverlayActive.setGeometry(self.topRect)
    
    
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
    
class videoOverlayStatic(QLabel):
    
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
        self.center_square_width = 10
        self.center_square_height = 30
        self.battery_img = QImage(os.path.join(Path(__file__).parent.parent, "highbatt.png"))
        self.beam_img = QImage(os.path.join(Path(__file__).parent.parent, "highbeams.png"))
        # print(os.path.join(Path(__file__).parent.parent, "highbatt.png"), "this is loc")
        self.arduino = ArduinoConnector()
        self.yaw = 0
        self.pitch = 0
        self.rpm = "0.0"
        self.speed = "0.0"
        self.depth = "0.0"
        self.timeBefore = datetime.datetime.now()
        
    def getArduino(self):
        json = self.arduino.readJsonFromArduino()
        self.yaw = json["yaw"]
        self.pitch = json["pitch"]
        self.rpm = json["rpm"]
        self.speed = json["speed"]
        self.depth = json["depth"]
        logging.info(msg = str(datetime.datetime.now()) + ' JSON Received from Arduino')
        
    
    def paintOpaque(self, painter):
        painter.save()
        self.top_height = self.up_quarter*3
        right_x = contextPerserver.width-self.left_quarter*2
        self.bot_height = contextPerserver.height -  self.top_height
        painter.setOpacity(0.3)
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
    
    def paintMovingSquares(self, painter):
        painter.save()
        x_off_set = self.center_square_width * 0.5
        y_off_set = self.center_square_height * 0.5
        painter.setPen(QPen(Qt.black, 4))
        painter.translate(-x_off_set, -y_off_set)
        painter.fillRect(QRect(self.top_mid_x + (self.yaw/100 * (self.right_quarter-self.top_mid_x)),self.up_quarter, self.center_square_width, self.center_square_height), Qt.black)
        painter.resetTransform()
        painter.translate(-y_off_set, -x_off_set)
        painter.fillRect(QRect(self.right_quarter,self.right_mid_y + (self.pitch/100 * (self.down_quarter- self.right_mid_y)), self.center_square_height,self.center_square_width), Qt.black)
        painter.restore()
        
        
    def paintText(self, painter):
        painter.save()
        painter.setPen(QPen(Qt.green, 4))
        font_size = max(contextPerserver.width * contextPerserver.height / 69120, 16)
        painter.setFont(QFont("times", font_size))
        ###Draw the text
        painter.drawText(QRect(self.left_quarter, self.up_quarter-5, self.right_quarter-self.left_quarter, self.center_square_height*2), 
                         QtCore.Qt.AlignCenter , "yaw")
        painter.drawText(QRect(self.right_quarter-45, self.up_quarter, self.center_square_width*2, self.down_quarter-self.up_quarter),
                         Qt.AlignCenter, "p\ni\nt\nc\nh")
        
        painter.setPen(QPen(Qt.blue,4))
        painter.drawText(QRect(contextPerserver.width*0.4, (contextPerserver.height + self.bot_height)/2 , contextPerserver.width, contextPerserver.height-self.bot_height), Qt.AlignLeft,
                         f"RPM:{self.rpm}rpm     Speed:{self.speed}m/s     Depth:{self.depth}m")

        # painter.drawText(QRect(contextPerserver.width*0.6, self.bot_height +10, self.right_quarter-self.left_quarter, self.center_square_height*2), "RPM:31 rpm")
        # painter.drawText(QRect(contextPerserver.width*0.8, self.bot_height +10, self.right_quarter-self.left_quarter, self.center_square_height*2), "RPM:31 rpm")
        
        painter.restore()
    
    def paintImages(self, painter):
        self.battery_img = self.battery_img.scaled(contextPerserver.width*0.04, self.top_height)
        painter.drawPixmap(contextPerserver.width*0.02,self.bot_height, QPixmap.fromImage(self.battery_img))
        
        self.beam_img = self.beam_img.scaled(contextPerserver.width*0.03, self.top_height)
        painter.drawPixmap(contextPerserver.width*0.08,self.bot_height, QPixmap.fromImage(self.beam_img))
    
    def checkTime(self):
        time_now = datetime.datetime.now()
        if (time_now - self.timeBefore).seconds > 1:
            self.timeBefore = time_now
            return True 
        return False
    
    def paintEvent(self, event):
        QLabel.paintEvent(self,event)
        painter = QPainter(self)
        self.updateParams()
        self.paintOpaque(painter)
        self.paintLines(painter)
        self.paintImages(painter)
        self.paintMidSquares(painter)
        self.paintMovingSquares(painter)
        self.paintText(painter) 

        print(self.left_quarter, self.right_quarter)
        
        # painter.fillRect(QRect(right_quarter-15, up_quarter, center_square_width*2, down_quarter-up_quarter), Qt.green)

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
        self.center_square_width = 10
        self.center_square_height = 30
        self.battery_img = QImage(os.path.join(Path(__file__).parent.parent, "highbatt.png"))
        self.beam_img = QImage(os.path.join(Path(__file__).parent.parent, "highbeams.png"))
        # print(os.path.join(Path(__file__).parent.parent, "highbatt.png"), "this is loc")
        self.arduino = ArduinoConnector()
        self.yaw = 0
        self.pitch = 0
        self.rpm = "0.0"
        self.speed = "0.0"
        self.depth = "0.0"
        self.timeBefore = datetime.datetime.now()
        
    def getArduino(self):
        json = self.arduino.readJsonFromArduino()
        self.yaw = json["yaw"]
        self.pitch = json["pitch"]
        self.rpm = json["rpm"]
        self.speed = json["speed"]
        self.depth = json["depth"]
        logging.info(msg = str(datetime.datetime.now()) + ' JSON Received from Arduino')
        
    
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
        painter.fillRect(QRect(self.top_mid_x + (self.yaw/100 * (self.right_quarter-self.top_mid_x)),self.up_quarter, self.center_square_width, self.center_square_height), Qt.black)
        painter.resetTransform()
        painter.translate(-y_off_set, -x_off_set)
        painter.fillRect(QRect(self.right_quarter,self.right_mid_y + (self.pitch/100 * (self.down_quarter- self.right_mid_y)), self.center_square_height,self.center_square_width), Qt.black)
        painter.restore()
        
        
    def paintText(self, painter):
        painter.save()
        painter.setPen(QPen(Qt.green, 4))
        font_size = max(contextPerserver.width * contextPerserver.height / 69120, 16)
        painter.setFont(QFont("times", font_size))
        ###Draw the text
        painter.drawText(QRect(self.left_quarter, self.up_quarter-5, self.right_quarter-self.left_quarter, self.center_square_height*2), 
                         QtCore.Qt.AlignCenter , "yaw")
        painter.drawText(QRect(self.right_quarter-45, self.up_quarter, self.center_square_width*2, self.down_quarter-self.up_quarter),
                         Qt.AlignCenter, "p\ni\nt\nc\nh")
        
        painter.setPen(QPen(Qt.blue,4))
        painter.drawText(QRect(contextPerserver.width*0.4, (contextPerserver.height + self.bot_height)/2 , contextPerserver.width, contextPerserver.height-self.bot_height), Qt.AlignLeft,
                         f"RPM:{self.rpm}rpm     Speed:{self.speed}m/s     Depth:{self.depth}m")

        # painter.drawText(QRect(contextPerserver.width*0.6, self.bot_height +10, self.right_quarter-self.left_quarter, self.center_square_height*2), "RPM:31 rpm")
        # painter.drawText(QRect(contextPerserver.width*0.8, self.bot_height +10, self.right_quarter-self.left_quarter, self.center_square_height*2), "RPM:31 rpm")
        
        painter.restore()
    
    def paintImages(self, painter):
        self.battery_img = self.battery_img.scaled(contextPerserver.width*0.04, self.top_height)
        painter.drawPixmap(contextPerserver.width*0.02,self.bot_height, QPixmap.fromImage(self.battery_img))
        
        self.beam_img = self.beam_img.scaled(contextPerserver.width*0.03, self.top_height)
        painter.drawPixmap(contextPerserver.width*0.08,self.bot_height, QPixmap.fromImage(self.beam_img))
    
    def checkTime(self):
        time_now = datetime.datetime.now()
        if (time_now - self.timeBefore).seconds > 1:
            self.timeBefore = time_now
            return True 
        return False
    
    def paintEvent(self, event):
        # self.frame_count += 1
        # if self.frame_count == 30:
        #     logging.info(msg = str(datetime.datetime.now()) + ' Counted 30 frames loaded')
        #     self.frame_count = 0
        QLabel.paintEvent(self,event)
        painter = QPainter(self)
        if self.checkTime():
            self.getArduino()
        self.updateParams()
        # self.paintOpaque(painter)
        # self.paintLines(painter)
        # self.paintImages(painter)
        # self.paintMidSquares(painter)
        self.paintMovingSquares(painter)
        # self.paintText(painter) 

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
