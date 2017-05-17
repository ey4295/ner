"""
tool program of twitter
"""
import re
import string
from string import lower

from nltk import word_tokenize, PorterStemmer
from pandas import json
from pprint import pprint

import pymysql
from twitter import *


def get_namelist():
    """
    get all names from mysql db people table name_list
    :return: list of names
    """
    connection = pymysql.connect(host='127.0.0.1',
                                 port=3306,
                                 user='root',
                                 password='123456',
                                 db='people',
                                 cursorclass=pymysql.cursors.DictCursor)

    sql = 'select name from name_list;'
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    connection.commit()
    connection.close()
    return result


def get_twitter_data(name, num):
    """
    get data from twitter api
    :param:name you'd like to search--with _
    :param: number of tweets you want
    :return: text data
    """
    auth = OAuth('862644832442789894-2vWBy8SIEUKLKQWRnTvSWO3gv0rsb9F', '9PWQN0SMGxkgxmU8O0gP8c3EIelyHO7KyCPcodhRdc6DL'
                 , 'SKjZV8CKLNnXKCINixEd0ubTc', 'NKt17D4qjAVDd6E8oeD3TiT7FLjhZFaSqRS8ICcBfSGJUPpQLw')
    twitter_stream = TwitterStream(auth=auth)
    # iter = twitter_stream.statuses.sample()
    iter = twitter_stream.statuses.sample()
    count = 0
    for tweet in iter:
        if count > num:
            break
        tweet=json.dumps(tweet)
        text=tweet['text']
        hashtags=tweet['entities']['hashtags']
        count += 1
    # return [clean_twitter(status['text'],name) for status in statuses]
    return None


def clean_twitter(text, name,exclude):
    """
    data clean for tweets
    :param name: person name searched--with
    :param text: each tweet
    :return: cleaned tweet
    """
    stemmer=PorterStemmer()
    name = re.sub('_', ' ', name)
    pattern = '((#|@|http)[\w\./\:]+\s?)|{0}|RT|(\.\.\.)|(que)|(amp)|(vote)|(\'n\'t\')'.format(name)
    text=re.sub(pattern, ' ', text).strip()

    text = lower(text)
    words = word_tokenize(text)
    words = filter(lambda x: x not in exclude and len(x)>2 and not unicode.isdigit(x) and x!='n\'t', words)
    words=[stemmer.stem(word) for word in words]
    return words


def sentiment_analysis(text):
    """
    conduct sentiment analysis on text
    :param text:
    :return: neg or pos
    """
    pass
