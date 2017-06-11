"""
evaluation problem
"""
########################################################################################################
# ner evaluation
#
########################################################################################################

# todo 1.evaluate with moretags(gmb corpus)
# from nltk import pos_tag, word_tokenize, tree2conlltags, conlltags2tree
#
# from moretags import read_gmb, corpus_root, NamedEntityChunker
#
# reader = read_gmb(corpus_root,1000)
# data = list(reader)
# training_samples = data[:int(len(data) * 0.9)]
# test_samples = data[int(len(data) * 0.9):]
#
# print "#training samples = %s" % len(training_samples)  # training samples = 55809
# print "#test samples = %s" % len(test_samples)  # test samples = 6201
# print (test_samples[0])
# chunker = NamedEntityChunker(training_samples[:1000])
# score = chunker.evaluate([conlltags2tree([(w, t, iob) for (w, t), iob in iobs]) for iobs in test_samples[:500]])
#
# print ('accuracy={}'.format(score))
# ner=chunker.parse(pos_tag(word_tokenize(" Jobs was diagnosed "
#                                         "with a pancreatic neuroendocrine "
#                                         "tumor in 2003 and died on October "
#                                         "5, 2011, of respiratory arrest related to the tumor. ")))
# #ner.draw()
# #flat_ner=ner.flatten()
# #print (flat_ner)
# #print (type(flat_ner))
#
# print (tree2conlltags(ner))

########################################################################################################
#   evaluation for sentiment analysis
#
########################################################################################################
import os
from _license import isfile, join
from random import shuffle


from sklearn.metrics import auc
from sklearn.metrics import precision_recall_curve
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

path = '/home/xuqh/Downloads/sentiment-master/tweets_train'
pos, neg = [], []


# read file
# put into list
# shuffle
# all test samples---evaluate

def get_max(x):
    """
    get max value of pos or neg
    :param x:
    :return:
    """
    return int(x['pos'] >= x["neg"]) * 2 - 1


def get_prob(x):
    return max(x['pos'], x['neg'])


def eval(labels, testing_samples):
    """
    evaluation
    :param labels: predicted labels
    :param testing_samples: samples with labels
    :return:
    """

    n = len(labels)
    correct = 0
    for i in range(n):
        if labels[i] == testing_samples[i][1]:
            correct += 1


pos_names = [f for f in os.listdir(os.path.join(path, "pos")) if isfile(join(path, "pos", f))]
for name in pos_names:
    if len(pos) >= 500:
        break
    else:
        f = open(os.path.join(path, "pos", name))
        pos.append((f.readline(), 1))
        f.close()

neg_names = [f for f in os.listdir(os.path.join(path, "neg")) if isfile(join(path, "neg", f))]
for name in neg_names:
    if len(neg) >= 500:
        break
    else:
        f = open(os.path.join(path, "neg", name))
        neg.append((f.readline(), -1))
        f.close()

testing_samples = pos + neg
shuffle(testing_samples)
features = [x[0] for x in testing_samples]
gold = [x[1] for x in testing_samples]
sia = SentimentIntensityAnalyzer()

labels = [get_prob(sia.polarity_scores(x)) for x in features]
# k fold
accuracy = []
import matplotlib.pyplot as plt

for i in range(10):
    testing_fold = testing_samples[i * 100:(i + 1) * 100]
    testing_labels=[x[1] for x in testing_fold]
    predicted_labels = labels[i * 100:(i + 1) * 100]
    precision, recall, _ = precision_recall_curve(testing_labels,predicted_labels)
    print (len(predicted_labels))
    lab = 'Fold %d AUC=%.4f' % (i + 1, auc(recall, precision))
    plt.step(recall, precision, label=lab)
    accuracy.append(eval(predicted_labels, testing_fold))
plt.legend(loc='lower left', fontsize='small')
plt.xlabel('Precision')
plt.ylabel('Recall')
plt.title('10 Fold Cross-Validation P-R Curve')
# plt.show()
plt.savefig('pr.png')
# fig, ax = plt.subplots()
# ax.plot([1,2,3],'ko-',label='line1')
# ax.plot([2,4,3],'ro-',label='lin2')
# ax.plot([1,5,9],'bo-',label='lin3')
# ax.set_xticklabels(['','A','B','C',''])
# plt.show()
# fig, ax = plt.subplots()
# ax.set_xlim(0, 5)
# key, val, m = [1, 2, 3, 4], [0, 41.1, 61.4, 61.9], ['o', 'x', 's', '^']
# for (k, v, m_) in zip(key, val, m):
#     print (k, v, m_)
#     ax.scatter(k, v, marker=m_)
# ax.plot([1, 2, 3, 4], val, color='black')
# for (x, y) in zip([1, 2, 3, 4], val):
#     ax.annotate('  {}'.format(y), xy=(x, y), color='blue')
# ax.set_xticklabels(["", 'History \nFeature', 'Position \nFeature', 'Word \nFeature', 'All \nFeatures', ""])
# plt.title("F1 scores With Different Features")
# plt.savefig('F1.png')

# compare semi and supervised
# import matplotlib.pyplot as plt
# fig, ax = plt.subplots()
# ax.set_xlim(0, 5)
# semi = [92.1, 57.1, 67.6, 61.9]
# normal = [91.0, 50, 48,55]
# index=[1,2,3,4]
# m=['o', 'x', 's', '^']
# for (i,s,n,m_ )in zip(index,semi,normal,m):
#     ax.scatter(i,s,marker=m_)
#     ax.scatter(i,n,marker=m_)
#
# ax.plot([1, 2, 3, 4], semi, color='red')
# ax.plot([1, 2, 3, 4], normal, color='green')
# for (x, s,n) in zip([1, 2, 3, 4], semi,normal):
#     ax.annotate(' {}'.format(s), xy=(x, s), color='blue')
#     ax.annotate('     {}'.format(n), xy=(x, n), color='blue')
# ax.set_xticklabels(["", 'Accuracy', 'Precision', 'Recall', 'F1 Scores', ""])
# plt.title("Semi-Supervised CRFs vs CRFs")
# plt.savefig('compare.png')
