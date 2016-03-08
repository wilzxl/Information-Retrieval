import requests
from bs4 import BeautifulSoup
import urllib2
import urlparse
import time
import re 

dictionary={}
links=[]
def is_unique(link, inlink):
	return inlink not in dictionary[link]

def is_valid_url(current_page_url, href_text):
	return ":" not in href_text \
		and "http://en.wikipedia.org/wiki/" in urlparse.urljoin(current_page_url, href_text)\
		and "http://en.wikipedia.org/wiki/Main_Page" not in urlparse.urljoin(current_page_url, href_text)

with open('/Users/XianlongZhang/Desktop/newoutput.txt', 'r') as file_object:
	for line in file_object.readlines():
		line=line.strip('\n')
		links.append(line)
	#print links
		
	for link in links:
	#	print link
		response_obj=requests.get(link)
		soup=BeautifulSoup(response_obj.content,"lxml")
		for url in soup.find_all('a',href=True):
			if is_valid_url(link, url['href']):
				whole_url=urlparse.urljoin(link, url['href'])
		

				if whole_url in links and link!=whole_url:
					#print True
					if whole_url in dictionary.keys() and is_unique(whole_url,link):
						dictionary[whole_url].append(link)
					else:
						dictionary[whole_url]=[link]
print dictionary
		
		#in_elements =line.strip().split(' ')
		#temp_list = in_elements[1:]
		#in_graph[in_elements[0]] = temp_list 