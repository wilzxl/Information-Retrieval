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

def crawling(keyphrase, maxdepth=5): 
	depth = 1 
	track_depth = 0
	total_keyphrase_url = 0

	def _fulfill_condition():
		return len(url_frontier) != 0 and depth <= maxdepth and total_keyphrase_url < 1000

	# Apply BFS
	url_frontier.append((seed_page,1))
	while _fulfill_condition(): 
		page_url, depth =  url_frontier.pop(0)
		if is_unique_url(page_url):
			visited_urls.append((page_url, depth))
			#time.sleep(1)
			raw_html = requests.get(page_url)
			soup = BeautifulSoup(raw_html.content, "lxml")

			def _get_adj_url():
				for link in soup.find_all('a', href=True):
					if is_valid_url(page_url, link['href']):
						whole_url = urlparse.urljoin(page_url, link['href'])
						if "#" in whole_url:
							whole_url = whole_url[:whole_url.find("#")]
						if is_unique_url(whole_url):
							url_frontier.append((whole_url, depth + 1))

			regex_keyphrase = re.compile(keyphrase, re.IGNORECASE)
			for tag in soup.findAll(['script', 'form']) + soup.findAll(id="footer"):
				tag.extract()

			text = soup.get_text()
			lines = (line.strip() for line in text.splitlines())
			chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
			text = '\n'.join(chunk for chunk in chunks if chunk)
			if regex_keyphrase.search(text):
				#urls_containing_keyphrase.append(page_url)
				total_keyphrase_url = total_keyphrase_url + 1
				print "key_crawled=%d depth=%d for %s" %(total_keyphrase_url, depth, page_url)
				_get_adj_url()
	return 0
			
print "At most 1000 URLs crawled upto depth 5:"
print "---------------------------------------"
crawling(keyphrase="solar", maxdepth =5)