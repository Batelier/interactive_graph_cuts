from .graph import Graph
from math import sqrt, exp
import sys


class GraphCut(Graph):
    def __init__(self, image, gamma=50, lamb=9):
        super(GraphCut, self).__init__()
        self.gamma = gamma
        self.diagonalGamma = self.gamma / sqrt(2) # gamma over the distance of the diagonal
        self.lamb = 9
        self.setImage(image)

    def setImage(self, image):
        self.image = image
        self.__calcBeta()

        for y in range(self.image.shape[0]):
            for x in range(self.image.shape[1]):
                nodeIndex = self.addNode()
                
                # N - Weights

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
