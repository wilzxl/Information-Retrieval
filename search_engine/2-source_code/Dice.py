import re
from collections import defaultdict
import math
import sys
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


def query_exepend():
    query_dic = get_query(query_file)
    stoped_query = []
    stop_list = stop_words(stop_file)
    for item in query_dic:
        query1 = []
        for term in query_dic[item]:
            if term not in stop_list:
                query1.append(term)
            else:
                continue
        stoped_query.append(query1)
        # print query1

    all_terms = []
    for row in stoped_query:
        for col in row:
            all_terms.append(col)
    unique_query_terms = set(all_terms)
    # print all_terms
    print unique_query_terms
    index, dl = build_index_stopping()

    diceVal = {}
    query_expansion = {}
    for term in index:
        diceVal[term] = 0.0
    for query_term in unique_query_terms:
        docs1 = index[query_term]
        na = len(docs1.keys())
        # print docs1.keys()
        print 'na=',na
        for term in index:
            nab = 0.0
            nb = len(index[term].keys())
            for key in index[term].keys():
                if key in docs1.keys():
                  nab += 1
            if na + nb != 0:
                diceofterm = nab/(na + nb)
            else:
                diceofterm = 0
            diceVal[term] = diceofterm
            # print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$    ',term, nab
        sorted_dice = sorted(diceVal.items(), key=lambda x:x[1], reverse=True)
        docs2 = []
        i = 0
        while i < 3:
            key, val = sorted_dice[i]
            # if key == query_term:
            #     continue
            if key not in stop_list:
                docs2.append(key)
                i += 1
            else:
                continue
        query_expansion[query_term] = []
        query_expansion[query_term].extend(docs2)
    # print query_expansion
    return query_expansion, index, dl


def bm25_expand(k1=1.2, k2=100.00, b=0.75):
    # query_dic = get_query(query_file)
    query_expansion, index, dl = query_exepend()
    print '-'*30 + ' bm25 starts ' + '-'*30
    expanded_queries = {}
    for num in query_dic.keys():
        expanded_queries[num] = []
        for term in query_dic[num]:
            if term not in stop_list:
                morequery = query_expansion[term]
                # morequery.append(item)
                expanded_queries[num].extend(morequery)
    print expanded_queries
    N = len(dl)
    # average length of docs
    avdl = float(sum(x for x in dl.values())) / N

    # calculate query frequency
    query_id = 1
    for num in expanded_queries.keys():
        # set initial value in case for fi=0
        for f in dirs:
            if f != '.DS_Store':
                doc_id = f.replace('.html', '')
                bm25[doc_id]
        for term in expanded_queries[num]:
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
        print query_dic[num]
        filename = 'BM25_QE_Dices_SE/' + num + '.txt'
        fileObj = open(filename, 'w')
        for i in range(100):
            fileObj.write('{0:3}   {1:5}{2:5}{3:5}{4:11f}   {5}'.format(num, "Q0", sorted_index_list[i][0],i+1, sorted_index_list[i][1], "BM25_QE_Dices_SE"))
			# print('{0:3}   {1:5}{2:5}{3:5}{4:11f}   {5}'.format(num, "Q0", sorted_index_list[i][0],i, sorted_index_list[i][1], "Dice"))
        #  print('{0:3}   {1:5}{2:5}{3:5}{4:11f}   {5}'.format(num, "Q0", sorted_index_list[i][0],i, sorted_index_list[i][1], "Dice"))
            fileObj.write('\n')
        print "\n\n"
        fileObj.close()
        query_id += 1
        query_freq.clear()
        bm25.clear()


if __name__ == '__main__':
    start = time.time()
    bm25_expand()
    end = time.time()
    print '-' * 80
    print 'total run time is', end - start, 's'
