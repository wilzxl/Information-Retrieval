import re
import json
from collections import defaultdict
import math
import sys

reload(sys)
import os
import nltk
from nltk.book import *


dirs = os.listdir('cacm/')
dl = defaultdict(int)
index = defaultdict(lambda: defaultdict(int))
query_freq = defaultdict(int)
tf_idf = defaultdict(float)
# normalize = defaultdict(float)
stop_list = []
stop_file = "common_words"
query_file = "cacm.query"
query_dic = defaultdict(list)

# generate stoplist
def stop_words(stop_file):
    with open(stop_file, 'r') as file_object:
        for line in file_object.readlines():
            word = line.strip()
            stop_list.append(word)
    return stop_list


# build inverted index
def build_index_stopping():
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
            new_tokens = filter(lambda x: x not in stop_list and not x.isdigit(), tokens)
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
                        #remove stopwords in query
						if word not in stop_list:
							query_dic[doc_id].append(word.lower())
    return query_dic


def tf_idf_run():
    query_dic = get_query(query_file)
    # calculate query frequency
    query_id = 1
    for num in query_dic.keys():
        # set initial value in case for fi=0
        for f in dirs:
            if f != '.DS_Store':
                doc_id = f.replace('.html', '')
                tf_idf[doc_id]
                # normalize[doc_id]
        for term in query_dic[num]:
            query_freq[term] += 1

        for term in query_freq.keys():
            # calculate number of docs containing i
            df = len(index[term])
            # calculate tf_idf for each doc
            for doc_id, tf in index[term].iteritems():
                # no relevance information
                idf = math.log(N/df)
                #print tf, idf, term, doc_id
                term1 = math.log(tf) + 1
                term2 = term1 * idf
                # term3 = math.pow(term2, 2)
                tf_idf[doc_id] += term2
                # normalize[doc_id] += term3
                #print normalize[doc_id], doc_id

        #normalization
        # for doc_id in tf_idf:
        #     if normalize[doc_id] != 0.0:
        #         tf_idf[doc_id] /= math.sqrt(normalize[doc_id])

        sorted_index_list = sorted(tf_idf.items(), key=lambda x: x[1], reverse=True)
        # print query_dic[str(query_id)]
        # for i in range(100):
        #     print('{0:3}   {1:5}{2:5}{3:5}{4:11f}   {5}'.format(num, "Q0", sorted_index_list[i][0], i+1,
        #                                                         sorted_index_list[i][1], "zhangxl"))
        # print "\n\n"

        #save rank list into file
        file = open('Tf_idf_Stop_SE/' + num + '.txt', 'w')
        for i in range(100):
            if sorted_index_list[i][1] <= 0.0:
                break
            file.write('{0:3}   {1:5}{2:5}{3:5}{4:11f}   {5}'.format(num, "Q0", sorted_index_list[i][0], i+1,
                                                                sorted_index_list[i][1], "Tf_idf_Stop_SE"))
            file.write('\n')
        file.close()

        print query_id
        query_id += 1
        query_freq.clear()
        tf_idf.clear()
        # normalize.clear()


if __name__ == '__main__':
    index, dl = build_index_stopping()
    #	print index
    # total number of docs
    N = len(dl)
    tf_idf_run()