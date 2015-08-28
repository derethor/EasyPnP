#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import logging

class Camera :

  def __init__(self,capture):

    assert capture is not None

    self.capture = capture

    self.brightness = self.capture.get ( cv2.cv.CV_CAP_PROP_BRIGHTNESS )
    self.brightness_disabled = self.capture.set ( cv2.cv.CV_CAP_PROP_BRIGHTNESS , self.brightness )

    self.contrast = self.capture.get ( cv2.cv.CV_CAP_PROP_CONTRAST )
    self.contrast_disabled = self.capture.set ( cv2.cv.CV_CAP_PROP_CONTRAST , self.contrast )

    self.exposure = self.capture.get ( cv2.cv.CV_CAP_PROP_EXPOSURE )
    self.exposure_disabled = self.capture.set ( cv2.cv.CV_CAP_PROP_EXPOSURE , self.exposure )

    self.gain = self.capture.get ( cv2.cv.CV_CAP_PROP_GAIN )
    self.gain_disabled = self.capture.set ( cv2.cv.CV_CAP_PROP_GAIN , self.gain )

    # self.saturation = self.capture.get ( cv2.cv.CV_CAP_PROP_SATURATION )
    # self.saturation_disabled = self.capture.set ( cv2.cv.CV_CAP_PROP_SATURATION , self.saturation )
    # CV_CAP_PROP_HUE

  def setBrightness (self,brightness) :
    if self.brightness_disabled :
      return

    if brightness == self.brightness :
      return

    logging.debug ( "SET CV_CAP_PROP_BRIGHTNESS %s" % brightness )
    self.capture.set ( cv2.cv.CV_CAP_PROP_BRIGHTNESS , brightness )
    self.brightness = brightness

  def setContrast (self,contrast) :
    if self.contrast_disabled :
      return

    if contrast == self.contrast :
      return

    logging.debug ( "SET CV_CAP_PROP_CONTRAST %s" % contrast )
    self.capture.set ( cv2.cv.CV_CAP_PROP_CONTRAST , contrast )
    self.contrast = contrast

  def setExposure (self,exposure) :
    if self.exposure_disabled :
      return

    if exposure == self.exposure :
      return

    logging.debug ( "SET CV_CAP_PROP_EXPOSURE %s" % exposure )
    self.capture.set ( cv2.cv.CV_CAP_PROP_EXPOSURE , exposure )
    self.exposure = exposure

  def setGain (self,gain) :
    if self.gain_disabled :
      return

    if gain == self.gain :
      return

    logging.debug ( "SET CV_CAP_PROP_GAIN %s" % gain )
    self.capture.set ( cv2.cv.CV_CAP_PROP_GAIN , gain )
    self.gain = gain
