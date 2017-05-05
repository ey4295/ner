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
        4.Store result in


"""
def save_in_mongo(key_vals,name):
    """
    store key values in mongodb
    :param key_vals: list of key values
    :param doc name
    :return: id or boolean value for success or not
    """
    pass

def ner_analyse(text):
    """
    extract human activity information from text
    :param text: doc
    :return: list of tuple(activity elements)
    """
    pass

def save_in_mysql(list):
    """
    store structural data into mysql
    :param list: list of tuples
    :return: id or boolean value for success or not
    """
    pass

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


def ner():
    # todo scrape data from wikipeida
    # todo find structure data and un-structual text
    text=''
    dict={}
    list=[]
    save_in_mongo(dict)
    ner_analyse(text)
    save_in_mysql(list)


def sa(text):
    """
    sentiment analysis on text
    :param text: doc you would like to conduct sentiment analysis
    :return: boolean value of neg or pos
    """
    pass
