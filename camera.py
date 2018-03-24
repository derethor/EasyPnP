#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
import logging

class Camera :

  def __init__(self,capture):

    assert capture is not None
    assert capture.isOpened() is True    

    self.capture = capture
    self.capture.set(cv2.CAP_PROP_FRAME_WIDTH,320)
    self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT,200)

    self.test = self.capture.get(cv2.CAP_PROP_POS_MSEC)
    self.ratio = self.capture.get(cv2.CAP_PROP_POS_AVI_RATIO)
    self.frame_rate = self.capture.get(cv2.CAP_PROP_FPS)
    self.width = self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    self.height = self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    self.brightness = self.capture.get(cv2.CAP_PROP_BRIGHTNESS)
    self.contrast = self.capture.get(cv2.CAP_PROP_CONTRAST)
    self.saturation = self.capture.get(cv2.CAP_PROP_SATURATION)
    self.hue = self.capture.get(cv2.CAP_PROP_HUE)
    self.gain = self.capture.get(cv2.CAP_PROP_GAIN)
    self.exposure = self.capture.get(cv2.CAP_PROP_EXPOSURE) 

    logging.debug ("GET CAP_PROP_FRAME_WIDTH: %s" % self.width )
    logging.debug ("GET CAP_PROP_FRAME_HEIGHT: %s" % self.height )
    logging.debug ("GET CAP_PROP_EXPOSURE: %s" % self.exposure )


    self.brightness_disabled = not self.capture.set ( cv2.CAP_PROP_BRIGHTNESS , self.brightness )
    if not self.brightness_disabled:
      self.brightness = self.capture.get ( cv2.CAP_PROP_BRIGHTNESS )
      logging.debug ( "GET CAP_PROP_BRIGHTNESS %s" % self.brightness )

    self.contrast_disabled = not self.capture.set ( cv2.CAP_PROP_CONTRAST , self.contrast )
    if not self.contrast_disabled :
      self.contrast = self.capture.get ( cv2.CAP_PROP_CONTRAST )
      logging.debug ( "GET CAP_PROP_CONTRAST %s" % self.contrast )

    self.exposure_disabled = not self.capture.set ( cv2.CAP_PROP_EXPOSURE , self.exposure )
    if not self.exposure_disabled :
      self.exposure = self.capture.get ( cv2.CAP_PROP_EXPOSURE )
      logging.debug ( "GET CAP_PROP_EXPOSURE %s" % self.exposure )

    self.gain_disabled = not self.capture.set ( cv2.CAP_PROP_GAIN , self.gain )
    if not self.gain_disabled :
      self.gain = self.capture.get ( cv2.CAP_PROP_GAIN )
      logging.debug ( "GET CAP_PROP_GAIN %s" % self.gain )

    self.saturation_disabled = not self.capture.set ( cv2.CAP_PROP_SATURATION , self.saturation )
    if not self.saturation_disabled :
      self.saturation = self.capture.get ( cv2.CAP_PROP_SATURATION )
      logging.debug ( "GET CAP_PROP_SATURATION %s" % self.saturation )

    # CV_CAP_PROP_HUE

  def setBrightness (self,brightness) :
    if self.brightness_disabled :
      return

    if brightness == self.brightness :
      return

    logging.debug ( "SET CAP_PROP_BRIGHTNESS %s" % brightness )
    self.capture.set ( cv2.CAP_PROP_BRIGHTNESS , brightness )
    self.brightness = brightness

  def setContrast (self,contrast) :
    if self.contrast_disabled :
      return

    if contrast == self.contrast :
      return

    logging.debug ( "SET CAP_PROP_CONTRAST %s" % contrast )
    self.capture.set ( cv2.CAP_PROP_CONTRAST , contrast )
    self.contrast = contrast

  def setExposure (self,exposure) :
    if self.exposure_disabled :
      return

    if exposure == self.exposure :
      return

    logging.debug ( "SET CAP_PROP_EXPOSURE %s" % exposure )
    self.capture.set ( cv2.CAP_PROP_EXPOSURE , exposure )
    self.exposure = exposure

  def setGain (self,gain) :
    if self.gain_disabled :
      return

    if gain == self.gain :
      return

    logging.debug ( "SET CAP_PROP_GAIN %s" % gain )
    self.capture.set ( cv2.CAP_PROP_GAIN , gain )
    self.gain = gain
