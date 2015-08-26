#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import cv2
import numpy as np
from scipy import ndimage as nd
from skimage import morphology
from skimage import exposure

from PyQt4.QtCore import *
from PyQt4.QtGui import *
 
from gui import Ui_MainWindow

class CamWorker(QThread): 

  def __init__(self): 

    super(CamWorker, self).__init__() 

    self.capture = cv2.VideoCapture(0)
    self.currentFrame=np.array([])
    self.mutex = QMutex()

    self.values = {}

  def __del__(self):
    self.wait()

  def setvalue(self,name,value):
    with QMutexLocker(self.mutex):
      self.values[name] = value

  def getvalue(self,name):
    with QMutexLocker(self.mutex):
      if not self.values.has_key (name) :
        return None
      return self.values [name]

  def captureNextFrame(self):

    flag , frame =self.capture.read()
    if(flag):
      self.currentFrame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

  def find_squares(self,img):

    def angle_cos(p0, p1, p2):
        d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
        return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

    squares = []

    for gray in cv2.split(img):
        for thrs in xrange(0, 255, 26):

            if thrs == 0:
                bin = cv2.Canny(gray, 0, 50, apertureSize=5)
                bin = cv2.dilate(bin, None)
            else:
                retval, bin = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)

            contours, hierarchy = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

            for cnt in contours:
                cnt_len = cv2.arcLength(cnt, True)
                cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
                if len(cnt) == 4 and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt):
                    cnt = cnt.reshape(-1, 2)
                    max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in xrange(4)])
                    if max_cos < 0.1:
                        squares.append(cnt)
    return squares

# http://docs.opencv.org/modules/refman.html
# http://scipy-lectures.github.io/packages/scikit-image/
# https://scipy-lectures.github.io/advanced/image_processing/
# https://github.com/Itseez/opencv/blob/master/samples/python2/squares.py
# http://stackoverflow.com/questions/7263621/how-to-find-corners-on-a-image-using-opencv
# http://docs.opencv.org/master/d4/d73/tutorial_py_contours_begin.html#gsc.tab=0
# http://docs.opencv.org/doc/tutorials/imgproc/shapedescriptors/find_contours/find_contours.html
# http://docs.opencv.org/modules/imgproc/doc/structural_analysis_and_shape_descriptors.html
# http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_imgproc/py_contours/py_contour_features/py_contour_features.html
# http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_core/py_basic_ops/py_basic_ops.html

  def processNextFrame(self,values):

      slide1 = values.get ('slide1' , 0 )
      slide2 = values.get ('slide2' , 0 )
      slide3 = values.get ('slide3' , 0 )
      check1 = values.get ('check1' , 0 )
      check2 = values.get ('check2' , 0 )

      flag, frame=self.capture.read()
      if not flag :
        return False

      rame = exposure.adjust_gamma(frame, gamma=1, gain=-0.5)

      p0, p1 = np.percentile(frame, (slide1, 100-slide1))
      frame = exposure.rescale_intensity(frame, in_range=(p0, p1))

      frame = nd.gaussian_filter(frame, sigma=slide2/(4.*10))

      gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

      if check2 :
        cv2.bitwise_not ( gray, gray )

      # gray = nd.gaussian_filter(gray, sigma=256/(4.*10))

      flag , gray = cv2.threshold ( gray , slide3 , 255 , cv2.THRESH_BINARY )
      if not flag :
        return False

      kernel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
      close = cv2.morphologyEx(gray,cv2.MORPH_CLOSE,kernel1)
      div = np.float32(gray)/(close)
      gray = np.uint8(cv2.normalize(div,div,0,255,cv2.NORM_MINMAX))

      # gray = morphology.remove_small_objects(gray, min_size=64, connectivity=1, in_place=False)

      # mask = gray > gray.mean()
      # label_im, nb_labels = ndimage.label(mask)
      # labels = np.unique(label_im)
      # label_im = np.searchsorted(labels, label_im)

      #element = cv2.getStructuringElement(cv2.MORPH_RECT, (5,3) )
      #cv2.erode(gray, gray, element);

      # corners = cv2.goodFeaturesToTrack(gray,25,0.01,10)

      # if corners is not None:
      #   corners = np.int0(corners)
      #   for i in corners:
      #       x,y = i.ravel()
      #       cv2.circle(frame,(x,y),3,255,-1)

      # gray = cv2.GaussianBlur(gray, (5, 5), 0)

      squares = self.find_squares (gray)
      cv2.drawContours( frame, squares, -1, (0, 255, 0), 3 )

      if check1 :
        self.currentFrame=cv2.cvtColor(gray,cv2.COLOR_GRAY2RGB)
      else :
        self.currentFrame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

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

      # GET VALUES
      with QMutexLocker(self.mutex):
        values = self.values
      
      #self.captureNextFrame ()
      if self.processNextFrame( values = values ) is True :
        pix = self.convertFrame ()
        self.emit( SIGNAL('webcam_frame(QImage)'), pix )
