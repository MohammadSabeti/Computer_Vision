# NOTE : more about moving average
# https://www.geeksforgeeks.org/background-subtraction-in-an-image-using-concept-of-running-average/

import cv2 as cv
import numpy as np
import imutils


class SingleMotionDetector:
    def __init__(self,accum_weight=0.5):
        # Alpha decides the speed of updating.
        # If you set a lower value for this variable,
        # running average will be performed over a larger amount
        # of previous frames and vice-versa.
        # store the accumulated weight factor
        self.accum_weight=accum_weight
        
        # initialize the background model
        self.bg=None
    
    def update(self,img):
        # if the background model is None, initialize it
        if self.bg is None:
            self.bg=img.copy().astype("float")
            return
        
        # update the background model by accumulating the weight average
        cv.accumulateWeighted(img,self.bg,self.accum_weight)
    
    def detect(self,img,t_val=25):
        # compute the absolute difference between the background model
        # and the image passed in, then threshold the delta image
        delta=cv.absdiff(self.bg.astype("uint8"),img)
        # any pixel locations that have a difference > t_val are set to 255 (white) otherwise they are set to 0 (black)
        thresh=cv.threshold(delta,t_val,255,cv.THRESH_BINARY)[1]
        
        # perform a series of erosions and dilations to remove small blobs
        thresh=cv.erode(thresh,None,iterations=2)
        thresh=cv.dilate(thresh,None,iterations=2)
        
        # find contours in the thresholded img and initialize the min and max bounding box regions for motion
        cnts=cv.findContours(thresh.copy(),cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
        cnts=imutils.grab_contours(cnts)
        (min_x,min_y)=(np.inf,np.inf) 
        (max_x,max_y)=(-np.inf,-np.inf) 
        
        # if no contours were found, return None
        if len(cnts)==0:
            return None
        
        # otherwise loop over the contours
        for c in cnts:
            # compute the bounding box of the contour and use it to 
            # update the min and max bounding box regions
            (x,y,w,h)=cv.boundingRect(c)
            (min_x,min_y)=(min(min_x,x),min(min_y,y))
            (max_x,max_y)=(max(max_x,x+w),max(max_y,y+h)) 
        
        # otherwise, return a tuple of the thresholded img along with bounding box
        return (thresh,(min_x,min_y,max_x,max_y)) 