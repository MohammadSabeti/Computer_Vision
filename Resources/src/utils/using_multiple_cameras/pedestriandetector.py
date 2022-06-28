import cv2 as cv

class PedestrianDetector:
    
    def __init__(self,cascadePath):
        # load the pedestrian detector
        self.pedestrianCascade=cv.CascadeClassifier(cascadePath)
        
    def detect(self,image,scaleFactor=1.1,minNeighbors=5,minSize=(30,30)):
        # detect pedestrian in the image
        rects=self.pedestrianCascade.detectMultiScale(image,scaleFactor=scaleFactor,
                                                      minNeighbors=minNeighbors,
                                                      minSize=minSize,
                                                      flags=cv.CASCADE_SCALE_IMAGE)
        
        # return the rectangles representing bounding boxes around the pedestrian
        return rects 

















