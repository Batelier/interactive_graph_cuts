from sklearn.cluster import KMeans
from scipy.stats import multivariate_normal as mvn
import numpy as np

class GMM:
    """
    Gaussian Mixture Model implementation 

    Constructor Parameters:

    clustersNumber (int) : number of gaussian distrubutions
    iterationsNumber (int) : number of oteration through the EM steps
    """

    def __init__(self, clustersNumber, iterationsNumber):
        self.clustersNumber = clustersNumber
        self.iterationsNumber = iterationsNumber

    def __estimateMeanCovariance(self, X, labeledX):
        dimension = X.shape[1]
        labelNames = np.unique(labeledX)

        self.means = np.zeros((self.clustersNumber, dimension))
        self.varianceCovariance = np.zeros((self.clustersNumber, dimension, dimension))
        self.weights = np.zeros(self.clustersNumber)

        for index, label in enumerate(labelNames):
            withLabel = X[labeledX == label]
            self.weights[index] = len(withLabel) / X.shape[0]
            self.means[index, :] = np.mean(withLabel, axis=0)
            deviationX = (withLabel - self.means[index, :])
            self.varianceCovariance[index, :, :] = np.dot(self.weights[index] * deviationX.T, deviationX) / np.sum(withLabel)



    def __initialize(self, X):
        """
        Initialize the Gaussian mixture parameters

        Parameters:
        X: training numpy array of shape (samplesNumber, dimension)
        """

        kmeans = KMeans(n_clusters=self.clustersNumber).fit(X)

        labeledX = kmeans.labels_

        self.__estimateMeanCovariance(X, labeledX)

    def __expectation(self, X):
        observationsNumber = len(X)

        self.gammas = np.zeros((observationsNumber, self.clustersNumber))

        for clusterIndex in range(self.clustersNumber):
            self.gammas[:, clusterIndex] = self.weights[clusterIndex] * mvn.pdf(X, self.means[clusterIndex, :], self.varianceCovariance[clusterIndex], allow_singular=True)
        
        self.gammas[self.gammas == 0] = np.finfo(np.float).eps

        self.gammas = self.gammas / (np.sum(self.gammas, axis=1)[:,np.newaxis])
    
    def __maximisation(self, X):
        observationsNumber = len(X)
        dimension = X.shape[1]

        self.weights = np.mean(self.gammas, axis = 0)

        self.means = np.dot(self.gammas.T, X) / np.sum(self.gammas, axis = 0)[:, np.newaxis]

        for clusterIndex in range(self.clustersNumber):
            x = X - self.means[clusterIndex, :]

            self.varianceCovariance[clusterIndex, :, :] = np.dot(self.gammas[:, clusterIndex] * x.T, x) / np.sum(self.gammas, axis = 0)[clusterIndex]
        
    def fit(self, X):
        dimension = X.shape[1]

        self.__initialize(X)

        for iteration in range(self.iterationsNumber):
            self.__expectation(X)
            self.__maximisation(X)
        
        return self
    
    def probabilitiesPerCluster(self, X):
        proba = np.zeros((X.shape[0], self.clustersNumber))

        for clusterIndex in range(self.clustersNumber):
            proba[:, clusterIndex] = self.weights[clusterIndex] * mvn.pdf(X, self.means[clusterIndex, :], self.varianceCovariance[clusterIndex])

        return proba
    
    def probability(self, X):
        return self.probabilitiesPerCluster(X).sum(axis=1)
    
    def labelPrediction(self, X):
        return self.probability(X).argmax(1)

