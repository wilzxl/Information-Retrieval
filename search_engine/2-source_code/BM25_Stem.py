import re
import json
from collections import defaultdict
import math

dl=defaultdict(int)
index=defaultdict(lambda:defaultdict(int))
query_freq = defaultdict(int)
bm25 = defaultdict(float)
stop_list=[]
stop_file="common_words"
corpus_file="cacm_stem.txt"

# generate stoplist
def stop_words(stop_file):
	with open(stop_file,'r') as file_object:
		for line in file_object.readlines():
			word=line.strip()
			stop_list.append(word)
	return stop_list

#build inverted index
def build_index():
	pattern=re.compile("^#\\s[0-9]+$")
#	stop_list=stop_words(stop_file)
	with open(corpus_file,'r') as file_object:
		for line in file_object.readlines():
			#find doc_id
			if pattern.match(line):
				doc_id=line.split()[-1]
			else:
				for word in line.split():
					#remove digits
					if not word.isdigit():
						index[word.lower()][doc_id]+=1
						dl[doc_id]+=1
	return index, dl
#	with open('number_of_tokens.txt', 'w') as file_object:
#		file_object.write(json.dumps(dl))

#	with open('index.txt', 'w') as file_object:
#		file_object.write(json.dumps(index))

def bm25_run():	
	with open('cacm_stem.query.txt', 'r') as query_file_obj:
		# calculate query frequency 
		query_id = 1
		for query_line in query_file_obj.readlines():
			query = query_line.split()
			for term in query:
				query_freq[term] += 1
		
			for term in query_freq.keys():
				# calculate number of docs containing i
				ni = len(index[term])
				# calculate BM25 for each doc 
				for doc_id,tf in index[term].iteritems():
					# calculate k
					k = k1*((1-b) + (b* (dl[doc_id] / avdl)))
					# no relevance information
					term1 =  (N - ni + 0.5) / (ni + 0.5)
					term2 =  ((k1 + 1) * tf) / (k + tf)
					term3 =  ((k2 + 1) * query_freq[term]) / (k2 + query_freq[term])
					bm25[doc_id] += math.log(term1)*term2*term3

			sorted_index_list = sorted(bm25.items(), key=lambda x:x[1], reverse=True)
			#print query_id
			print query
			for i in range(100):
				#print sorted_index_list[i][0],
				#print "\t"
				#print sorted_index_list[i][1]
				print('{0:3}   {1:5}{2:5}{3:5}{4:11f}   {5}'.format(query_id, "Q0", sorted_index_list[i][0],i+1, sorted_index_list[i][1], "BM25_Stem_SE"))
			print "\n\n"
			query_id += 1
			query_freq.clear()
			bm25.clear()

if __name__=='__main__':
	index, dl=build_index()
	#total number of docs
	N=len(dl)
	#average length of docs
	avdl = float(sum(x for x in dl.values())) / N
	#initial parameters
	k1 = 1.2 
	k2 = 100.00
	b = 0.75
	bm25_run()