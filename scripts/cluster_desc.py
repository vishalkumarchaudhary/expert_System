from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

with open ('jobDescriptions.txt') as f:
	content = f.readlines()

vectorizer = TfidfVectorizer(max_df=.5, max_features=310 ,min_df=10 ,
										stop_words='english',use_idf=True)				

dat = vectorizer.fit_transform(content)
dat = dat.toarray()

f = open ('dump.txt', 'w')
f.write (dat)

km = KMeans(n_clusters=100)
km.fit(dat)
