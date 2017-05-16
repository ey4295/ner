"""
===========
SMOTE + ENN
===========

An illustration of the SMOTE + ENN method.

"""

# Authors: Christos Aridas
#          Guillaume Lemaitre <g.lemaitre58@gmail.com>
# License: MIT

import matplotlib.pyplot as plt
from pandas import Series
from sklearn.datasets import make_classification
from sklearn.decomposition import PCA

from imblearn.combine import SMOTEENN

print(__doc__)

# Generate the dataset
X, y = make_classification(n_classes=2, class_sep=2, weights=[0.2,0.8],
                           n_informative=3, n_redundant=1, flip_y=0,
                           n_features=20, n_clusters_per_class=1,
                           n_samples=100, random_state=10)

print ('samples are \n{0},\n\n\nlabels are\n{1}'.format(X,y))
s0=0
s1=0
s2=0
for y_i in y:
    if y_i==0:
        s0+=1
    elif y_i==1:
        s1+=1
    else:
        s2+=1
print ('s0={0} s1={1} s2={2} s={3}'.format(s0,s1,s2,s0+s1+s2))
# Instanciate a PCA object for the sake of easy visualisation
pca = PCA(n_components=2)
# Fit and transform x to visualise inside a 2D feature space
X_vis = pca.fit_transform(X)

# Apply SMOTE + ENN
sm = SMOTEENN(ratio=1.0)

X_resampled, y_resampled = sm.fit_sample(X, y)
s0=0
s1=0
s2=0
for y_i in y_resampled:
    if y_i==0:
        s0+=1
    elif y_i==1:
        s1+=1
    else:
        s2+=1
print ('s0={0} s1={1} s2={2} s={3}'.format(s0,s1,s2,s0+s1+s2))
X_res_vis = pca.transform(X_resampled)
#print ('samples are \n{0},\n\n\nlabels are\n{1}'.format(X_resampled,y_resampled))
#x=Series.describe(Series(y_resampled))
#print (x)
# Two subplots, unpack the axes array immediately
f, (ax1, ax2) = plt.subplots(1, 2)

c0 = ax1.scatter(X_vis[y == 0, 0], X_vis[y == 0, 1], label="Class #0",
                 alpha=0.5)
c1 = ax1.scatter(X_vis[y == 1, 0], X_vis[y == 1, 1], label="Class #1",
                 alpha=0.5)
ax1.set_title('Original set')

ax2.scatter(X_res_vis[y_resampled == 0, 0], X_res_vis[y_resampled == 0, 1],
            label="Class #0", alpha=0.5)
ax2.scatter(X_res_vis[y_resampled == 1, 0], X_res_vis[y_resampled == 1, 1],
            label="Class #1", alpha=0.5)
ax2.set_title('SMOTE + ENN')

# make nice plotting
for ax in (ax1, ax2):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    ax.spines['left'].set_position(('outward', 10))
    ax.spines['bottom'].set_position(('outward', 10))
    ax.set_xlim([-6, 8])
    ax.set_ylim([-6, 6])

f.legend((c0, c1), ('Class #0', 'Class #1'), loc='lower center',
         ncol=2, labelspacing=0.)
plt.tight_layout(pad=3)

#plt.show()
