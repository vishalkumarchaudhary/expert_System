import pandas
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from numpy import *
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from matplotlib import pyplot

papers = pandas.read_csv('../datasets/papers/training.txt' , header = None).values
reviewers = pandas.read_csv('../datasets/papers/reviewers.txt' , header = None).values
peshi = pandas.read_csv('../datasets/papers/abstracts.txt' , header = None ,delimiter='\n').values

#print papers
#print reviewers.shape

keys = reviewers[:,1]
vals = reviewers[:,0]
author_map = dict(zip(keys,vals))
author_map_ = dict(zip(vals,keys))
authorid = []
for i in range(papers.shape[0]):
	authorid = authorid + [author_map[papers[i][0]]]

tmp = hstack((papers[:,1],peshi[:,0]))

v_papers = TfidfVectorizer(decode_error='ignore', max_features=75, max_df=.5 ,min_df=0.001).fit_transform(tmp).toarray()

#print(v_papers[:,len(authorid)].shape)

classifier = KNeighborsClassifier(n_neighbors=5)

classifier.fit(v_papers[:len(authorid),] , authorid )

(neig , ind )= classifier.kneighbors(v_papers[len(authorid):,],100)
print len(vals)
arr=[]
for i in ind :
	tmp = []
	tmp_ = []
	_tmp = []
	for j in i:
		tmp.append(authorid[j])


	for j in range(len(vals)):
		tmp_.append(tmp.count(j))
	tmp_ = array(tmp_)

	for j in range(5):
		_tmp.append(author_map_[ argmax(tmp_)])
		tmp_[argmax(tmp_)] = -1
	arr.append(_tmp)

print(arr)