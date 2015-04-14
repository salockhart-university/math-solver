import pandas as pd
from sklearn import ensemble
from sklearn.metrics import accuracy_score
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn import tree
from sklearn import neighbors
from sklearn.metrics import precision_recall_fscore_support

#Load extracted features
train = pd.read_csv('extracted_features.csv').drop(['review/text','review/summary','product/productId','Unnamed: 0'],axis=1)
target = pd.read_csv('data.csv')

#Load target label
train['score'] = target['review/score']
print train
print train.shape

#Deal with infinite values
train = train.replace([np.inf,-np.inf],np.nan)
train = train.fillna(0)
print train.shape


#Differntiate training and validation set
valid = train.ix[:int(len(train)/3),:]
train = train.ix[set(train.index)-set(valid.index),:]
print 'Size of training set %i' % len(train)
print 'Size of validation set %i' % len(valid)

#Set up GradientBoostingClassifier
#clf = ensemble.GradientBoostingClassifier(n_estimators = 400)

#set up Gaussian Navie bayes
#clf = GaussianNB()

#set up decision tree
clf = tree.DecisionTreeClassifier()

print 'Start Training'

clf.fit(train.drop(['score'],axis=1),train['score'])

#Prediction on validation set
predict = clf.predict(valid.drop(['score'],axis=1))

#Compute accuracy
print accuracy_score(valid['score'],predict)

#precision recall fscore
print precision_recall_fscore_support(valid['score'], predict, average='macro')
