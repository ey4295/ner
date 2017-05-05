"""
This is simply a practicing demo of nltk package.
"""

# data
import nltk

#nltk.download('averaged_perceptron_tagger')
from nltk.corpus import conll2002

nltk.download('maxent_ne_chunker')
nltk.download('words')


document = 'The fourth Wells account moving to another agency ' \
           'is the packaged paper-products division of Georgia-Pacific Corp., which arrived ' \
           'at Wells only last fall. Like Hertz and the History Channel, it is also leaving for' \
           ' an Omnicom-owned agency, the BBDO South unit of BBDO Worldwide. BBDO South in Atlanta' \
           ', which handles corporate advertising for Georgia-Pacific, will assume additional duties ' \
           'for brands like Angel Soft toilet tissue and Sparkle paper towels, said Ken Haldin, a ' \
           'spokesman for Georgia-Pacific in Atlanta.'

# sentence segment
sentences = nltk.sent_tokenize(document)
print ('Segmented sentences are like below:\n{0}'.format(sentences))

# word segment
sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
print ('Segmented words tokens are like below:\n{0}'.format(sentences))

# part-of-speech tagger
sentences = [nltk.pos_tag(sentence) for sentence in sentences]
print ('Tagged sentences are like:\n{0}'.format(sentences))

# chunking
sentence = [("the", "DT"), ("little", "JJ"), ("yellow", "JJ"),
            ("dog", "NN"), ("barked", "VBD"), ("at", "IN"), ("the", "DT"), ("cat", "NN")]
grammar = "NP: {<DT>?<JJ>*<NN>}"
cp = nltk.RegexpParser(grammar)
result=cp.parse(sentence)
print ('The chunked sentence is shown as below:\n{0}'.format(result))
#result.draw()

# use chunkparser to decide chunk grammar
# nltk.app.chunkparser()

# named entity recognition
## corpus example
sent = nltk.corpus.treebank.tagged_sents()[21]
ne_sent=nltk.ne_chunk(sent)
print ('Example tagged sentence is: \n{0}'.format(ne_sent))


vnv = """
 (
 is/V|    # 3rd sing present and
 was/V|   # past forms of the verb zijn ('be')
 werd/V|  # and also present
 wordt/V  # past of worden ('become)
 )
 .*       # followed by anything
 van/Prep # followed by van ('of')
 """
VAN = nltk.re.compile(vnv, nltk.re.VERBOSE)
for doc in conll2002.chunked_sents('ned.train'):
   print (doc)
   for r in nltk.sem.extract_rels('PER', 'ORG', doc,
                                   corpus='conll2002', pattern=VAN):
       #print(nltk.sem.clause(r, relsym="VAN"))
       print(nltk.rtuple(r, lcon=True, rcon=True))