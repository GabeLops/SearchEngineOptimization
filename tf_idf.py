def computeTF(wordDict):
  tfDict = {}
  bowCount = sum(wordDict.values())
  for word, count in wordDict.items():
    tfDict[word] = count/float(bowCount)
  return tfDict

def computeIDF(docList):
  import math
  idfDict = {}
  N = len(docList)
  first_doc_counts = list(docList[0].values())[0]
  idfDict = dict.fromkeys(first_doc_counts.keys(), 0)
  for doc in docList:
    doc_counts = list(doc.values())[0]
    for word, val in doc_counts.items():
      if val > 0:
        if word in idfDict:
          idfDict[word] += 1
        else:
          idfDict[word] = 1
  
  for word, val in idfDict.items():
    idfDict[word] = math.log10(N/float(val))
  
  return idfDict

def computeTFIDF(tfBow, idfs, counts):
  tfidf = {}
  for word, val in tfBow.items():
    tfidf[word] = {'count': counts[word], 'tf_idf':val*idfs[word]}
  return tfidf
