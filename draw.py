#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np

def draw_hud ( img , color = (0,0,255) ) :

  assert img is not None

  h,w,channels = img.shape

  cv2.line (img , ( int(w/2),0 ) , (int(w/2),h)  , color , 1 )
  cv2.line (img , ( 0,int(h/2) ) , (w,int(h/2))  , color , 1 )

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

def draw_square ( img , square , color = (0,255,0) ) :

  assert img is not None

  if square is None :
    return img

  p0,p1,p2,p3 = square

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
