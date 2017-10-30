import pandas
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from numpy import *
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from matplotlib import pyplot

papers = pandas.read_csv('../datasets/papers/training.txt' , header = None).values
reviewers = pandas.read_csv('../datasets/papers/reviewers.txt' , header = None).values

print papers
print reviewers.shape

v_papers = TfidfVectorizer(decode_error='ignore', max_features=100).fit_transform(papers[:,1]).toarray()
for rev in reviewers[:,1]:
	x = v_papers[v_papers[:,0]==rev]
	print x