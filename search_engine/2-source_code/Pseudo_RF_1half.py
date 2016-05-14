import re
import json
from collections import defaultdict
import math
import sys
# import numpy as np
import time
reload(sys)
import os
import nltk

dirs = os.listdir('cacm/')
dl = defaultdict(int)
index = defaultdict(lambda: defaultdict(int))
query_freq = defaultdict(int)
bm25 = defaultdict(float)
stop_list = []
stop_file = "common_words"
corpus_file = "cacm_stem.txt"
query_file = "cacm.query"
query_dic = defaultdict(list)


# generate stoplist
def stop_words(stop_file):
    with open(stop_file, 'r') as file_object:
        for line in file_object.readlines():
            word = line.strip()
            stop_list.append(word)
    return stop_list


# build inverted index without stopwords
def build_index_stopping():
    print 'buliding index...'
    doc_count = 0
    stop_list = stop_words(stop_file)
    pattern1 = re.compile('[!"#$%&\'()*+,\/:;.=?@[\\]^_`{|}~]+')
    pattern2 = re.compile('<\\w+>')
    for f in dirs:
        if f != '.DS_Store':
            doc_id = f.replace('.html', '')
            text_object = open('cacm/' + f, 'r')
            text = re.sub(pattern1, '', text_object.read().lower())
            text = re.sub(pattern2, '', text)

            # print doc_count
            tokens = nltk.word_tokenize(text)
            new_tokens = filter(lambda x: x not in stop_list and not x.isdigit(), tokens)
            dl[doc_id] = len(new_tokens)
            fredist = nltk.FreqDist(new_tokens)
            for localkey in fredist.keys():
                index[localkey][doc_id] = fredist[localkey]
            doc_count += 1
            text_object.close()
    print 'build index done.'
    return index, dl


def get_query(query_file):
    print 'getting query....'
    with open(query_file, 'r') as query_file_obj:
        # remove punctuation and </DOC>
        pattern1 = re.compile('[!"#$%&\'()*+,\/:;.=?@[\\]^_`{|}~]+')
        # find query ID
        pattern2 = re.compile(r'<\w+> [0-9]+')
        # remove <DOC>
        pattern3 = re.compile(r'<\w{3}>')

        for line in query_file_obj.readlines():
            line = re.sub(pattern3, '', line)
            # find query_ID
            if pattern2.match(line):
                doc_id = line.split()[1]
            else:
                line = re.sub(pattern1, '', line)
                # select lines excluding <DOC>
                if not pattern3.match(line):
                    for word in line.split():
                        query_dic[doc_id].append(word.lower())
    print 'all queries get.'
    return query_dic


def bm25_return(k1=1.2, k2=100.00, b=0.75):
    # dictionary for original bm25
    oriRank = {}
    index, dl = build_index_stopping()
    N = len(dl)
    # average length of docs
    avdl = float(sum(x for x in dl.values())) / N
    query_dic = get_query(query_file)
    # calculate query frequency
    query_id = 1
    for num in query_dic.keys():
        oriRank[num] = {}
        # set initial value in case for fi=0
        for f in dirs:
            if f != '.DS_Store':
                doc_id = f.replace('.html', '')
                bm25[doc_id]
        for term in query_dic[num]:
            query_freq[term] += 1

        for term in query_freq.keys():
            # calculate number of docs containing i
            ni = len(index[term])
            # calculate BM25 for each doc
            for doc_id, tf in index[term].iteritems():
                # calculate k
                k = k1 * ((1 - b) + (b * (dl[doc_id] / avdl)))
                # no relevance information
                term1 = (N - ni + 0.5) / (ni + 0.5)
                term2 = ((k1 + 1) * tf) / (k + tf)
                term3 = ((k2 + 1) * query_freq[term]) / (k2 + query_freq[term])
                bm25[doc_id] += math.log(term1) * term2 * term3

        sorted_index_list = sorted(bm25.items(), key=lambda x: x[1], reverse=True)
        for i in range(100):
            oriRank[num][sorted_index_list[i][0]] = 0.0
            oriRank[num][sorted_index_list[i][0]] = sorted_index_list[i][1]
        query_id += 1
        query_freq.clear()
        bm25.clear()
    return oriRank, index, dl, query_dic


# class Pseudo:
#     def __init__(self):
#         self = self
#
#     def Pseudo_relFb(self, oriRank):
#         # print query_dic
#         print '-' * 80
# 		print oriRank
#

def pseudo_relFb(alpha = 8.0, beta = 16.0, gamma = 4.0):
    oriRank, index, dl, query_dic = bm25_return()
    docs = []
    for item in dirs:
        if item != '.DS_Store':
            doc_id = item.replace('.html', '')
        docs.append(doc_id)
    # print docs
    REL = 100.0
    NonREL = len(docs)-100.0
    # print index

    vocabulary = {}
    modified_query = {}
    for item in index:
        vocabulary[item] = [0.0,0.0,0.0]
        # print vocabulary[item][0]
    for num in query_dic:
        modified_query[num] = {}
        for term in vocabulary:
            vocabulary[term] = [0.0,0.0,0.0]
            modified_query[num][term] = 0.0
        query = query_dic[num]
        for item in index:
            if term in query:
                vocabulary[term][0] = 1.0
        for reldoc in oriRank[num]:
            for term in index:
                if reldoc in index[term]:
                    vocabulary[term][1] += 1.0
        for nonreldoc in docs:
            if nonreldoc not in oriRank[num]:
                for term in index:
                    if nonreldoc in index[term]:
                        vocabulary[term][2] += 1.0
        for term in vocabulary:
            weight = alpha*vocabulary[term][0] + (1.0/REL)*vocabulary[term][1] + (1.0/NonREL)*vocabulary[term][2]
            modified_query[num][term] += weight
            if weight > 0.0:
                print 'a weight found'
        print num
    fileObj = open('Pesudo_modified_weight.txt', 'w')
    for num in modified_query:
        fileObj.write('~~query_index ' + num + '\n')
        for term in modified_query[num]:
            fileObj.write(term + '|' + str(modified_query[num][term])+' ')
        fileObj.write('\n')
    fileObj.close()



    # for item in oriRank:
    #     print '-'*80
    #     print query_dic[item]
    #     # print item, len(oriRank[item])/2
    #     print oriRank[item]
    # print '-'*80



if __name__ == '__main__':
    start = time.time()
    # pse = Pseudo()
    # orirank = bm25_return()
    # pse.Pseudo_relFb(orirank)
    pseudo_relFb()
    end = time.time()
    print '-'* 80
    print 'total run time is:', end-start,'s'
