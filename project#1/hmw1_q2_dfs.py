# -*- coding: utf-8 -*- 
import requests
from bs4 import BeautifulSoup
import urllib2
import urlparse
import time
import re 

urls_containing_keyphrase = []
url_frontier = []
seed_page = "http://en.wikipedia.org/wiki/Sustainable_energy"
def is_valid_url(current_page_url, href_text):
	return ":" not in href_text \
		and "http://en.wikipedia.org/wiki/" in urlparse.urljoin(current_page_url, href_text)\
		and "http://en.wikipedia.org/wiki/Main_Page" not in urlparse.urljoin(current_page_url, href_text)

def is_unique_url(url):
	return url not in [i[0] for i in urls_containing_keyphrase]

def crawling(keyphrase, maxdepth=5): 
	depth = 1 
	total_crawled_urls = 1

	# Apply DFS
	urls_containing_keyphrase.append((seed_page, depth))
	print "crawled=%d depth=%d for %s" %(total_crawled_urls, depth, seed_page)
	def _get_child_url(currpage,depth):
		raw_html=requests.get(currpage)
		soup=BeautifulSoup(raw_html.content,"lxml")
		#The HttpConnectionError may happen in DFS situation, so I use "try" to throw exception.
		try:
			for link in soup.find_all('a', href=True):
				
				if is_valid_url(currpage, link['href']):
					whole_url=urlparse.urljoin(currpage, link['href'])
					if "#" in whole_url:
						whole_url=whole_url[:whole_url.find("#")]

					if is_unique_url(whole_url):
						raw_html=requests.get(whole_url)
						soup=BeautifulSoup(raw_html.content,"lxml")
						regex_keyphrase = re.compile(keyphrase, re.IGNORECASE)
						for tag in soup.findAll(['script', 'form']) + soup.findAll(id="footer"):
							tag.extract()
						text = soup.get_text()
						lines = (line.strip() for line in text.splitlines())
						chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
						text = '\n'.join(chunk for chunk in chunks if chunk)

						if regex_keyphrase.search(text):
							if len(urls_containing_keyphrase)<1000:
								urls_containing_keyphrase.append((whole_url,depth+1))
								print "crawled=%d depth=%d for %s" %(len(urls_containing_keyphrase), depth+1, whole_url)
								if depth+1<maxdepth:
									time.sleep(1)
									_get_child_url(whole_url,depth+1)
							else:
								return 0
		except:
			return 0
	_get_child_url(seed_page, depth)

print "At most 1000 URLs crawled upto depth 5:"
print "---------------------------------------"
crawling(keyphrase="solar", maxdepth=5)
