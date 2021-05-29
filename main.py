from typing import Text
from PyQt5.Qt import *
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtGui import *
from img_segm_ui import Ui_MainWindow
import pyqtgraph as pg
import os, sys
import cv2 as cv
from FCM import FCM
class ApplicationWindow(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setGeometry(600, 300, 400, 200)
        self.setWindowTitle('image segmentation')
        pg.setConfigOption('background', 'w')
        # hiding axis
        self.ui.fcm.getPlotItem().hideAxis('bottom')
        self.ui.fcm.getPlotItem().hideAxis('left')

        self.ui.original_img.getPlotItem().hideAxis('bottom')
        self.ui.original_img.getPlotItem().hideAxis('left')
        # rest of functions
        self.ui.upload.clicked.connect(self.UploadImage)
        self.ui.fcm_button.clicked.connect(self.fcm_function)


    def UploadImage(self):
        self.senderOBJ = self.sender()
        print(self.senderOBJ.text())
        filePaths = QtWidgets.QFileDialog.getOpenFileNames(self, 'Open File',"~/Desktop/FCM/dataset",'*.bmp')   
        for filePath in filePaths:
            for self.f in filePath:
                if self.f == '*':
                        break
                # sending the image to the FCM class in grey scale
                self.send=cv.imread(self.f,cv.IMREAD_GRAYSCALE)
                # reading the image in colors for viewing it 
                self.theimage=cv.imread(self.f)
                self.image = pg.ImageItem(self.theimage)      
                self.ui.original_img.addItem(self.image)
                self.image.rotate(270) 
 
   
    def fcm_function(self):
        # getting the values from the user
        self.C=self.ui.spinBox.value()
        print(self.C)
        cluster = FCM(self.send,self.C)
        cluster.formatClusters()
        result=cluster.result
        result_img = pg.ImageItem(result)   
        # adding the resulted image
        self.ui.fcm.addItem(result_img)
        result_img.rotate(270)



def main():

    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    app.exec_()
    
    

if __name__ == '__main__':
    main()
