import numpy as np
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture as GMM

np.random.seed(2)
x = np.concatenate([np.random.normal(0, 2, 2000),
                    np.random.normal(5, 5, 2000),
                    np.random.normal(3, 0.5, 2000)])



clf = GMM(4, n_inter=500, random_state=3).fit(x)
xpdf = np.linspace(-10, 20, 1000)
density = np.exp(clf.score(xpdf))

plt.hist(x, 80)
plt.plot(xpdf, density)
plt.xlim(-10, 20)

