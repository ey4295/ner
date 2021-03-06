import matplotlib.pyplot as plt
import numpy
from sklearn.datasets import make_blobs
from sklearn.metrics import precision_recall_curve, auc
from sklearn.model_selection import KFold
from sklearn.svm import SVC

FOLDS = 5

X, y = make_blobs(n_samples=1000, n_features=2, centers=2, cluster_std=10.0,
                  random_state=12345)





k_fold = KFold(n_splits=FOLDS, shuffle=True, random_state=12345)
predictor = SVC(kernel='linear', C=1.0, probability=True, random_state=12345)

y_real = []
y_proba = []
for i, (train_index, test_index) in enumerate(k_fold.split(X)):
    Xtrain, Xtest = X[train_index], X[test_index]
    ytrain, ytest = y[train_index], y[test_index]
    predictor.fit(Xtrain, ytrain)
    pred_proba = predictor.predict_proba(Xtest)
    precision, recall, _ = precision_recall_curve(ytest, pred_proba[:, 1])
    print (precision)
    lab = 'Fold %d AUC=%.4f' % (i + 1, auc(recall, precision))
    plt.step(recall, precision, label=lab)
    y_real.append(ytest)
    y_proba.append(pred_proba[:, 1])


plt.legend(loc='lower left', fontsize='small')

plt.tight_layout()
plt.savefig('result.png')
