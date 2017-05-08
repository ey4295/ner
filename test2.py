"""
test file
"""
import nltk
import pymysql
from nltk import word_tokenize
from pymongo import MongoClient, cursor

text = """
A biography is a detailed description or account of someone's
life. More than a list of basic facts (education, work, relationships, and death),
 a biography also portrays a subject's experience of these events. Unlike a
 profile or curriculum vitae , a biography presents a subject's life story,
 highlighting various aspects of his or her life, including intimate
 details of experience, and may include an analysis of a subject's personality."""
tokens = word_tokenize(text)
sents = nltk.sent_tokenize(text)
tokens = word_tokenize(str(sents))

st = 'hello 2017 '
result = nltk.re.match('.*\d\d\d\d.*', st)
result.group(0)
print (result.group(0))
print ('Tokens are {0}'.format(sents))
print (type(sents[1]))

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
"""

import ner

tagger = ner.SocketNER(host='localhost', port=4295,output_format='slashTags')
entities = tagger.get_entities("Jobs and Wozniak co-founded Apple in 1976 to sell Wozniak's Apple I personal computer. ")
print (entities)
