"""
ner tool
"""
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
import ner
import bs4
import nltk
from nltk import pos_tag, word_tokenize

from pymongo import MongoClient
from twitter import *

import moretags
import pymysql

# mongoDB
client = MongoClient()
db = client.people
collection = db.properties


def save_in_mongo(key_vals,is_update):
    """
    store key values in mongodb
    :param key_vals: list of key values
    :param doc name
    :return: id or boolean value for success or not
    """
    if is_update:
        collection.upate(key_vals)
    else:
        collection.insert(key_vals)


def clean_data(text):
    """
    clean data ([]and ())
    :param text:string
    :return: cleaned string
    """
    pattern1 = '.*\[\d*\].*'
    pattern2 = '.*\(.*\).*'
    try:
        if re.match(pattern1, text):
            text = re.sub('\[\d*\]', '', text)
        if re.match(pattern2, text):
            text = re.sub('\(.*?\)', '', text)
    except Exception as err:
        print ('regular expression down')
    return text


def ner_analyse(text, chunker):
    """
    extract human activity information from text(filted text with only time labeled sent )
    :param text: doc
    :return: list of tuple(activity elements)
    """
    sents = nltk.sent_tokenize(text)
    result = []
    for sent in sents:
        if not re.match('(.*\d\d\d\d.*)|(.*\d\ds*)', sent):
            continue
        entities = chunker.parse(pos_tag(word_tokenize(sent)))
        entities = nltk.tree2conlltags(entities)
        has_per = False
        has_loc = False
        has_org = False
        has_tim = False
        print ('Analysing following sentence:\n{0}'.format(sent.encode('utf-8')))
        for entity in entities:
            # print('Etity[2] is \n{0}'.format(entity[2]))
            if entity[2] == 'B-per':
                has_per = True
            elif entity[2] == 'B-tim':
                has_tim = True
            elif entity[2] == 'B-loc':
                has_loc = True
            elif entity[2] == 'B-org':
                has_org = True
        if has_per and has_tim and (has_loc or has_org):
            # nltk.conlltags2tree(entities).draw()
            print ('Yes!  This sentence has per tim and org|loc\n'
                   'Its entities are like:\n {0}'.format(entities))
            result.append(entities)
        else:
            print ('No! This sentence does not meet our standard\n'
                   'Its entities are like:\n{0}'.format(entities))

    return result


def ner_analyse_crfs(tagger, text):
    """
    Find activity sentence and analyse it
    :param text: doc
    :return: list of entities
    """
    # start server by java -mx1000m -cp stanford-ner.jar edu.stanford.nlp.ie.NERServer     -loadClassifier classifiers/english.muc.7class.distsim.crf.ser.gz     -port 4295 -outputFormat inlineXML
    sents = nltk.sent_tokenize(text)
    result = []
    tags = set(['PERSON', 'LOCATION', 'ORGANIZATION', 'DATE'])

    for sent in sents:
        if not re.match('(.*\d\d\d\d.*)|(.*\d\ds*)', sent):
            continue
        # get verb
        pos_tags = pos_tag(word_tokenize(sent))
        tag = ''
        VBS = []
        for pos in pos_tags:
            if re.match('VB.*', pos[1]):
                if not tag == '':
                    tag = tag + ' ' + pos[0]
                else:
                    tag += pos[0]
            elif not tag == '':
                VBS.append(tag)
                tag = ''
        l = len(VBS)
        new_VBS = []
        count = random.randint(1, 3)
        if count > l:
            count = l
        indices = random.sample(range(count), count)
        for index in indices:
            new_VBS.append(VBS[index])
        entities = {'VB': '|'.join(new_VBS)}
        # get entities
        crf_entities = tagger.get_entities(sent)
        for (key, val) in crf_entities.items():

            if key in tags:
                # trick for special form stanford ner generate
                val = re.search('<{}>(.*?)<'.format(key), val[0]).group(1)
                entities.update({key: val})
                """
            elif key=='O':
                new_val=[]
                l=len(val)
                count=random.randint(1,l+1)
                indices=random.sample(range(count),count)
                for index in indices:
                    new_val.append(val[index])
                entities.update({key: new_val})
                """
        result.append(entities)
    return result


def extract_rels(entities_list):
    """
    convert list of entities to tables  for mysql
    :param entities_list:
    :return: list of dict
    """
    tags = set(['B-tim', 'B-org', 'B-geo'])
    rels = []
    for entities in entities_list:
        i = 0
        rel = {}
        while i < len(entities):
            entity = entities[i]
            if entity[2][2:] == 'org' or entity[2][2:] == 'geo':
                before_org = False
            if re.match('VB.*', entity[1]):
                key = 'vb'
                val = entity[0]
                j = i + 1
                while re.match('VB.*', entities[j][1]):
                    val = val + ' ' + entities[j][0]
                    j += 1
                rel.update({key: val})

            if entity[2] in tags:
                key = entity[2][2:]
                val = entity[0]
                j = i + 1
                while entities[j][2][0] == 'I':
                    val = val + ' ' + entities[j][0]
                    j += 1
                rel.update({key: val})
            i += 1
        rels.append(rel)
    return rels


def save_in_mysql(name, list):
    """
    store structural data into mysql
    :param list: list of dict
    :return: id or boolean value for success or not
    """
    connection = pymysql.connect(host='127.0.0.1',
                                 port=3306,
                                 user='root',
                                 password='123456',
                                 db='people',
                                 cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()
    # save name && get id
    if not list:
        return None

    sql = 'insert into name_list(name) values(%s);'
    cursor.execute(sql, name)
    person_id=cursor.lastrowid
    for dict in list:
        if 'PERSON' not in dict:
            dict['PERSON'] = re.sub('_', ' ', name)
        var_name, var_value, count = 'person_id', '%s{}', len(dict.keys())
        for (key, val) in dict.items():
            var_name += (',' + key)

        var_value = var_value.format(',%s' * count)
        sql = 'insert into activity({0}) values({1});'.format(var_name, var_value)

        cursor.execute(sql, [person_id] + dict.values())
    connection.commit()
    connection.close()
    return person_id


def ner_eval(chunker, test_samples):
    """
    evaluate named entity recognition accuracy
    :return:
    """
    score = chunker.evaluate(
        [nltk.conlltags2tree([(w, t, iob) for (w, t), iob in iobs]) for iobs in test_samples[:500]])
    return score.accuracy()


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
    # todo key can not contain .
    if len(info_card) > 0:
        info_card = info_card[0]
        # print (info_card)
        # trs = info_card.findChildren() children means all children including indirect children
        trs = info_card.find_all('tr')
        result = {}
        key = 'Name'
        val = uri[6:]
        result.update({key: val})
        for tr in trs:
            if len(tr.find_all('th')) == 1:
                is_key = True
                key = tr.find('th').get_text()
                key = re.sub('\.', ' ', key)
                val = ''
                tds = tr.find_all('td')
                # 1 value text,several value list
                if len(tds) == 1:
                    val = tds[0].get_text()
                else:
                    for td in tds:
                        val = []
                        val.append(td.get_text())
                result.update({key: val})
    else:
        result = None

    # get un-structral text
    text = mw_content_text.find('p').get_text()
    return links, result, text
