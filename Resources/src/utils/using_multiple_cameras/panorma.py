from imutils import is_cv3
import time 
import cv2 as cv
import numpy as np 

# NOTE : In Perspective Transformation, we can change the perspective of a given image or video for
# getting better insights into the required information. In Perspective Transformation,
# we need to provide the points on the image from which want to gather information by changing the perspective.
# We also need to provide the points inside which we want to display our image.
# Then, we get the perspective transform from the two given sets of points and wrap it with the original image



class Stitcher:
    def __init__(self):
        # determine if we are using OpenCV v3.x and initialize the cached homography matrix 
        self.isv3=is_cv3(or_better=True)
        self.cachedH=None
    
    
    def stitch(self,images,ratio=0.75,reprojThresh=4.0):
        
        # unpack the images
        (imageA,imageB)=images
        
        # if cached homography matrix is None, then we need to apply keypoint matching to construct it
        if self.cachedH is None:
            (kpsA,featuresA)=self.detectAndDescribe(imageA)
            (kpsB,featuresB)=self.detectAndDescribe(imageB)

            # match features between the two images
            M=self.matchKeypoints(kpsA,kpsB,
                                  featuresA,featuresB,
                                  ratio,reprojThresh)
            
            # if the match is None, then there aren't enough matched keypoints to create a panorama
            if M is None:
                return None
            
            # cache the homography matrix 
            self.cachedH=M[1]
            
        # apply  a perspective transform to switch the images together 
        # using the cache the homography matrix
        result=cv.warpPerspective(imageA,self.cachedH,(imageA.shape[1]+imageB.shape[1],imageA.shape[0]))
        result[0:imageB.shape[0],0:imageB.shape[1]]=imageB
        
        # return the stitched image
        return result 
            
        
    def detectAndDescribe(self,image):
        # convert the image to grayscale
        gray=cv.cvtColor(image,cv.COLOR_BGR2GRAY)
        
        # check to see if we are using OpenCV 3.x
        if self.isv3: 
            # detect and extract features from the image
            descriptor=cv.xfeatures2d.SIFT_create()
            (kps,features)= descriptor.detectAndCompute(image,None)
        
        # otherwise, we are using OpenCV 2.4.x
        else:
            # detect features from the image
            detector=cv.FastFeatureDetector_create('SIFT')
            kps= detector.detect(gray)
            
            # extract features from the image
            extractor=cv.DescriptorExtractor_create('SIFT')
            (kps,features)= extractor.compute(gray,kps)
            
        # convert the keypoints from KeyPoint objects to Numpy array
        kps=np.float32([kp.pt for kp in kps])
        
        # return a tuple of keypoints and features
        return(kps,features)
        
            
    def matchKeypoints(self,kpsA,kpsB,featuresA,featuresB,ratio,reprojThresh):
        # compute the raw matches and initialize the list of actual matches
        matcher=cv.DescriptorMatcher_create('BruteForce')
        rawMatches=matcher.knnMatch(featuresA,featuresB,2)
        matches=[]
        
        # loop over the raw matches
        for m in rawMatches:
            # ensure the distance is within a certain ratio of each other (i.e. low's ratio test)
            if len(m)==2 and m[0].distance < m[1].distance * ratio:
                matches.append((m[0].trainIdx,m[0].queryIdx))
        
        # computing a homography requires at latest 4 matches
        if len(matches)> 4:
            # construct the two sets of points 
            ptsA=np.float32(np.array([kpsA[i] for (_,i) in matches])) 
            ptsB=np.float32(np.array([kpsB[i] for (i,_) in matches])) 
            # ptsB=np.float32([kpsB[i] for (i,_) in matches]) 

            # compute the homography between the two sets of points 
            (H,status)=cv.findHomography(ptsA,ptsB,cv.RANSAC,reprojThresh)
            
            # return the matches along with the homography matrix and status of each matched point
            return (matches,H,status)
        
        # otherwise, no homography could be computed
        return None
    
        
        
        