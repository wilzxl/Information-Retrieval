# -*- coding: utf-8 -*- 
import requests
from bs4 import BeautifulSoup
import urllib2
import urlparse
import time
import re 

visited_urls = []
url_frontier = []
seed_page = "http://en.wikipedia.org/wiki/Sustainable_energy"
def is_valid_url(current_page_url, href_text):
	return ":" not in href_text \
		and "http://en.wikipedia.org/wiki/" in urlparse.urljoin(current_page_url, href_text)\
		and "http://en.wikipedia.org/wiki/Main_Page" not in urlparse.urljoin(current_page_url, href_text)

def is_unique_url(url):
	return url not in [i[0] for i in visited_urls]

def crawling(maxdepth=5): 
	depth = 1 
	total_crawled_urls = 1

	# Apply DFS
	visited_urls.append((seed_page, depth))
	print "crawled=%d depth=%d for %s" %(total_crawled_urls, depth, seed_page)
	def _get_child_url(currpage,depth):
		response_obj=requests.get(currpage)
		soup=BeautifulSoup(response_obj.content,"lxml")
		for link in soup.find_all('a', href=True):
			
			if is_valid_url(currpage, link['href']):
				whole_url=urlparse.urljoin(currpage, link['href'])
				if "#" in whole_url:
					whole_url=whole_url[:whole_url.find("#")]
				if is_unique_url(whole_url):
					
					#print len(visited_urls)
					if len(visited_urls)<1000:
						visited_urls.append((whole_url,depth+1))
						print "crawled=%d depth=%d for %s" %(len(visited_urls), depth+1, whole_url)
						if depth+1<maxdepth:
							time.sleep(1)
							_get_child_url(whole_url,depth+1)

	_get_child_url(seed_page, depth)
print "At most 1000 URLs crawled upto depth 5:"
print "---------------------------------------"
crawling(maxdepth=5)
