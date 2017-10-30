import pandas
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import numpy as np 
from numpy import *

papers = pandas.read_csv('../datasets/papers/training.txt' , header = None)
reviewers = pandas.read_csv('../datasets/papers/reviewers.txt' , header = None)

peshi = pandas.read_csv('../datasets/papers/abstracts.txt' , header = None ,delimiter='\n')


reviewers = reviewers.values

keys = reviewers[:,1]
vals = reviewers[:,0]
author_map = dict(zip(keys,vals))


papers = papers.values

authorid = []
for i in range(papers.shape[0]):
	authorid = authorid + [author_map[papers[i][0]]]


peshi = peshi.values

papers =  np.concatenate((papers[:,1] , peshi[:,0]) )


vectorizer = TfidfVectorizer( decode_error  = 'ignore')
tfidf = vectorizer.fit_transform(papers) 

clasifier = RandomForestClassifier(n_estimators=20, criterion='gini');
classifier = clasifier.fit(tfidf[:len(authorid)], authorid);

labels = clasifier.predict(tfidf[len(authorid):])

centroid = []
print(tfidf[0].shape)
initial_val = []
for i in range(tfidf[0].shape[1]):
	initial_val.append(0)

num_papers = []
for i in keys:
	centroid.append(initial_val)
	num_papers.append(0.0)

for i in range(len(labels)):
	centroid[labels[i]] = tfidf[len(authorid) + i] + centroid[labels[i]]
	num_papers[labels[i]] = num_papers[labels[i]] + 1;
print centroid[1]
print centroid[2]

j = 1
for i in keys:
	centroid[j] = map(lambda x: x/num_papers[j], centroid[j])
	j = j + 1





