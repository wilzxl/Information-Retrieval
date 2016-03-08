"""
PageRank Algorithm
"""
__author__="Utkarsh J"

from collections import defaultdict, OrderedDict
import itertools
import math
import pdb
import operator

IN_DICT = defaultdict(list) # default graph representation
OUT_DICT = defaultdict(int) # dictionary maintaining total unique outlinks
TOTALIL_DICT = defaultdict(int) # total inlink dictionary
PAGE_RANK = defaultdict(float) # Dictionary maintaining page ranks 
NEW_PAGE_RANK = defaultdict(float) # Dictionary maintaining temporary new page ranks
teleportation_factor = 0.85 
perplexity = [] # List maintaining perplexity 
sink_nodes =  [] # Sink nodes 

def get_outlinks():
	""" Gets page and generates hash for outlinks
	"""
	for page in IN_DICT.keys():
		OUT_DICT[page] = 0
	for page in IN_DICT.keys():
		for in_nodes in set(IN_DICT[page]): # set because we do not want duplicates
			OUT_DICT[in_nodes] += 1 


def main(file_path):
	"""
	Argument :
		file_path - path of file from which in link data is to be read
	"""
	# Read input and store it in adjacency list
	with open(file_path, 'r') as file_object:
		for line in file_object.readlines():
			in_elements =  line.strip().split(' ')
			# hashmap for in link dictionary
			# Approach 2 - remove self links 
			# if in_elements[0] in in_elements[1: ]:
			# 	temp_list = [x for x in in_elements[1:] if x != in_elements[0]]
			# else:
			temp_list = in_elements[1:]
			# this may contain duplicates
			IN_DICT[in_elements[0]] = temp_list

	# Calculate sources
	total_sources = 0
	for i in IN_DICT.keys():
		if len(IN_DICT[i]) == 0:
			total_sources += 1

	get_outlinks()

	# Calculate sinks
	for page in OUT_DICT:
		if OUT_DICT[page] == 0:
			sink_nodes.append(page)

	# Calculate total pages
	total_no_pages =  len(IN_DICT)

main("/Users/XianlongZhang/Desktop/small_graph.txt")
IN_DICT['Z']=['a']
IN_DICT['Z'].append('b')
print IN_DICT.keys()