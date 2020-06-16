from .graph import Graph
from .gmm import GMM
from .ford_fulkerson import mincut
from math import sqrt, exp, log
import numpy as np
import sys


class GraphCut(Graph):
    def __init__(self, image, mask, gamma=50, lamb=9):
        super(GraphCut, self).__init__()
        self.gamma = gamma
        self.diagonalGamma = self.gamma / sqrt(2) # gamma over the distance of the diagonal
        self.lamb = 9
        self.setImage(image)
        self.setMask(mask)
        self.applyMincut()

    def setImage(self, image):
        self.image = image
        self.nodes = []
        self.edges = []
        for i in range(self.image.shape[0]*self.image.shape[1]):
            self.addNode()
        self.__calcBeta()
        self.calcNWeights()
        self.calcK()

    def setMask(self, mask):
        self.mask = mask

        backgroundMask = self.mask == 1
        foregroundMask = self.mask == 2

        backgroundX = self.image[backgroundMask]
        foregroundX = self.image[foregroundMask]

        self.gmms = {
            'background': GMM(5, 30).fit(backgroundX),
            'foreground': GMM(5, 30).fit(foregroundX)
        }

        self.calcTWeights()
    
    def calcNWeights(self):
        for y in range(self.image.shape[0]):
            for x in range(self.image.shape[1]):
                nodeIndex = self.image.shape[1]*y + x
                # Only need to treat upper pixels and left pixel since we go to the others after
                if x > 0: # left
                    diff = self.image[y, x] - self.image[y, x-1]
                    weight = self.gamma * exp(-self.beta * diff.dot(diff))
                    self.addEdge(nodeIndex, nodeIndex-1, weight, weight)
                if y > 0 and x > 0: # upleft
                    diff = self.image[y, x] - self.image[y-1, x-1]
                    weight = self.gamma * exp(-self.diagonalGamma * diff.dot(diff))
                    self.addEdge(nodeIndex, nodeIndex-self.image.shape[1]-1, weight, weight)
                if y > 0: # up
                    diff = self.image[y, x] - self.image[y-1, x]
                    weight = self.gamma * exp(-self.beta * diff.dot(diff))
                    self.addEdge(nodeIndex, nodeIndex-self.image.shape[1], weight, weight)
                if y > 0 and x < self.image.shape[1]-1: # upright
                    diff = self.image[y, x] - self.image[y-1, x+1]
                    weight = self.gamma * exp(-self.diagonalGamma * diff.dot(diff))
                    self.addEdge(nodeIndex, nodeIndex-self.image.shape[1]+1, weight, weight)

    def calcK(self):
        weights = np.zeros(len(self.nodes))

        for edge in self.edges:
            weights[edge.origin] += edge.weight

        self.K = 1 + np.max(weights)
    
    def calcTWeights(self):
        self.foregroundNodeIndex, self.backgroundNodeIndex = self.addTerminalNodes()

        for y in range(self.image.shape[0]):
            for x in range(self.image.shape[1]):
                if(self.mask[y, x] == 1): # background
                    self.addEdge(self.image.shape[1]*y + x, self.backgroundNodeIndex, self.K, self.K)
                    self.addEdge(self.image.shape[1]*y + x, self.foregroundNodeIndex, 0, 0)
                elif(self.mask[y, x] == 2): #foreground
                    self.addEdge(self.image.shape[1]*y + x, self.backgroundNodeIndex, 0, 0)
                    self.addEdge(self.image.shape[1]*y + x, self.foregroundNodeIndex, self.K, self.K)
                else: # others
                    backgroundWeight = -log(self.gmms['background'].probability(np.array([self.image[y, x]]))[0] + sys.float_info.epsilon) # TODO: Better handling
                    foregroundWeight = -log(self.gmms['foreground'].probability(np.array([self.image[y, x]]))[0] + sys.float_info.epsilon)

                    self.addEdge(self.image.shape[1]*y + x, self.backgroundNodeIndex, backgroundWeight, backgroundWeight)
                    self.addEdge(self.image.shape[1]*y + x, self.foregroundNodeIndex, foregroundWeight, foregroundWeight)


    def __calcBeta(self):
        beta = 0.
        for y in range(self.image.shape[0]):
            for x in range(self.image.shape[1]):
                # Only need to treat upper pixels and left pixel since we go to the others after
                if x > 0: # left
                    diff = self.image[y, x] - self.image[y, x-1]
                    beta += diff.dot(diff)
                if y > 0 and x > 0: # upleft
                    diff = self.image[y, x] - self.image[y-1, x-1]
                    beta += diff.dot(diff)
                if y > 0: # up
                    diff = self.image[y, x] - self.image[y-1, x]
                    beta += diff.dot(diff)
                if y > 0 and x < self.image.shape[1]-1: # upright
                    diff = self.image[y, x] - self.image[y-1, x+1]
                    beta += diff.dot(diff)
        
        if beta < sys.float_info.epsilon:
            beta = 0
        else:
            beta = 1. / (2 * beta/(4*self.image.shape[1]*self.image.shape[0] - 3*self.image.shape[0] - 3*self.image.shape[1] + 2))
        
        self.beta = beta

    def applyMincut(self):
        matrix = self.toMatrix()

        resultMatix = mincut(matrix, self.foregroundNodeIndex, self.backgroundNodeIndex)
        
        finalForegroundListMask = np.array(resultMatix[self.foregroundNodeIndex]) != 0
        finalBackgroundListMask = np.array(resultMatix[self.backgroundNodeIndex]) != 0

        finalForegroundMask = np.zeros(self.image.shape[:2], dtype=bool)
        finalBackgroundMask = np.zeros(self.image.shape[:2], dtype=bool)
        for y in range(self.image.shape[0]):
            finalForegroundMask[y, :] = finalForegroundListMask[y*self.image.shape[1]:(y+1)*self.image.shape[1]]
            finalBackgroundMask[y, :] = finalBackgroundListMask[y*self.image.shape[1]:(y+1)*self.image.shape[1]]
        
        
        self.foregroundImage = np.copy(self.image)
        self.foregroundImage[finalForegroundMask == False] = 0
        self.backgroundImage = np.copy(self.image)
        self.backgroundImage[finalForegroundMask == False] = 0