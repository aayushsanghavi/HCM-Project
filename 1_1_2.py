#importing python modules and libraries
import urllib2
import re
from bs4 import BeautifulSoup

#url of the desired webpage
categories = []
webpages = ["disease-and-conditions","drugs","treatments","procedures","lab-tests"]

#this segment of code retrives the url of the next page
def get_next_page(page_link):
	page = urllib2.urlopen(page_link)
	soup = BeautifulSoup(page,'lxml')
	get_values(soup)
	page_li = soup.find_all("a",class_="box");
	page.close()
	for li in page_li:
		page_li_value = li.string
		page_li_url = li.get('href')
		page_li_value = page_li_value.lstrip()
		page_li_value = page_li_value.rstrip()
		match = re.search(r'\D+',page_li_value)
		if match:
			match = match.group()
			if match:
				next_page_url = "http://www.healthcaremagic.com" + page_li_url
		else:
			next_page_url = None
	return next_page_url
		
#this function retrives the title, url and number of each category for the specific url
def get_values(soup):
	ul = soup.find("ul",class_="itemListUL anchorListing")
	all_li = ul.find_all("li")
	for li in all_li:
		title = li.a.string
		title = title.lstrip()
		title = title.rstrip()
		url = "http://www.healthcaremagic.com" + li.a.get('href')
		url = url.lstrip()
		url = url.rstrip()
		match = re.search(r'\d+',url)
		match = match.group()
		number = match
		d = [title,url,number]
		categories.append(d)

#this loop extracts all the required information from all the pages of each category
for webpage in webpages:
	page_url = "http://www.healthcaremagic.com/topics/" + webpage
	continue_extraction = True
	
	#this loop extracts all the required information from all the pages
	while continue_extraction:
		next_page = get_next_page(page_url)
		if next_page == None:
			continue_extraction = False
		else:
			pass
		page_url = next_page