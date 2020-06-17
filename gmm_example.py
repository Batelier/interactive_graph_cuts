from src.gmm import GMM
import numpy as np
import matplotlib.pyplot as plt

clf = GMM(2, 30)

n_samples = 300

# generate random sample, two components
np.random.seed(0)

# generate spherical data centered on (20, 20)
shifted_gaussian = np.random.randn(n_samples, 2) + np.array([20, 20])

# generate zero centered stretched Gaussian data
C = np.array([[0., -0.7], [3.5, .7]])
stretched_gaussian = np.dot(np.random.randn(n_samples, 2), C)

# concatenate the two datasets into the final training set
X_train = np.vstack([shifted_gaussian, stretched_gaussian])

X_train = X_train + 30

clf.fit(X_train)

# display predicted scores by the model as a contour plot
x = np.linspace(0., 60., 500)
y = np.linspace(0., 70., 500)
X, Y = np.meshgrid(x, y)
XX = np.array([X.ravel(), Y.ravel()]).T
Z = clf.probability(XX)
Z = Z.reshape(X.shape)

CS = plt.contour(X, Y, Z, levels=100, cmap='RdGy')
plt.colorbar()

plt.scatter(X_train[:, 0], X_train[:, 1], .8)

plt.title('Negative log-likelihood predicted by a GMM')
plt.axis('tight')
plt.show()