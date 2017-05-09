# coding: utf-8
# Manuel Aragonés maragones@outlook.com
# ### The following code transforms an HTML document containing newspieces and dumps it into csv files.

#testing this module

import urllib.request, json, time, re, random, hashlib, nltk.data
from collections import defaultdict
from bs4 import BeautifulSoup as bs
from nltk import word_tokenize
from nltk.tokenize.api import TokenizerI
from nltk.tokenize.treebank import TreebankWordTokenizer
import os



# hard coding direcotry with news articles
DIR = 'PATH'
FILENAME = 'FILE'


def load_html(dir_file, file_name):
    # function that loads html files
    with open(dir_file+file_name, 'r') as f:
                result = f.read()
                if len(result) > 0:
                    #print("Retrieving from cache:", url)
                    return result

html = load_html(dir_, filename)

# The text we want to id in order to split
string_ = 'Document 1 of 500L'
# Corresponding regular expression
regex_ = '\S+Document+\s+\d{1,5}+\S+of+\S+\d{1,5}'
# We can find all of the instances that comply with the regex
search_results = re.findall('\SDocument\s\d{1,5}\sof\s[\d]{1,4}\S',soup.text) # debugg
# We can also substitute
text_without_regex_ = re.sub('\SDocument\s\d{1,5}\sof\s[\d]{1,4}\S', 'XXXXXX',soup.text)
# The most efficient is to split
list_= re.split('Document\s\d{1,5}\sof\s[\d]{1,5}', soup.text)

# Helper function to slice text based on regular expressions
def slice_text(regex, text):
    return re.split(regex, text)

l = []
for i in range(1,8):
    REGEX = 'Document\s\d{1,5}\sof\s[\d]{1,5}'
    DIR = '/Users/manuelaragones/Dropbox/0_DeepDive/P/ANM/'
    html_ = load_html(DIR, '0'+str(i)+'_ProQuestDocuments-2016-03-03.html')
    soup = bs(html_, 'lxml')
    l.append(slice_text(REGEX, soup.text))
    # one single list
    ListOfTexts = [item for sublist in l for item in sublist]

def ArtToJSON(text):
    """
    Function that converts unstructured text from a specific source into a dictionary
    I: Html text
    O: JSON Array
    """
    try:
        d = {}
        d['Title'] =  re.findall('.+?(?=ProQuest\sdocument\slinkAbstract:)', text, re.DOTALL)
        # non-greedy look forward (do not include first string) ?<=
        # non-greedt look backward ?=        
        d['Full Text'] = re.findall('(?<=Full\stext:\s).+?(?=Publication\stitle: )', text, re.DOTALL)
        return json.dumps(d)
    except:
        pass
    

for i in range(1, len(ListOfTexts)):
    JSONi = ArtToJSON(ListOfTexts[i])
    with open('ANM_articles.txt', 'w') as outfile:
        json.dump(JSONi, outfile)
