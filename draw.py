#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np

def draw_hud ( img , color = (0,0,255) ) :

  assert img is not None

  h,w,channels = img.shape

  cv2.line (img , ( w/2,0 ) , (w/2,h)  , color , 1 )
  cv2.line (img , ( 0 , h/2 ) , (w,h/2)  , color , 1 )

  return img

def draw_points ( img , points , color = (255,0,0) ) :
  assert img is not None
  if points is None :
    return img

  if points is not None :

    for p in points:
        x,y = p.ravel()
        cv2.circle(img,(x,y),3,color,-1)

  return img

  #return cv2.drawKeypoints(img, keypoints, np.array([]), (255,0,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

def draw_oob ( img , points , color = (0,255,0) ) :

  assert img is not None

  if points is None :
    return img

  obb = cv2.minAreaRect(points) 

  center , size , angle = obb

  w = size[0]/2
  h = size[1]/2
  ox,oy = center

  rangle = np.radians(angle)
  sinn = np.sin (rangle)
  coss = np.cos (rangle)

  def f(x,y) :
    return ( 
      int ((x * w * coss) - ( y * h * sinn ) + ox ),
      int ((x * w * sinn ) + (y * h * coss ) + oy )
      )

  p0 = f( 1, 1)
  p1 = f( 1,-1)
  p2 = f(-1,-1)
  p3 = f(-1, 1)

  cv2.line (img, p0, p1 , color , 1 )
  cv2.line (img, p1, p2 , color , 1 )
  cv2.line (img, p2, p3 , color , 1 )
  cv2.line (img, p3, p0 , color , 1 )

  return img

def draw_labels ( self , label_im , img ) :

  labels = np.unique(label_im)
  for l in labels :
    c = ( random.randint (0,255) , random.randint (0,255) , random.randint (0,255) )
    img [ label_im == l ] = c

  return img
