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

cap = cv2.VideoCapture(0)
width= int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height= int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
writer= cv2.VideoWriter(os.path.join("test_videos", 'test_videos.mp4'), cv2.VideoWriter_fourcc(*'DIVX'), 20, (width,height))


while True:
    ret, frame = cap.read()
    if ret:
        writer.write(frame)
    # cv2.imshow('frame', frame)

                