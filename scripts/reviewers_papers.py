import pandas
from numpy import *

papers = pandas.read_csv('../datasets/papers/training.txt' , header = None)
reviewers = pandas.read_csv('../datasets/papers/reviewers.txt' , header = None)

reviewers = reviewers.values

keys = reviewers[:,1]
vals = reviewers[:,0]
author_map = dict(zip(keys,vals))

papers = papers.values

authorid = []
for i in range(papers.shape[0]):
	authorid = authorid + [author_map[papers[i][0]]]

papers = papers[:,1]

for i in set(authorid):
	p[i] = i == 