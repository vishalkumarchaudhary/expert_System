import resource 
import pandas
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from numpy import *

def using(point = ""):
	usage = resource.getrusage(resource.RUSAGE_SELF)
	return '''%s: usertime=%s systime=%s mem=%s mb'''%(point,usage[0],usage[1],(usage[2]*resource.getpagesize())/1000000.0 )

def predictExpert(N):
	print using('start')
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
	ind = KNeighborsClassifier(n_neighbors=5).fit(v_papers[:len(authorid),], authorid).kneighbors(v_papers[len(authorid):,],N)[1]
	print using('after knn')
	arr=[]
	for i in ind :
		tmp = []
		tmp_ = []
		_tmp = []
		for j in i:
			tmp.append(authorid[j])
		for j in range(1,len(vals)):
			tmp_.append(str(author_map_[j]+':'+str(tmp.count(j))))
		arr.append(tmp_)
	print using('stop')
	f = open('out.txt', "w")
	for a in arr:
		for b in a:
			f.write(str(b) + ',')
		f.write('\n')
	f.close()

predictExpert(100)
a=[0,1,2,3,4,5,10,11,13,14,16,17,18,22,26,29,34,35,36,40,45,52,56,63,79,83,88,93,103,128,139,144,145,147]
f=open ('paper_reviewer_score.txt','w')
with open("out.txt") as fp:
	for i, line in enumerate(fp):
		if i in a:
			f.write(line)