from collections import defaultdict, OrderedDict
import math
import operator


def load_file(file_path):
	teleportation_factor = 0.1 
	in_graph = defaultdict(list)
	outlink_dic = defaultdict(int) 
	inlink_dic = defaultdict(int)
	perplexity =[] 
	sink_nodes =[]
	PAGE_RANK = defaultdict(float)  
	TEMP_PAGE_RANK = defaultdict(float)  

	def calcu_perplexity():
		entropy = 0
		for page in PAGE_RANK.keys():
			entropy += PAGE_RANK[page]*math.log(1.0/PAGE_RANK[page],2)
		return pow(2, entropy)

	def is_converged():
		perplex_1 = round(perplexity[-4]) 
		perplex_2 = round(perplexity[-3])
		perplex_3 = round(perplexity[-2])
		perplex_4 = round(perplexity[-1])
		return (perplex_1 == perplex_2 == perplex_3 == perplex_4)

	with open(file_path, 'r') as file_object:
		for line in file_object.readlines():
			in_elements =line.strip().split(' ')
			temp_list = in_elements[1:]
			in_graph[in_elements[0]] = temp_list

	# Calculate sources in task 1
	total_sources = 0
	for i in in_graph.keys():
		if len(in_graph[i]) == 0:
			total_sources+= 1

	# Calculate outlinks
	for link in in_graph.keys():
		outlink_dic[link]= 0
		#print link
	#print "***********"
	for link in in_graph.keys():
		#print link
		for in_nodes in set(in_graph[link]): 
			#print in_nodes
			outlink_dic[in_nodes]+= 1 
		#print outlink_dic
		#print "---------"	

	# Calculate sinks
	for page in outlink_dic:
		if outlink_dic[page] == 0:
			sink_nodes.append(page)

	total_pages =  len(in_graph)
	#total_sinks = len(sink_nodes)
	#print "ratio of pages with no inlinks (source nodes)"
	#print float(total_sources)/float(total_pages)

	#print "ratio of pages with no outlinks (sink nodes)"
	#print float(total_sinks)/float(total_pages)

	# Initial probability
	for page in in_graph.keys():
		PAGE_RANK[page] =  1.0/total_pages

#	while(len(perplexity)<=4 or not is_converged()):
#		sinkPR = 0
#		for page in sink_nodes:
#			sinkPR += PAGE_RANK[page]
#
#		for page, in_nodes in in_graph.iteritems():
#			TEMP_PAGE_RANK[page] = (1.0 - teleportation_factor) / total_pages
#			TEMP_PAGE_RANK[page] += teleportation_factor * sinkPR / total_pages
#			for in_node in set(in_graph[page]):			
#				TEMP_PAGE_RANK[page] += teleportation_factor * PAGE_RANK[in_node]/ outlink_dic[in_node]
#		for page in in_graph.keys():
#			PAGE_RANK[page] = TEMP_PAGE_RANK[page]
		
#		perplexity.append(calcu_perplexity())


#	with open('/Users/XianlongZhang/Desktop/output_perplexity.txt', 'a') as file_object:
#		if file_path=="/Users/XianlongZhang/Desktop/WG1.txt":
#			file_object.write("WG1---Perplexity values when get convergence\n")
#		else:
#			file_object.write("WG2---Perplexity values when get convergence\n")
#		for value in perplexity:
#			file_object.write(str(perplexity.index(value))+ " " + str(value) + "\n")
#
#	with open('/Users/XianlongZhang/Desktop/output_docID.txt', 'a') as file_object:
#		SortedPR = OrderedDict(sorted(PAGE_RANK.iteritems(), key=operator.itemgetter(1), reverse=True))
#		if file_path=="/Users/XianlongZhang/Desktop/WG1.txt":
#			file_object.write("WG1---Document IDs of the top 50 pages sorted by PageRank\n")
#		else:
#			file_object.write("\n\n---------------------------------------------------------\r")
#			file_object.write("WG2---Document IDs of the top 50 pages sorted by PageRank\n")
#		count = 1
#		for page, value in SortedPR.items():
#			file_object.write(page + "\n")
#			count =  count + 1
#			if count==51:
#				break

#		if file_path=="/Users/XianlongZhang/Desktop/WG1.txt":
#			file_object.write("\n\nWG1---Document IDs of the top 50 pages sorted by inlinks\n")
#		else:
#			file_object.write("\n\nWG2---Document IDs of the top 50 pages sorted by inlinks\n")
#
		for page, inlinks in in_graph.items():
			inlink_dic[page] = len(set(inlinks))
			print len(set(inlinks))
		

#		count = 1
#		SortedIL = OrderedDict(sorted(inlink_dic.iteritems(), key=operator.itemgetter(1), reverse=True))
#		for page, value in SortedIL.items():
#			file_object.write(page +"\n")
#			count  = count + 1
#			if count == 51:
#				break
				
load_file("/Users/XianlongZhang/Desktop/WG1.txt")
#load_file("/Users/XianlongZhang/Desktop/WG2.txt")

