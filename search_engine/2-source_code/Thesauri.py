import re
import json
from collections import defaultdict
import math
import sys

import operator

reload(sys)
import os
import nltk
from nltk.book import *
from nltk.corpus import wordnet as wn

dirs = os.listdir('cacm/')
dl = defaultdict(int)
index = defaultdict(lambda: defaultdict(int))
query_freq = defaultdict(int)
bm25 = defaultdict(float)
stop_list = []
stop_file = "common_words"
#corpus_file = "cacm_stem.txt"
query_file = "cacm.query"
query_dic = defaultdict(list)
syn_dic = defaultdict(float)


# generate stoplist
def stop_words(stop_file):
    with open(stop_file, 'r') as file_object:
        for line in file_object.readlines():
            word = line.strip()
            stop_list.append(word)
    return stop_list


# build inverted index
def build_index():
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
            #			print text
            print doc_count
            tokens = nltk.word_tokenize(text)
            new_tokens = filter(lambda x: not x.isdigit(), tokens)
            dl[doc_id] = len(new_tokens)
            fredist = nltk.FreqDist(new_tokens)
            for localkey in fredist.keys():
                index[localkey][doc_id] = fredist[localkey]
            doc_count += 1
            text_object.close()
        #			print new_tokens
    return index, dl


def get_query(query_file):
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
    return query_dic

def bm25_run():
    query_dic = get_query(query_file)
    # calculate query frequency
    query_id = 1
    for num in query_dic.keys():
        # set initial value in case for fi=0
        for f in dirs:
            if f != '.DS_Store':
                doc_id = f.replace('.html', '')
                bm25[doc_id]
        for term in query_dic[num]:
            query_freq[term] += 1

        # calculate BM25 for each doc
        for doc_id in bm25.keys():
            for term in query_freq.keys():
                syn = []
                #print term, num, query_id
                if term in stop_list:
                    bm25[doc_id] += calculation(doc_id, term, term)
                    #print bm25[doc_id], term
                else:
                    if wn.synsets(term) != []:
                        syn = wn.synsets(term)[0].lemma_names()
                        #print syn
                        for i in range(len(syn)):
                            syn_dic[syn[i]] = calculation(doc_id, syn[i], term)
                            if i == 3:
                                break
                        #print syn_dic
                        score = wight * max(syn_dic.iteritems(), key = operator.itemgetter(1))[1]
                    else:
                        score = 0
                    #print calculation('CACM-1519', term), doc_id, term
                    bm25[doc_id] += max(score, calculation(doc_id, term, term))
                    syn_dic.clear()

        sorted_index_list = sorted(bm25.items(), key=lambda x: x[1], reverse=True)


        #save rank list into file
        file = open('BM25_QE_Thesauri_SE/' + num + '.txt', 'w')
        for i in range(100):
            if sorted_index_list[i][1] <= 0.0:
                break
            file.write('{0:3}   {1:5}{2:5}{3:5}{4:11f}   {5}'.format(num, "Q0", sorted_index_list[i][0], i+1,
                                                                sorted_index_list[i][1], "BM25_QE_Thesauri_SE"))
            file.write('\n')
        file.close()

        print query_id
        query_id += 1
        query_freq.clear()
        bm25.clear()
    file.close

def calculation(doc_id, syn_term, org_term):
    tf = index[syn_term][doc_id]
    if tf == 0:
        del index[syn_term][doc_id]
    # calculate number of docs containing i
    ni = len(index[syn_term])
    #print tf
    # calculate k
    k = k1 * ((1 - b) + (b * (dl[doc_id] / avdl)))
    # no relevance information
    term1 = (N - ni + 0.5) / (ni + 0.5)
    term2 = ((k1 + 1) * tf) / (k + tf)
    term3 = ((k2 + 1) * query_freq[org_term]) / (k2 + query_freq[org_term])
    score = math.log(term1) * term2 * term3
    #print term1, term2, term3
    return score


if __name__ == '__main__':
    print wn.lemmas('car')
    index, dl = build_index()
    #	print index
    # total number of docs
    N = len(dl)
    # average length of docs
    avdl = float(sum(x for x in dl.values())) / N
    # initial parameters
    k1 = 1.2
    k2 = 100.00
    b = 0.75
    wight = 0.7
    bm25_run()
