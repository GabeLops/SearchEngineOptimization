import nltk
from bs4 import BeautifulSoup
from html2text import html2text 
import re
from collections import Counter
from nltk.tokenize import RegexpTokenizer
from tf_idf import computeIDF, computeTF, computeTFIDF
from db import insert_indices

doc_list_tfidf = []
combined_tokens = Counter([])
tokens_by_doc = {}
doc_list = []

import glob, os
cwd = os.getcwd()
files = cwd + '/webpages_raw/**'


def clean_html(html):
    """
    Copied from NLTK package.
    Remove HTML markup from the given string.

    :param html: the HTML string to be cleaned
    :type html: str
    :rtype: str
    """

    # First we remove inline JavaScript/CSS:
    cleaned = re.sub(r"(?is)<(script|style).*?>.*?(</\1>)", "", html.strip())
    # Then we remove html comments. This has to be done before removing regular
    # tags since comments can contain '>' characters.
    cleaned = re.sub(r"(?s)<!--(.*?)-->[\n]?", "", cleaned)
    # Next we can remove the remaining tags:
    cleaned = re.sub(r"(?s)<.*?>", " ", cleaned)
    # Finally, we deal with whitespace
    cleaned = re.sub(r"&nbsp;", " ", cleaned)
    cleaned = re.sub(r"  ", " ", cleaned)
    cleaned = re.sub(r"  ", " ", cleaned)
    return cleaned.strip()

# Should we need to use Python 3.4 and below
def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z

# samples = ['0/8', '1/8']
# for sample in samples:
#   filename = 'webpages_raw/' + sample
#   current_file = re.sub(cwd + '/webpages_raw/', '', filename)
#   if os.path.isfile(filename): # filter dirs
#     print(filename)
#     html = open(filename, 'r').read()
#     soup = BeautifulSoup(html, 'lxml')
#     cleanhtml = clean_html(html)
#     text = html2text(cleanhtml)
#     tokenizer = RegexpTokenizer(r'\w+')
#     tokens = tokenizer.tokenize(text)
#     counts = Counter(tokens)
#     tokens_by_doc[current_file] = dict(counts)
#     combined_tokens = combined_tokens + counts
#     doc_list.append(text)

for filename in glob.iglob(files, recursive=True):
  current_file = re.sub(cwd + '/webpages_raw/', '', filename)
  if os.path.isfile(filename): # filter dirs
    print(current_file)
    html = open(filename, 'r').read()
    soup = BeautifulSoup(html, 'lxml')
    cleanhtml = clean_html(html)
    text = html2text(cleanhtml)
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)
    counts = Counter(tokens)
    # tokens_by_doc[current_file] = dict(counts)
    # combined_tokens = combined_tokens + counts
    doc_list.append({current_file: dict(counts)})

# combined_tokens = dict(combined_tokens)

idf = computeIDF(doc_list)
for document in doc_list:
  document_id = list(document.keys())[0]
  document = list(document.values())[0]
  tf = computeTF(document)
  tfidf = computeTFIDF(tf, idf, document)
  doc_list_tfidf.append({document_id: tfidf})

insert_indices(doc_list_tfidf)

8845891