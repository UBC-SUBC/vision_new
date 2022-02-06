from glob import glob
import cv2
import sys
from PyQt5.QtWidgets import QWidget, QLabel, QApplication
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot, QRect
from PyQt5 import QtCore
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap, QPalette, QPainter, QPen, QFont
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtWidgets import QLabel, QSizePolicy, QScrollArea, QMessageBox, QMainWindow, QMenu, QAction, \
    qApp, QFileDialog, QHBoxLayout


class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    
    # def __init__(self, app):
    #     super(QThread, self).__init__()
    #     self.app = app
        
    def run(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if ret:
                # https://stackoverflow.com/a/55468544/6622587
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(contextPerserver.width, contextPerserver.height, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
                
class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'SUBC Vision Feed'
        self.screen = QApplication.primaryScreen()
        self.videoLabel = videoFeed(self)
        self.initUI()
        
        
    def get_main_size(self):
        width = self.frameGeometry().width()
        height = self.frameGeometry().height()
        contextPerserver.width = width
        contextPerserver.height = height
        return width, height
    
    @pyqtSlot(QImage)
    def setImage(self, image):
        self.videoLabel.setPixmap(QPixmap.fromImage(image))

    def initUI(self):
        self.setWindowTitle(self.title)
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()

        self.showMaximized()
        self.get_main_size()
        self.setUpVideoFeedUi()
        
    
    def setUpVideoFeedUi(self):
        self.topRect = QRect(0, 0, contextPerserver.width, contextPerserver.height)
        self.videoLabel.setGeometry(self.topRect)
    
    
class videoFeed(QLabel):
    def __init__(self, parent=None):
        QLabel.__init__(self, parent)
        
    def paintEvent(self, event):
        QLabel.paintEvent(self, event)
        painter = QPainter(self)
        painter.setPen(QPen(Qt.green, 4))
        # print(contextPerserver.height, contextPerserver.width)
        left_quarter = contextPerserver.width * 0.04
 
        right_quarter = contextPerserver.width * 0.96
        up_quarter = contextPerserver.height * 0.04
        down_quarter = contextPerserver.height * 0.96
        top_mid_x = (left_quarter + right_quarter)/2
        right_mid_y = (up_quarter + down_quarter)/2
        center_square_width = 20
        center_square_height = 20
        print(left_quarter, right_quarter)   
        painter.drawLine(left_quarter, up_quarter, right_quarter, up_quarter)
        painter.drawLine(right_quarter, up_quarter, right_quarter, down_quarter)
        painter.fillRect(QRect(top_mid_x,up_quarter-(center_square_height/2), center_square_width, center_square_height), Qt.green)
        painter.fillRect(QRect(right_quarter-(center_square_width/2),right_mid_y, center_square_width, center_square_height), Qt.green)
        painter.setFont(QFont("times", 76))
        painter.drawText(QRect(top_mid_x,up_quarter, top_mid_x +70, up_quarter), QtCore.Qt.AlignCenter ,"test")
        # painter.setPen(Qt.blue)
        # painter.drawRect(120,10,80,80)

        # rectf = QRectF(230.0,10.0,80.0,80.0)
        # painter.drawRoundedRect(rectf,20,20)

        # p1 = [QPoint(10,100),QPoint(220,110),QPoint(220,190)]
        # painter.drawPolyline(QPolygon(p1))

        # p2 = [QPoint(120,110),QPoint(220,110),QPoint(220,190)]
        # painter.drawPolygon(QPolygon(p2))
    


class contextPerserver():
    width = 0
    height = 0


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())