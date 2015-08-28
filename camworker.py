#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import numpy as np
from time import clock

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from camera import Camera
from vision import *
from draw import *

class CamWorker(QThread): 

  def __init__(self): 

    super(CamWorker, self).__init__() 

    self.cam0 = Camera ( capture = cv2.VideoCapture(0) )

    self.currentFrame=np.array([])

    self.mutex = QMutex()
    self.values = {}

  def __del__(self):
    self.wait()

  def setvalue(self,name,value):
    with QMutexLocker(self.mutex):
      self.values[name] = value

  def processNextFrame(self,values):

    slide1 = values.get ('camera_slide1' , 0 )
    slide2 = values.get ('camera_slide2' , 0 )
    slide3 = values.get ('camera_slide3' , 0 )
    slide4 = values.get ('camera_slide4' , 0 )
    slide5 = values.get ('camera_slide5' , 0 )
    slide6 = values.get ('camera_slide6' , 0 )
    slide7 = values.get ('camera_slide7' , 0 )
    slide8 = values.get ('camera_slide8' , 0 )

    check1 = values.get ('camera_check1' , False )
    check2 = values.get ('camera_check2' , False )
    check3 = values.get ('camera_check3' , False )
    check4 = values.get ('camera_check4' , False )
    check5 = values.get ('camera_check5' , False )
    check6 = values.get ('camera_check6' , False )

    combo1 = values.get ('camera_combo1' , 0 )

    cam0_saturation = values.get ('cam0_saturation' , 0 )
    cam0_brightness = values.get ('cam0_brightness' , 0 )
    cam0_contrast = values.get ('cam0_contrast' , 0 )
    cam0_exposure = values.get ('cam0_exposure' , 0 )
    cam0_gain = values.get ('cam0_gain' , 0 )

    self.cam0.setBrightness ( cam0_brightness / 100.0 )
    self.cam0.setContrast ( cam0_contrast / 100.0 )
    self.cam0.setExposure ( cam0_exposure / 100.0 )
    self.cam0.setGain ( cam0_gain / 100.0 )

    display = combo1
    invert = check1

    threshold_mask = 255.0 *(slide1 / 100.0)
    blur_mask = [ 3 , 5 , 7 , 9 , 11 , 13 , 15 , 17 , 19 , 21 , 23 , 25 , 27 , 29 ] [ int( 13.0 *(slide2 / 100.0) ) ]

    threshold_border = 255.0 *(slide3 / 100.0)
    blur_border = [ 3 , 5 , 7 , 9 , 11 , 13 , 15 , 17 , 19 , 21 , 23 , 25 , 27 , 29 ] [ int( 13.0 *(slide4 / 100.0) ) ]

    features_blocksize = [ 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10 , 11 , 12 ] [ int( 10.0 *(slide5 / 100.0) ) ]
    features_ksize = [ 3 , 5 , 7 , 9 , 11 , 15 , 21 , 25 , 27 , 29 , 31 ] [ int( 10.0 *(slide6 / 100.0) ) ]
    features_quality = (slide7+1) / 1000.0

    flag, frame=self.cam0.capture.read()
    if not flag :
      return False

    # CONVERT TO GRAY

    gray = get_gray ( img = frame , invert = invert )

    # GET CENTER MASK

    gray_mask = smooth_mask ( gray = gray  , blur = blur_mask , threshold = threshold_mask )
    gray_mask = mask_center_label ( gray = gray_mask )

    # GET FEATURES

    gray_borders = smooth_borders ( gray = gray_mask , blur = blur_border )

    keypoints = find_keypoints ( gray = gray_borders , quality = features_quality , ksize = features_ksize , blocksize = features_blocksize )

    # DRAW OOB

    frame = draw_oob ( img = frame , points = keypoints )
    frame = draw_points ( img = frame , points = keypoints )

    if display == 0 :
      frame = draw_hud ( img = frame )
      self.currentFrame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
      return True

    if display == 1 :
      self.currentFrame=cv2.cvtColor(gray,cv2.COLOR_GRAY2RGB)
      return True

    if display == 2 :
      self.currentFrame=cv2.cvtColor(gray_mask,cv2.COLOR_GRAY2RGB)
      return True

    if display == 3 :
      self.currentFrame=cv2.cvtColor(gray_borders,cv2.COLOR_GRAY2RGB)
      return True

  def convertFrame(self):

    try:
      height,width=self.currentFrame.shape[:2]
      img=QImage(self.currentFrame,width,height,QImage.Format_RGB888)
      self.previousFrame = self.currentFrame
      return img
    except Exception as e :
      print e
      return None

  def run(self):
    while True :

      begin = clock ()

      # GET VALUES
      with QMutexLocker(self.mutex):
        values = self.values
      
      #self.captureNextFrame ()
      if self.processNextFrame( values = values ) is True :
        pix = self.convertFrame ()
        elapsed = clock () - begin
        self.emit( SIGNAL('webcam_frame(QImage)'), pix )
        self.emit( SIGNAL('webcam_frame_elapsed(float)'), elapsed )
