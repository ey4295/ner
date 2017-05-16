import random
import re
from pprint import pprint

import ner
from twitter import *
from twitter import OAuth

from ner_tool import get_info, save_in_mysql, save_in_mongo, clean_data, ner_analyse_crfs


def get_twitter_data(name,num):
    """
    get data from twitter api
    :param:name you'd like to search--with _
    :param: number of tweets you want
    :return: text data
    """
    t = Twitter(
        auth=OAuth('862644832442789894-2vWBy8SIEUKLKQWRnTvSWO3gv0rsb9F', '9PWQN0SMGxkgxmU8O0gP8c3EIelyHO7KyCPcodhRdc6DL'
                   , 'SKjZV8CKLNnXKCINixEd0ubTc', 'NKt17D4qjAVDd6E8oeD3TiT7FLjhZFaSqRS8ICcBfSGJUPpQLw'))

    tweets = t.search.tweets(q=name, count=num)
    statuses = tweets['statuses']
    return [clean_twitter(status['text'],name) for status in statuses]


def clean_twitter(text,name):
    """
    data clean for tweets
    :param name: person name searched--with
    :param text: each tweet
    :return: cleaned tweet
    """
    name=re.sub('_',' ',name)
    pattern='((#|@|http)[\w\./\:]+\s?)|{0}|RT'.format(name)
    return re.sub(pattern,' ',text).strip()



def sentiment_analysis(text):
    """
    conduct sentiment analysis on text
    :param text:
    :return: neg or pos
    """
    pass




def ner_main(total):
    # scrape data from wikipeida
    uri = '/wiki/Kevin_Bacon'
    links, info, text = get_info(uri)
    names = set()
    tagger = ner.SocketNER(host='localhost', port=4295, output_format='slashTags')
    result=[]
    while len(links) > 0 and len(names) < total:
        uri = links[random.randint(0, len(links) - 1)].attrs['href']
        name = uri[6:]
        if name not in names:
            names.add(name)
            print (name)
            try:
                links, info, text = get_info(uri)
                save_in_mongo(info)
            except Exception as err:
                print(err)
                continue
            # print('Name of this page is {0}\nInformation Card\n{1}\nUri:{2}'
            #      .format(name, info, uri))
            try:
                text = clean_data(text)
                """
                result = ner_analyse(text)
                rels=extract_rels(result)
                print ('Relations are \n\n\n{0}\n\n\n'.format(rels))
                """
                entities= ner_analyse_crfs(tagger,text)
                print ('crf analysis result is \n{0}'.format(entities))
                # result.draw()
                # result= nltk.tree2conlltags(result)
                # print ('Relation entities are like \n{0}'.format(result))
                save_in_mysql(name,entities)
            except Exception as err:
                print ('Named Entity Analysis Error:\n{0}'.format(err))

                # if result != []:
                #    result[0].draw()
                # print ("Named Entity Recognition result is \n{0}".format(result))



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

ner_main(10)
# data=get_twitter_data('donald_trump',100)
# for d in data:
#     print (d)