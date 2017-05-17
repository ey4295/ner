import random
import re
import string
from string import lower

import nltk
from nltk import word_tokenize, PorterStemmer, FreqDist
from pandas import json
from pprint import pprint

import ner
from twitter import *
from twitter import OAuth

import moretags
from ner_tool import get_info, save_in_mysql, save_in_mongo, clean_data, ner_analyse_crfs
from twitter_tool import get_namelist, get_twitter_data, clean_twitter, sentiment_analysis

from nltk.corpus import stopwords

path = '/media/maomao/7f986c26-c04a-4a07-b4ec-06862fc46045/xuqh'


# nltk.download('stopwords')
def ner_main(total):
    # corpus
    reader = moretags.read_gmb(moretags.corpus_root, 1000)
    data = list(reader)
    training_samples = data[:int(len(data) * 0.9)]
    test_samples = data[int(len(data) * 0.9):]
    chunker = moretags.NamedEntityChunker(training_samples[:5000])
    print "#training samples = %s" % len(training_samples)  # training samples = 55809
    print "#test samples = %s" % len(test_samples)  # test samples = 6201

    # scrape data from wikipeida
    uri = '/wiki/Kevin_Bacon'
    links, info, text = get_info(uri)
    names = set()
    tagger = ner.SocketNER(host='localhost', port=4295, output_format='slashTags')
    result = []
    while len(links) > 0 and len(names) < total:
        uri = links[random.randint(0, len(links) - 1)].attrs['href']
        name = uri[6:]
        if name not in names:
            names.add(name)
            print (name)
            try:
                links, info, text = get_info(uri)
                save_in_mongo(info,is_update=False)
            except Exception as err:
                print(err)
                continue
            # print('Name of this page is {0}\nInformation Card\n{1}\nUri:{2}'
            #      .format(name, info, uri))
            try:
                text = clean_data(text)
                """
                result = ner_analyse(text,chunker)
                rels=extract_rels(result)
                print ('Relations are \n\n\n{0}\n\n\n'.format(rels))
                """
                entities = ner_analyse_crfs(tagger, text)
                print ('crf analysis result is \n{0}'.format(entities))
                # result.draw()
                # result= nltk.tree2conlltags(result)
                # print ('Relation entities are like \n{0}'.format(result))
                save_in_mysql(name, entities)
            except Exception as err:
                print ('Named Entity Analysis Error:\n{0}'.format(err))
                # if result != []:
                #    result[0].draw()
                # print ("Named Entity Recognition result is \n{0}".format(result))


def twitter_main(num):
    """
    use twitter api to gather data and conduct sentiment analysis
    :param num:number of tweets
    :return: [{name:{pos_perc:val},{neg_perc:val},{topic1:{pos_perc:val},{neg_perc:val}}}]
    """
    names = get_namelist()[:5]
    stopws = set(stopwords.words('english'))
    punct = set(string.punctuation)
    exclude = stopws.union(punct)
    for row in names:
        name = row['name']
        auth = OAuth('862644832442789894-2vWBy8SIEUKLKQWRnTvSWO3gv0rsb9F',
                     '9PWQN0SMGxkgxmU8O0gP8c3EIelyHO7KyCPcodhRdc6DL'
                     , 'SKjZV8CKLNnXKCINixEd0ubTc', 'NKt17D4qjAVDd6E8oeD3TiT7FLjhZFaSqRS8ICcBfSGJUPpQLw')
        twitter_stream = TwitterStream(auth=auth)
        # iter = twitter_stream.statuses.sample()
        tweets_iter = twitter_stream.statuses.sample()
        count = 0
        word_dist = []
        for tweet in tweets_iter:
            print (count)
            if count > num:
                break
            tweet = json.dumps(tweet)
            tweet = json.loads(tweet)
            if 'text' in tweet:
                words = clean_twitter(tweet['text'], str(name), exclude)
                word_dist = word_dist + words
                count += 1
        word_dist = FreqDist(word_dist)
        word_top5 = word_dist.most_common(5)
        mongo_dict = {'Name': name, 'Top5': word_top5}
        save_in_mongo(mongo_dict,is_update=True)


def sa(text):
    """
    sentiment analysis on text
    :param text: doc you would like to conduct sentiment analysis
    :return: boolean value of neg or pos
    """
    text = ''
    data = get_twitter_data()
    sentiment_analysis(text)
    # todo find top 5 topics
    # todo store result in mongodb


# ner_main(10)
twitter_main(100)
