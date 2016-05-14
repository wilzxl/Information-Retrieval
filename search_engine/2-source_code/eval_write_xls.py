import sys
reload(sys)
import os
import math
from collections import defaultdict

precis_dic=defaultdict(int)
doc_dic=defaultdict(dict)
relev_doc_dic=defaultdict(list)
total_preci=defaultdict(int)
RR=defaultdict(int)
AVP=defaultdict(int)
query_list=[]
relev_file_name='cacm.rel'

#get all information of a specific query, create relevant file for each query
def get_query_list():
	dirs=os.listdir('Tf_idf_Stop_SE/')
	for f in dirs:
		if f!='.DS_Store':
			query_no=int(f.replace('.txt',''))
			query_list.append(query_no)
	return query_list

def get_docs(file_name):
	with open('Tf_idf_Stop_SE/'+file_name, 'r') as file_object:
		for line in file_object.readlines():
			#format: query_id Q0 doc_id rank BM25_score system_name
			temp_list=line.split()
			rank=int(temp_list[-3])
			doc_dic[rank]['doc_id']=temp_list[2]
			doc_dic[rank]['score']=float(temp_list[-2])

#get relevant documents for specific query in expansion query txt
#format: rank Q0 doc_id relevance(1)
def get_relev(query_id):
	with open(relev_file_name) as file_object:
		for line in file_object.readlines():
			temp_list=line.split()
			if temp_list[0]==str(query_id):
				#format: rele_dic[query_id]=doc_id
				relev_doc_dic[query_id].append(temp_list[-2])

def calcu_precision_recall(query_id):
	relev_num=0
	total_relev_num=len(relev_doc_dic[query_id])
	if total_relev_num==0:
		return 0
	for rank, info in doc_dic.iteritems():
		if info['doc_id'] in relev_doc_dic[query_id]:
			relev_num+=1
			doc_dic[rank]['relevance']=1
		else:
			doc_dic[rank]['relevance']=0

		doc_dic[rank]['precision']=float(relev_num)/rank
		doc_dic[rank]['recall']=float(relev_num)/total_relev_num
		if info['doc_id'] in relev_doc_dic[query_id]:
			total_preci[query_id]+=doc_dic[rank]['precision']
	#calculate RR and AVG for each query		
	AVP[query_id]=round(float(total_preci[query_id])/total_relev_num,6)
	for rank, info in doc_dic.iteritems():
		if doc_dic[rank]['relevance']==1:
			RR[query_id]=round(1/float(rank),6)
			break

def calcu_MAP(query_id_list):
	MAP=0
	preci_sum=0
	for query_txt in query_id_list:
		query_id=str(query_txt)
#		query_id=query_txt.replace('.txt','')
		relev_num_for_query=len(relev_doc_dic[query_id])
		if relev_num_for_query==0:
			break
#		print query_id,relev_num_for_query
		preci_sum+=(total_preci[query_id]/relev_num_for_query)
	MAP=preci_sum/len(query_id_list)
	return MAP

def preci_at_k(position):
	return doc_dic[position]['precision']

def calcu_MRR(query_id_list):
	MRR=0
	RR_sum=0
	for query_txt in query_id_list:
		query_id=str(query_txt)
#		query_id=query_txt.replace('.txt','')
		RR_sum+=(RR[query_id])
	MRR=RR_sum/len(query_id_list)
	return MRR


query_list=get_query_list()
query_list.sort()
with open('Tf_idf_Stop_AVP_RR.xls','a') as file_object:
	file_object.write("Tf_idf_Stop"+"\t"+"AVP"+"\t"+"RR"+"\r")
for relev_file in query_list:
	#reset
	doc_dic.clear()
#	relev_num = 0
	query_id=str(relev_file)
	get_docs(query_id+'.txt')
	get_relev(query_id)
#	calcu_precision_recall(query_id)
	if calcu_precision_recall(query_id)!=0:
		if len(doc_dic)>5:
			k5=preci_at_k(5)
		else:
			k5="numberlessthan5"
		if len(doc_dic)>20:
			k20=preci_at_k(20)
		else:
			k20="numberlessthan20"
		with open('Tf_idf_Stop_eval/'+query_id+'_eval.xls', 'a') as file_object:
			file_object.write("Precision at 5:"+"\t"+str(k5)+"\t"+"Precision at 20:"+"\t"+str(k20)+"\r")
			file_object.write("Rank"+"\t"+"Doc_id"+"\t"+"Score"+"\t"+"Relevance"+"\t"+"Precision"+"\t"+"Recall"+"\r")
		for rank, info in doc_dic.iteritems():
			#change name for each SE run
			with open('Tf_idf_Stop_eval/'+query_id+'_eval.xls', 'a') as file_object:
				file_object.write(str(rank) +"\t"+ str(info['doc_id'])+"\t"+ str(info["score"]) +"\t"+str(info["relevance"]) +"\t"+str(round(info["precision"],6)) +"\t"+ str(info["recall"])+'\r')
		with open('Tf_idf_Stop_AVP_RR.xls','a') as file_object:
			file_object.write(str(query_id)+"\t"+str(AVP[query_id])+"\t"+str(RR[query_id])+"\r")

MAP=calcu_MAP(query_list)
MRR=calcu_MRR(query_list)	

print "All eval files are written in folder. The values of MAP and MRR are as following:"
with open('Tf_idf_Stop_eval.xls','a') as file_object:
	file_object.write("SE"+"\t"+"MAP"+"\t"+"MRR"+'\r')
	#searchengine name
	file_object.write("Tf_idf_Stop"+"\t"+str(round(MAP,6))+"\t"+str(round(MRR,6))+"\r")

