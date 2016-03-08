import math
num={}
inlink_dic={}
in_graph={}
with open("/Users/XianlongZhang/Desktop/WG2.txt", 'r') as file_object:
	for line in file_object.readlines():
		in_elements =line.strip().split(' ')
		temp_list = in_elements[1:]
		in_graph[in_elements[0]] = temp_list

for page, inlinks in in_graph.items():
	inlink_dic[page] = len(set(inlinks))
	num[len(set(inlinks))]=0

for page, inlinks in in_graph.items():
	inlink_dic[page] = len(set(inlinks))
	num[len(set(inlinks))]+=1


		#print link
	#print "***********"

for inlinknum, webnumber in num.items():
	if inlinknum!=0:
		print str(math.log(webnumber,2))+" "+str(math.log(inlinknum,2))