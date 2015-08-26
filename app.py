#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
 
from PyQt4.QtCore import *
from PyQt4.QtGui import *
 
from gui import Ui_MainWindow
from camera import CamWorker

class MainWindow(QMainWindow):

  def __init__(self):
    QMainWindow.__init__(self)    

    self.ui = Ui_MainWindow ()
    self.ui.setupUi(self)

    self.scenecam = QGraphicsScene (self)
    self.ui.camera.setScene (self.scenecam)

    self.camworker = CamWorker()
    self.camworker.start()

    QObject.connect(self.camworker, SIGNAL("webcam_frame(QImage)"), self.updatecamera)

    self.ui.camera_slide1.valueChanged.connect( lambda v: self.camworker.setvalue("slide1",v) )
    self.ui.camera_slide2.valueChanged.connect( lambda v: self.camworker.setvalue("slide2",v) )
    self.ui.camera_slide3.valueChanged.connect( lambda v: self.camworker.setvalue("slide3",v) )
    self.ui.camera_check1.stateChanged.connect( lambda v: self.camworker.setvalue("check1",v) )
    self.ui.camera_check2.stateChanged.connect( lambda v: self.camworker.setvalue("check2",v) )

    self.update()

  def updatecamera(self,img):
    try:
      pix=QPixmap.fromImage(img)
      self.scenecam.clear()
      self.scenecam.addPixmap(pix)
    except TypeError:
      self.statusbar.showMessage('Error From CAM0')

# Main entry to program.  Sets up the main app and create a new window.
def main(argv):

  # create Qt application
  app = QApplication(argv,True)

  # create main window
  wnd = MainWindow() # classname
  wnd.show()

  # Connect signal for app finish
  app.connect(app, SIGNAL("lastWindowClosed()"), app, SLOT("quit()"))

  # Start the app up
  sys.exit(app.exec_())
 
if __name__ == "__main__":
  main(sys.argv)
