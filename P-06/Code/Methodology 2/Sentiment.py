import sqlite3
import nltk
import re
from nltk.tokenize import WordPunctTokenizer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score

conn=sqlite3.connect('knowledgeBase.db')
c=conn.cursor()

negativeWords = []
positiveWords = []

sql = "SELECT * FROM wordVals WHERE value =?"

def loadWordArrays():
    for negRow in c.execute(sql, [(-1)]):
        negativeWords.append(negRow[0])
    print 'neg words loaded'

    for posRow in c.execute(sql, [(1)]):
        positiveWords.append(posRow[0])
    print 'pos words loaded'


def testSentiment():
    predSentiment = []
    stopset = set(stopwords.words('english'))
    readFile = pd.read_csv('Reviews.csv')
    readFile = readFile.replace([np.inf,-np.inf],np.nan)
    readFile = readFile.fillna('')
    reviews = readFile['Review']
    print 'Number of Reviews: ' + str(len(reviews))
    
    for review in reviews:
        sentimentCounter = 0
        token =  nltk.word_tokenize(review)
        tagged = nltk.pos_tag(token)
        
        
        adj = re.findall(r'\(\'(\w*)\',\s\'JJ\w?\'',str(tagged))
        verb = re.findall(r'\(\'(\w*)\',\s\'VBZ\'',str(tagged))
        adverb = re.findall(r'\(\'(\w*)\',\s\'RB\w?\'',str(tagged))
        finalString = adj + verb + adverb
       
        fstring = ''
        for word in finalString:
            if word not in stopset:         
                fstring = fstring + word + ' '
      
        
        for eachPosWord in positiveWords:
            if eachPosWord in fstring:
                sentimentCounter += .52
    
        for eachNegWord in negativeWords:
            if eachNegWord in fstring:
                sentimentCounter -= 1.7
    
        if sentimentCounter > 0:
            predSentiment.append('positive')
    
        if sentimentCounter ==0:
            predSentiment.append('neutral')
    
        if sentimentCounter < 0:
            predSentiment.append('negative')
    

    print 'Accuracy: ' + str(accuracy_score(readFile['Sentiment'],predSentiment))
    

loadWordArrays()
testSentiment()
