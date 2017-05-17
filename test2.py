"""
test file
"""
import random

import nltk
import pymysql
from nltk import word_tokenize
from numpy import where, ndarray
from pandas import Series
from pymongo import MongoClient, cursor

from ner_tool import save_in_mysql

text = """
A biography is a detailed description or account of someone's
life. More than a list of basic facts (education, work, relationships, and death),
 a biography also portrays a subject's experience of these events. Unlike a
 profile or curriculum vitae , a biography presents a subject's life story,
 highlighting various aspects of his or her life, including intimate
 details of experience, and may include an analysis of a subject's personality."""
# tokens = word_tokenize(text)
# sents = nltk.sent_tokenize(text)
# tokens = word_tokenize(str(sents))
#
# st = 'hello 2017 '
# result = nltk.re.match('.*\d\d\d\d.*', st)
# result.group(0)
# print (result.group(0))
# print ('Tokens are {0}'.format(sents))
# print (type(sents[1]))

"""
client=MongoClient()
db=client.people
connection=db.properties
data={'hhh':'fasdu'}
result=connection.insert(data)
print (result)
print (connection.find_one())

st = 'hello'
print (st == 'hello')

connection=pymysql.connect(host='127.0.0.1',
                             port=3306,
                             user='root',
                             password='123456',
                             db='people',
                             cursorclass=pymysql.cursors.DictCursor)
cursor=connection.cursor()
#insert
sql='insert into name_list(name) values(%s)'
effect_rows=cursor.execute(sql,('xuqh',))
connection.commit()
cursor.close()
connection.close()


import ner

tagger = ner.SocketNER(host='localhost', port=4295,output_format='slashTags')
entities = tagger.get_entities("Jobs and Wozniak co-founded Apple in 1976 to sell Wozniak's Apple I personal computer. ")
print (entities)
pos=nltk.pos_tag(word_tokenize('Jobs and Wozniak co-founded Apple in 1976 to sell Wozniaks Apple I personal'))
print (pos)

a=random.randint(0,2)
l=range(2)
print (random.sample(l,5))

print (tuple(entities.keys()))
print 'fjalsdjfl{0}  {1}'.format(tuple(l))

a=set([1,2,3])
a=a.difference(set([1,2]))
print a
a=[1,2,2,3,4]
print (a.index(2))
print (random.randint(0,100)/100.00)

import pandas as pd
pd.read_table('')

a=[1,2,3]
b=Series(a)*2+4
print (Series([b,b]))

########################################################################################################
#
#
########################################################################################################
#twitter api
from twitter import *
t=Twitter(auth=OAuth('862644832442789894-2vWBy8SIEUKLKQWRnTvSWO3gv0rsb9F',
'9PWQN0SMGxkgxmU8O0gP8c3EIelyHO7KyCPcodhRdc6DL'
                     ,'SKjZV8CKLNnXKCINixEd0ubTc','NKt17D4qjAVDd6E8oeD3TiT7FLjhZFaSqRS8ICcBfSGJUPpQLw'))
tweets=t.search.tweets(q='steve jobs',count=100)
statuses=tweets['statuses']
for status in statuses:
    nltk.pprint(nltk.word_tokenize(status['text']) )

from collections import Counter
from sklearn.datasets import make_classification
from imblearn.over_sampling import     SMOTE
X, y = make_classification(n_classes=3, class_sep=2,
weights=[0.1, 0.8,0.1], n_informative=3, n_redundant=1, flip_y=0,
n_features=20, n_clusters_per_class=1, n_samples=1000, random_state=10)
print (y)
print('Original dataset shape {}'.format(Counter(y)))
sm = SMOTE(random_state=42,kind='borderline1')
X_res, y_res = sm.fit_sample(X, y)
print('Resampled dataset shape {}'.format(Counter(y_res)))"""
# import numpy as np
# X = np.random.randint(5, size=(6, 100))
# print (X)
# y = np.array([1, 2, 3, 4, 5, 6])
# from sklearn.naive_bayes import MultinomialNB
# clf = MultinomialNB()
# clf.fit(X, y)
# print ('x[2:3]\n\n\n\n\n{0}'.format(X[9:10]))
# print(clf.predict(X[2:3]))

# import numpy as np
# sents=['life is happy','you are disapointing','here we go']
# labels=[1,-1,1]
# X=np.array([])
# for sent in sents:
#     words=word_tokenize(sent)
#     words=np.array(words)
#     np.vstack((X,words))
#
# print ('X is \n{0}'.format(X))

# dict={u'asdfk':3,2:4,5:8}
# print (dict)
# a=[1,2,2,3,4,4]
# print (a[3:-1])
# pattern='<DATE>(.*?)<'
# s='In <DATE>2006< >, Lane received a star on the Hollywood Walk of Fame, and in <DATE>2008<'
# result=nltk.re.search(pattern,s).group(1)
# print(result)

# l=[{'PERSON':'123','ORGANIZATION':'APPLE'}]
# name='12345'
# save_in_mysql(name,l)

########################################################################################################
# FreqDist Usage
#
########################################################################################################
# a=['a','a','a','b','b','b','b','d']
# fd= nltk.FreqDist(a)
# print (fd.most_common(3))

# mongoDB
client = MongoClient()
db = client.people
collection = db.properties
result=collection.find_one({'Name':'xuqh'})
nltk.pprint(result)