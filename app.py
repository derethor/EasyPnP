#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys , json
import logging
import inspect

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
 
from gui import Ui_MainWindow
from camworker import CamWorker

class CoreMotion :
  def __init__(self):
    self.current = {}

class MainWindow(QMainWindow):

  def __init__(self):
    QMainWindow.__init__(self)       

    self.logger = self.setup_logger( level = logging.DEBUG)

    self.coremotion = CoreMotion ()

    self.settings = QSettings ('staticboards' , 'pickplacev1.0.0')

    self.ui = Ui_MainWindow ()
    self.ui.setupUi(self)

    self.scenecam = QGraphicsScene (self)
    self.ui.camera.setScene (self.scenecam)

    self.camworker = CamWorker()
    self.camworker.start()

    self.camworker.webcam_frame.connect( self.update_camera )
    self.camworker.webcam_frame_elapsed.connect( self.update_elapsed )

    # CONNECT CALLBACKS
    self.ui.camera_slide1.valueChanged.connect( lambda v: self.set_config_value(section = "camworker" , name="camera_slide2", value = v) )
    self.ui.camera_slide2.valueChanged.connect( lambda v: self.set_config_value(section = "camworker" , name="camera_slide2", value = v) )
    self.ui.camera_slide3.valueChanged.connect( lambda v: self.set_config_value(section = "camworker" , name="camera_slide3", value = v) )
    self.ui.camera_slide4.valueChanged.connect( lambda v: self.set_config_value(section = "camworker" , name="camera_slide4", value = v) )
    self.ui.camera_slide5.valueChanged.connect( lambda v: self.set_config_value(section = "camworker" , name="camera_slide5", value = v) )
    self.ui.camera_slide6.valueChanged.connect( lambda v: self.set_config_value(section = "camworker" , name="camera_slide6", value = v) )
    self.ui.camera_slide7.valueChanged.connect( lambda v: self.set_config_value(section = "camworker" , name="camera_slide7", value = v) )
    self.ui.camera_slide8.valueChanged.connect( lambda v: self.set_config_value(section = "camworker" , name="camera_slide8", value = v) )

    self.ui.camera_check1.stateChanged.connect( lambda v: self.set_config_value(section = "camworker" , name="camera_check1", value = v) )
    self.ui.camera_check2.stateChanged.connect( lambda v: self.set_config_value(section = "camworker" , name="camera_check2", value = v) )
    self.ui.camera_check3.stateChanged.connect( lambda v: self.set_config_value(section = "camworker" , name="camera_check3", value = v) )
    self.ui.camera_check4.stateChanged.connect( lambda v: self.set_config_value(section = "camworker" , name="camera_check4", value = v) )
    self.ui.camera_check5.stateChanged.connect( lambda v: self.set_config_value(section = "camworker" , name="camera_check5", value = v) )
    self.ui.camera_check6.stateChanged.connect( lambda v: self.set_config_value(section = "camworker" , name="camera_check6", value = v) )

    self.ui.camera_combo1.currentIndexChanged.connect( lambda v: self.set_config_value(section = "camworker" , name="camera_combo1", value = v) )

    self.ui.cam0_brightness.valueChanged.connect( lambda v: self.set_config_value(section = "camworker" , name="cam0_brightness", value = v) )
    self.ui.cam0_contrast.valueChanged.connect( lambda v: self.set_config_value(section = "camworker" , name="cam0_contrast", value = v) )
    self.ui.cam0_exposure.valueChanged.connect( lambda v: self.set_config_value(section = "camworker" , name="cam0_exposure", value = v) )
    self.ui.cam0_gain.valueChanged.connect( lambda v: self.set_config_value(section = "camworker" , name="cam0_gain", value = v) )

    # LOAD VALUES AGAIN TO EMIT CALLBACKS
    self.guirestore()

  def setup_logger (self , level = logging.DEBUG ) :

    root = logging.getLogger()
    root.setLevel(level)

    ch = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    ch.setLevel ( logging.DEBUG )
    root.addHandler(ch)

    return root

  ###############################################################
  ###############################################################

  @pyqtSlot('QImage')
  def update_camera(self,img):

    try:

      pix=QPixmap.fromImage(img)
      self.scenecam.clear()
      self.scenecam.addPixmap(pix)

      self.ui.camera.fitInView ( self.scenecam.sceneRect () , Qt.KeepAspectRatio )

    except Exception as e :
      logging.error ( str(e) )
      self.ui.statusbar.showMessage( str(e) )

  @pyqtSlot(float)
  def update_elapsed(self,elapsed):
    ms = elapsed * 1000.0
    self.ui.statusbar.showMessage( "Frame time: %s" % ms )

  ##

  def update_coremotion(self,section,name,value) :
    assert section is not None
    assert name is not None

    if section == 'current' :
      self.coremotion.current [name] = value

      if name == 'component_hangle' :
        self.ui.label_current_hangle.setText ( 'HANGLE %03d' % value )
      if name == 'component_vangle' :
        self.ui.label_current_vangle.setText ( 'VANGLE %03d' % value )


  ###############################################################
  ###############################################################

  def guisave(self,name):

    for n, obj in inspect.getmembers(self.ui):

      if n != name :
        continue

      value = None

      if isinstance(obj, QComboBox):
        value = obj.currentIndex ()
      if isinstance(obj, QSlider):
        value = obj.value ()
      if isinstance(obj, QCheckBox):
        value = obj.isChecked()

      if value is not None :
        self.settings.setValue(name, value)

      return

  def guirestore(self):

    for name, obj in inspect.getmembers(self.ui):

      value = self.settings.value(name)   # get stored value from registry

      if value is None :
        continue

      if isinstance(obj, QComboBox):
        value = int(value)
        if value is not None:
          obj.setCurrentIndex(value)

      if isinstance(obj, QSlider):
        value = int(value)
        if value is not None:
          obj.setValue(value)

      if isinstance(obj, QCheckBox):        
        value = bool(value)
        if value is not None:
          obj.setChecked( value )

  def set_config_value ( self , section , name , value ) :
    """
    Save value and update json
    """

    assert section is not None
    assert name is not None

    logging.debug ( "set_config_value %s %s %s" % (section,name,value) )

    self.guisave ( name = name )

    if section == 'camworker' :
      self.camworker.setvalue(name,value)

# Main entry to program.  Sets up the main app and create a new window.
def main():

  # create Qt application
  app = QApplication(sys.argv)

  # create main window
  wnd = MainWindow() # classname
  wnd.show()

  # Connect signal for app finish
  app.lastWindowClosed.connect ( app.quit )

  # Start the app up
  sys.exit(app.exec_())
 
if __name__ == "__main__":
  main()

