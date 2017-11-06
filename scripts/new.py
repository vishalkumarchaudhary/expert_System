import pandas
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from numpy import *
papers = pandas.read_csv('../datasets/papers/training.txt' , header = None).values
reviewers = pandas.read_csv('../datasets/papers/reviewers.txt' , header = None).values
peshi = pandas.read_csv('../datasets/papers/abstracts.txt' , header = None ,delimiter='\n').values
keys = reviewers[:,1]
vals = reviewers[:,0]
author_map = dict(zip(keys,vals))
author_map_ = dict(zip(vals,keys))
authorid = []
for i in range(papers.shape[0]):
	authorid = authorid + [author_map[papers[i][0]]]
tmp = hstack((papers[:,1],peshi[:,0]))
v_papers = TfidfVectorizer(decode_error='ignore', max_features=75, max_df=.8 ,min_df=0.001).fit_transform(tmp).toarray()
ind = KNeighborsClassifier(n_neighbors=5).fit(v_papers[:len(authorid),], authorid).kneighbors(v_papers[len(authorid):,],50)[1]
arr=[]
for i in ind :
	tmp = []
	tmp_ = []
	_tmp = []
	for j in i:
		tmp.append(authorid[j])
	for j in range(len(vals)):
		tmp_.append(tmp.count(j))
	for j in range(10):
		_tmp.append(author_map_[ argmax(tmp_)])
		tmp_[argmax(tmp_)] = -1
	arr.append(_tmp)
f = open('out.txt', "w")
for a in arr:
	f.write(str(a)[1:-1]+'\n')
f.close()