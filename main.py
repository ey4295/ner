"""
This is the main programme of my final design.
This programme accomplished the following goals:
    Part 1:
        Named Entity Recognition
        1.Scrape data from wikipedia
        2.Find structural property and un-structural text
        3.Store structural property in MongoDB
        4.Analyse un-structural text to find human activity
        5.Store human activity information into Mysql

    Part 2:
        Sentiment Analysis
        1.Use Twitter api to download twits
        2.Analyse text to find neg or pos sentiment
        3.Find top 5 topics and analyse neg or pos sentiment for them
        4.Store result in MongoDB


"""
import random
import re
from urllib import urlopen

import bs4
import nltk
from nltk import pos_tag, word_tokenize
import  pymongo
from pymongo import MongoClient

import moretags

reader = moretags.read_gmb(moretags.corpus_root, 1000)
data = list(reader)
training_samples = data[:int(len(data) * 0.9)]
test_samples = data[int(len(data) * 0.9):]
chunker = moretags.NamedEntityChunker(training_samples[:5000])
print "#training samples = %s" % len(training_samples)  # training samples = 55809
print "#test samples = %s" % len(test_samples)  # test samples = 6201

#mongoDB
client=MongoClient()
db=client.people
collection=db.properties

def save_in_mongo(key_vals):
    """
    store key values in mongodb
    :param key_vals: list of key values
    :param doc name
    :return: id or boolean value for success or not
    """
    collection.insert(key_vals)


def ner_analyse(text):
    """
    extract human activity information from text(filted text with only time labeled sent )
    :param text: doc
    :return: list of tuple(activity elements)
    """
    sents = nltk.sent_tokenize(text)
    result = []
    for sent in sents:
        if re.match('(.*\d\d\d\d.*)|(.*\d\ds.*)', sent) != None:
            entities=chunker.parse(pos_tag(word_tokenize(sent)))
            entities=nltk.tree2conlltags(entities)
            has_per=False
            has_loc=False
            has_org=False
            has_tim=False
            for entity in entities:
                if entity[2]=='B-per':
                    has_per=True
                elif entity[2]=='B-tim':
                    has_tim=True
                elif entity[2]=='B-loc':
                    has_loc=True
                elif entity[2]=='B-org':
                    has_org=True
                if has_per and has_tim and (has_loc or has_org):
                    result.append(entities)
    return result


def save_in_mysql(list):
    """
    store structural data into mysql
    :param list: list of tuples
    :return: id or boolean value for success or not
    """
    pass

def ner_eval(chunker):
    """
    evaluate named entity recognition accuracy
    :return:
    """
    score = chunker.evaluate([nltk.conlltags2tree([(w, t, iob) for (w, t), iob in iobs]) for iobs in test_samples[:500]])
    return score.accuracy()

def get_twitter_data():
    """
    get data from twitter api
    :return: text data
    """
    pass


def sentiment_analysis(text):
    """
    conduct sentiment analysis on text
    :param text:
    :return: neg or pos
    """
    pass


def get_info(uri):
    """
    This function finds all links and text from uri you give
    :param uri: article uri on wikipedia
    :return: a list of links on that page,structural data,un-structural data
    """
    html = urlopen("http://en.wikipedia.org{0}".format(uri))
    html_soup = bs4.BeautifulSoup(html)
    links = html_soup.find('div', {'id': 'bodyContent'}).find_all('a',
                                                                  href=re.compile('^(/wiki/)((?!:).)*$'))

    # get structural data
    mw_content_text = html_soup.find('div', {'id': 'mw-content-text'})
    # print (mw_content_text)
    info_card = mw_content_text.find_all('table', {'class': re.compile('infobox.*')})
    # print (info_card)
    #todo key can not contain .
    if len(info_card) > 0:
        info_card = info_card[0]
        # print (info_card)
        # trs = info_card.findChildren() children means all children including indirect children
        trs = info_card.find_all('tr')
        result = {}
        key = 'name'
        val = uri[6:]
        result.update({key:val})
        for tr in trs:
            if len(tr.find_all('th')) == 1:
                is_key = True
                key = tr.find('th').get_text()
                val = ''
                tds = tr.find_all('td')
                # 1 value text,several value list
                if len(tds) == 1:
                    val = tds[0].get_text()
                else:
                    for td in tds:
                        val = []
                        val.append(td.get_text())
                result.update({key:val})
    else:
        result = None

    # get un-structral text
    text = mw_content_text.find('p').get_text()
    return links, result, text


def ner(total):
    # scrape data from wikipeida
    uri = '/wiki/Kevin_Bacon'
    links, info, text = get_info(uri)
    names = set()
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
            print('Name of this page is {0}\nInformation Card\n{1}\nUri:{2}'
                  .format(name, info, uri))
            try:
                result = ner_analyse(text)
                #result.draw()
                #result= nltk.tree2conlltags(result)
                print (result)
            except Exception as err:
                print ('Named Entity Analysis Error:\n{0}'.format(err))

            #if result != []:
            #    result[0].draw()
            #print ("Named Entity Recognition result is \n{0}".format(result))

    list = []
    save_in_mysql(list)


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


ner(10)
