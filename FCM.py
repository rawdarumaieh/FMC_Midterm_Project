import numpy as np
from scipy import signal
import cv2 as cv

class FCM():
    def __init__(self,image,n_clusters=2,fuzziness=2,epsilon=0.05,max_iter=300):

        self.image = image
        self.n_clusters = n_clusters
        self.fuzziness = fuzziness
        self.epsilon = epsilon
        self.max_iter = max_iter

        self.shape = image.shape # image shape
        self.X = image.flatten().astype('float') # flatted image shape: (number of pixels,1) 
        self.numPixels = image.size

        #-----------------Initial weights-----------------#
        self.weight = np.zeros((self.numPixels, self.n_clusters))
        arranged_pixels = np.arange(self.numPixels)
        for i in range(self.n_clusters):
            true = arranged_pixels%self.n_clusters==i
            # result is like [[1,0,0]
                           #  [0,1,0]
                              #[0,0,1] ]
            self.weight[true,i] = 1

        #-----------------Initial centers-----------------#
        # evenly put weights over a max and min value in pixels weights are equal to number of clusters
        self.centres = np.linspace(np.min(image),np.max(image),n_clusters)
        self.centres = self.centres.reshape(self.n_clusters,1)
      

                    
        #-----------------updating weights-----------------#

    def updateWeights(self):
        centres,points = np.meshgrid(self.centres,self.X)
        #power equals 2 divided by fuzziness-1
        power = 2./(self.fuzziness-1)
        #neumerator equals the difference between the centre and each point 
        p1 = abs(centres-points)**power
        #summation of 1/p1
        p2 = np.sum((1./abs(centres-points))**power,axis=1)

        return 1./(p1*p2[:,None])

        #-----------------updating centres-----------------#

    def updateCentres(self):
        # computinig the centroid of the cluster 
        # dot product between the pixel values and weight power the fuzziness 
        numerator = np.dot(self.X,self.weight**self.fuzziness)
        # summation of weights power thr funzziness 
        denomerator = np.sum(self.weight**self.fuzziness,axis=0)

        return numerator/denomerator


  
        #-----------------iterativly formating the cluster----------------#

    def formatClusters(self):     
        #errors 
        error = 100
        # didn't reach the maximum iterations 
        if self.max_iter != -1:
            i = 0
            while True:      
                # update the centre
                self.centres = self.updateCentres()
                # copy prev weights to compute the error
                prev_weights = np.copy(self.weight)
                # update the weight
                self.weight = self.updateWeights()
                # calculating the new error
                error = np.sum(abs(self.weight - prev_weights))

                if error < self.epsilon or i > self.max_iter:
                    break
                i+=1
        else:
            i = 0
            while error > self.epsilon:
                self.centres = self.updateCentres()
                prev_weights = np.copy(self.weight)
                self.weight = self.updateWeights()
                error = np.sum(abs(self.weight- prev_weights))
                if error < self.epsilon or i > self.max_iter:
                    break
                i+=1
        self.imageSegmentation()


        #-----------------Segmenting the image-----------------#


    def imageSegmentation(self):
        # segmenting the image based on the maximum weights computed
        result = np.argmax(self.weight, axis = 1)
        self.result = result.reshape(self.shape).astype('int')

        return self.result

