import re
import operator
file_object_1 = open('/Users/XianlongZhang/Desktop/KT_value/test.txt')
file_object_2 = open('/Users/XianlongZhang/Desktop/KT_value/WG2_inlink.txt')
list_of_pagerank = file_object_1.read().split('\n')
list_of_inlink=file_object_2.read().split('\n')
count=0
cor=0
discor=0
for link1 in list_of_pagerank:
	count+=1
	cor_num=0
	discor_num=0
	if link1 in list_of_inlink:
		for link2 in list_of_inlink[list_of_inlink.index(link1)+1:]:
			if link2 in list_of_pagerank[count:]:
				cor_num+=1
			if link2 in list_of_pagerank[:count-1]:
				discor_num+=1
		discor=discor+discor_num
		cor=cor+cor_num
print cor		
print discor
		#print link1
a=0
for link1 in list_of_pagerank:
	for link2 in list_of_inlink:
		if link1==link2:
			a+=1
			#print link2
print a






