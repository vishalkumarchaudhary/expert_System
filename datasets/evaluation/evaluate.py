import sys
import os,sys,string,re
from math import sqrt,log
import operator
import matplotlib.pyplot as plt
import resource 
import pandas
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from numpy import *

def using(point = ""):
	usage = resource.getrusage(resource.RUSAGE_SELF)
	return '''%s: usertime=%s systime=%s mem=%s mb'''%(point,usage[0],usage[1],(usage[2]*resource.getpagesize())/1000000.0 )

def predictExpert(N):
	#print using('start')
	papers = pandas.read_csv('../papers/training.txt' , header = None).values
	reviewers = pandas.read_csv('../papers/reviewers.txt' , header = None).values
	peshi = pandas.read_csv('../papers/abstracts.txt' , header = None ,delimiter='\n').values
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
	#print using('after knn')
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
	#print using('stop')
	f = open('out.txt', "w")
	for a in arr:
		for b in a:
			f.write(str(b) + ',')
		f.write('\n')
	f.close()

	

_debug=0
_K=5
_R=2
#....................................................
def main():
	Revs=get_revs()
	ofname='paper_reviewer_score.txt'
	ifname='short_listed_papers.txt'
	
	res=open(ofname,'r').read()
	res_list=res.split('\n')

	gfname='gold_standard.txt'
	ih=open(gfname,'r')

	i=-1;N=-1;Prec=0;Chk=0;M=0

	#read gold-standard
	for line in ih:
		i=i+1
		ref_record=line.strip()
		if ref_record != 'UNK':
			N=N+1
			res_record=res_list[N].strip()
			(prec,chk,flag)=process_paper(Revs,ref_record,res_record,i)
			print str(i)+' '+str(N)+' '+str(prec)
			print '........................'
			Prec=Prec+prec
			Chk=Chk+chk
			if flag:
				M=M+1
	ih.close()
	Prec=float(Prec)/float(M)
	Chk=Chk/float(M)
	#print M
	print '\nPrecision: '+str(Prec)+'\n'
	#print Chk
	return(Prec)

#....................................................
def process_paper(Revs,ref_record,res_record,pap_id):
	ref_parts=ref_record.split(',')
	ref={}
	flag=False
	for part in ref_parts:
		part=part.strip()
		if part != '':
			(rev,score)=part.split(':')
			ref[rev]=int(score)
			if ref[rev]>=_R:
				flag=True

	res_parts=res_record.split(',')
	res={}
	for part in res_parts:
		part=part.strip()
		if part != '':
			(rev,score)=part.split(':')
			if rev.find('_')==-1:
				revs=rev.split()
				revname=revs[0]+'_'+revs[1]
			else:
				revname=rev
			if revname in Revs:
				res[revname]=float(score)
	(prec,chk)=compute_prec(ref,res,pap_id)
	return(prec,chk,flag)


#....................................................
def compute_prec(ref,res,pap_id):	
      	sorted_revs = sorted(res.items(), key=operator.itemgetter(1), reverse=True)
	prec=0;drec='';flag=False
      	for i in range(_K):
		record=sorted_revs[i]
              	(name,score)=record
		drec=drec+name+':'+str(score)+','
		if name in ref:
			if ref[name]>=_R:
				prec=prec+1
				flag=True

	chk=0
	for rev in ref:
		if ref[rev]>=_R:
			chk=chk+1
	if chk>_K:
		chk=_K
	chk=chk/float(_K)
	prec=prec/float(_K)

	return(prec,chk)		
	
		
#....................................................
def get_revs():
	ifname='short_listed_revs.txt'
	shlst_revs=open(ifname,'r').read().strip().split('\n')
	return(shlst_revs)

#....................................................
def create_shlst_revs():
	gfname='gold_standard.txt'
	ofname='short_listed_revs.txt'
	ih=open(gfname,'r')
	oh=open(ofname,'w')
	Revs=[]
	for line in ih:
		line=line.strip()
		if line!='UNK':
			parts=line.split(',')
			for part in parts:
				part=part.strip()
				if part != '':
					#print part;#debug()
					(rev,score)=part.split(':')
					oh.write(rev+'\n')
					Revs.append(rev) 
	ih.close()
	oh.close()
	return(Revs)

#....................................................
def debug():
	stop_str=raw_input("Press q to quit.")
    	if stop_str is 'q':
        	sys.exit(1)
#....................................................
if __name__=='__main__':
	c=[]
	b=[]
	for i in [158]:
		print i
		predictExpert(i)
		a=[0,1,2,3,4,5,10,11,13,14,16,17,18,22,26,29,34,35,36,40,45,52,56,63,79,83,88,93,103,128,139,144,145,147]
		f=open ('paper_reviewer_score.txt','w')
		with open("out.txt") as fp:
		    for i, line in enumerate(fp):
		        if i in a:
		            f.write(line)
		f.close()
		b.append(i)
		c.append(main())