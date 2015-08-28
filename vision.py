#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import random

from scipy import ndimage as nd
from scipy.ndimage import label

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

def get_gray (img , invert = False ) :

  gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
  if invert :
    cv2.bitwise_not ( gray, gray )

  gray = cv2.equalizeHist (gray)

  return gray

def smooth_mask ( gray  , blur = 1 , threshold = 128 ) :

  assert gray is not None

  gray_markers = nd.median_filter(gray, blur)
  _ , gray_markers = cv2.threshold ( gray_markers , threshold , 255 , cv2.THRESH_BINARY )

  return gray_markers

def smooth_borders (gray , blur = 1 ) :

  assert gray is not None

  gray_borders = cv2.GaussianBlur(gray, (blur, blur), 0)
  gray_borders = cv2.adaptiveThreshold(gray_borders, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 1)

  # Some morphology to clean up image
  kernel = np.ones((5,5), np.uint8)
  gray_borders = cv2.morphologyEx(gray_borders, cv2.MORPH_OPEN, kernel)
  gray_borders = cv2.morphologyEx(gray_borders, cv2.MORPH_CLOSE, kernel)

  return gray_borders

def find_squares(img,minArea=1000):

  """
  Find squared contours with min area
  """

  def angle_cos(p0, p1, p2):
      d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
      return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

  squares = []

  contours, hierarchy = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

  print len(contours)

  for cnt in contours:
    cnt_len = cv2.arcLength(cnt, True)
    cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
    if len(cnt) == 4 and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt):
        cnt = cnt.reshape(-1, 2)
        max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in xrange(4)])
        if max_cos < 0.1:
            squares.append(cnt)
  return squares

def mask_center_label ( gray ) :
  """
  Create a mask with the label on the center
  http://stackoverflow.com/questions/11294859/how-to-define-the-markers-for-watershed-in-opencv
  """

  assert gray is not None

  # s = ndimage.generate_binary_structure(2,2) # iterate structure
  label_im, nb_labels = label(gray)

  # get center label

  h = label_im.shape[0]
  w = label_im.shape[1]

  l = label_im [h/2,w/2]

  gray [ label_im == l ] = 255
  gray [ label_im != l ] = 0

  return gray

def find_keypoints ( gray , quality , ksize , blocksize ) :
  gray32 = np.float32(gray)
  return cv2.goodFeaturesToTrack(gray32,maxCorners = 100, qualityLevel = quality ,minDistance = ksize , blockSize = blocksize )

def find_blobs (img) :

  """
  http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_imgproc/py_thresholding/py_thresholding.html
  """

  assert img is not None

  # Setup SimpleBlobDetector parameters.
  params = cv2.SimpleBlobDetector_Params()

  # Change thresholds
  params.minThreshold = 10
  params.maxThreshold = 200

  # Filter by Area.
  params.filterByArea = True
  params.minArea = 1000

  # Filter by Circularity
  params.filterByCircularity = False
  params.minCircularity = 0.1

  # Filter by Convexity
  params.filterByConvexity = False
  params.minConvexity = 0.87

  # Filter by Inertia
  params.filterByInertia = False
  params.minInertiaRatio = 0.01

  # Create a detector with the parameters
  detector = cv2.SimpleBlobDetector(params)

  # Detect blobs.
  keypoints = detector.detect(img)

  return keypoints

def test_harris (gray) :
  """
  Find corners using harris
  """
  gray32 = np.float32(gray)
  dst = cv2.cornerHarris(gray32,blocksize,ksize,k)
  dst = cv2.dilate(dst,None)
  return dst

def test_features () :

  # WHAT?
  element = cv2.getStructuringElement(cv2.MORPH_RECT, (5,3) )
  cv2.dilate(gray, gray, element);

  # FIND SQUARES
  squares = self.find_squares (gray)
  cv2.drawContours( frame, squares, -1, (0, 255, 0), 3 )
