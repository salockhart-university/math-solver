import pandas as pd
import nltk
from sklearn import preprocessing
from sklearn import feature_extraction
from sklearn import ensemble
from nltk.tokenize import WordPunctTokenizer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords


#Read data into pandas dataframe
train = pd.read_csv('data.csv')
#Remove unnecessary columns 
target = train['review/score']
train = train.drop(['product/price', 'review/profileName','review/userId','product/title','review/helpfulness','review/score'],axis=1)
print train

def noWords(text): #Find no of words in text
    return len(nltk.word_tokenize(text.decode('utf-8')))

def noLines(text): #Find no of line in text
    return text.count('\n')



#Set up tokenizer and stemmer
tokenizer = WordPunctTokenizer()
stemmer = PorterStemmer()

#Find no of words, no of lines in review text
train['review/summary'] = train['review/summary'].fillna("")
train['summary length'] = train['review/summary'].apply(len)
train['summary no of words'] = train['review/summary'].apply(noWords)

train['review/text'] = train['review/text'].fillna(" ")
train['review length'] = train['review/text'].apply(len)
train['review no of words'] = train['review/text'].apply(noWords)
train['review no of lines'] = train['review/text'].apply(noLines)

print 'Start Stemming and stopword removal'

#Tokenize, Stem and remove stop words
stopset = set(stopwords.words('english'))
stemReviews = []
for i in range(len(train)):
    stemReviews.append(
    [stemmer.stem(word.decode('latin_1')) for word in [w for w in
            tokenizer.tokenize(train.ix[i,'review/text'].lower())
                if (w not in stopset)]
     ]
    )


stemSummary = []
for i in range(len(train)):
    stemSummary.append(
    [stemmer.stem(word.decode('latin_1')) for word in [w for w in
            tokenizer.tokenize(train.ix[i,'review/summary'].lower())
                if (w not in stopset)]
     ]   
    )

train['review/text'] =  stemReviews
train['review/summary'] = stemSummary
train['stem review len'] = train['review/text'].apply(len)
train['stem summary len'] = train['review/summary'].apply(len)
train['review/text'] = [' '.join(w) for w in train['review/text']]
train['review/summary'] = [' '.join(w) for w in train['review/summary']]
train['ratio of stem and original length review'] = train['review length']/train['stem review len']
train['ratio of stem and original length summary'] = train['summary length']/train['stem summary len']

print 'Preprocessing complete!'
train.to_csv('extracted_features.csv')
