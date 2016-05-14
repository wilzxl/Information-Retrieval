import os
import re
from collections import defaultdict
import time


dirs=os.listdir('cacm/')
dl=defaultdict(int)
index=defaultdict(lambda:defaultdict(int))
query_freq = defaultdict(int)
bm25 = defaultdict(float)
stop_list=[]
stop_file="common_words"
corpus_file="cacm_stem.txt"
query_file="cacm.query"
query_dic=defaultdict(list)


def stop_words(stop_file):
	with open(stop_file,'r') as file_object:
		for line in file_object.readlines():
			word=line.strip()
			stop_list.append(word)
	return stop_list


def get_query(query_file):
	with open(query_file, 'r') as query_file_obj:
		#remove punctuation and </DOC>
		pattern1=re.compile('[!"#$%&\'()*+,\/:;.=?@[\\]^_`{|}~]+')
		#find query ID
		pattern2=re.compile(r'<\w+> [0-9]+')
		#remove <DOC>
		pattern3=re.compile(r'<\w{3}>')

		for line in query_file_obj.readlines():
			line=re.sub(pattern3,'',line)
			#find query_ID
			if pattern2.match(line):
				doc_id=line.split()[1]
			else:
				line=re.sub(pattern1,'',line)
				#select lines excluding <DOC>
				if not pattern3.match(line):
					for word in line.split():
						query_dic[doc_id].append(word.lower())
	return query_dic


def read_Query(folder):
    print 'reading query...'
    Allfile = {}
    Topfile = {}
    for num in range(64):
        # print folder
        # print '---------------', num+1, '------------------'
        Topfile[num+1] = {}
        filename = folder + '/' + str(num+1) + '.txt'
        fileObj = open(filename, 'r')
        content = fileObj.readlines()
        fileObj.close()
        body = {}
        for i in range(len(content)):
            token = map(str, content[i].split(" "))
            token = [x for x in token if x != '']
            body[int(token[3])] = token[2]
        # sorted_body = sorted(body.items(), key=lambda x: x[1], reverse=False)
        Topfile[num+1] = body
    # print Topfile

    for num in Topfile:
        Allfile[num] = {}
        for rank in Topfile[num]:
            doc = Topfile[num][rank]
            Allfile[num][doc] = []
            filename = 'cacm/' + doc + '.html'
            try:
                fileObj = open(filename, 'r')
            except:
                continue
            content = fileObj.readlines()
            fileObj.close()
            body = []
            buffer = 0
            for row in range(len(content)):
                # print content[row]
                if row < 4:
                    continue
                elif len(content[row]) > 10:
                    if content[row][:2] == 'CA' and content[row][3].isdigit() and content[row][4].isdigit():
                        break;

                    # if content[row][9] == 'J' and content[row][10] == 'B' \
                    #         or content[row][9] == 'D' and content[row][10] == 'H' \
                    #         or content[row][9] == 'D' and content[row][10] == 'B':
                    #     break

                    # buffer += 1
                    # if buffer >= 4:
                    #     buffer = 0
                    #     break
                    # else:
                    #     body.append(content[row])
                    else:
                        body.append(content[row])
            Allfile[num][doc] = body
    # print Allfile
    print 'read query done.'
    return Allfile, Topfile


def snippet(sourcefolder):
    print 'creating snippet...'
    # BOLD = '\033[1m'
    # END = '\033[0m'
    queries = get_query(query_file)
    stop_list = stop_words(stop_file)

    outfolder = sourcefolder + '_Snippet'
    allcontent, topfile = read_Query(sourcefolder)
    if not os.path.exists(outfolder):
        os.mkdir(outfolder)
    for num in topfile:
        print 'procesing query: ', str(num)
        fileObj = open(outfolder + '/' + str(num) + '_snippet.html', 'w')
        for rank in topfile[num]:
            doc = topfile[num][rank]
            fileObj.write('-'*40 + ' QueryId: ' + str(num) + '   Document: ' + doc + '   Rank: '+str(rank) +'\n')
            fileObj.write('-'*80 + '\n')
            content =  allcontent[num][doc]
            content = [x for x in content if x != '\n']
            heighlight = '<p>'
            for line in content:
                token = map(str, line.split(" "))
                buffer = 0
                for word in token:
                    if str.lower(word) in queries[str(num)] and str.lower(word) not in stop_list:
                        boldword = word
                        heighlight += '...<b>' + boldword + '</b> '
                        buffer = 0
                    elif buffer < 3:
                        heighlight += word + ' '
                        buffer += 1
                    else:
                        continue
            heighlight += '</p>'
            fileObj.write(heighlight)
            fileObj.write('\n')
        fileObj.close()
    print 'creat snippet done.'


if __name__ == '__main__':
    start = time.time()
    stop_list = stop_words(stop_file)
    # print stop_list
    folder1 = 'BM25_QE_Dice_SE'
    folder2 = 'BM25_QE_Thesauri_SE'
    folder3 = 'BM25_SE'
    folder4 = 'BM25_Stop_SE'
    folder5 = 'Tf_idf_SE'
    folder6 = 'Tf_idf_Stop_SE'
    folder7 = 'Lucene_SE'
    snippet(folder1)
    snippet(folder2)
    snippet(folder3)
    snippet(folder4)
    snippet(folder5)
    snippet(folder6)
    snippet(folder7)
    end = time.time()
    print '-'* 80
    print 'total run time is:', end-start,'s'