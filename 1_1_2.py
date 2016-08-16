#importing python modules and libraries
import urllib2
import re
from bs4 import BeautifulSoup

#url of the desired webpage
page_url = "http://www.healthcaremagic.com/topics/disease-and-conditions"
page = urllib2.urlopen(page_url)
soup = BeautifulSoup(page,'lxml')
page.close()
categories = []

#this segment of code retrives the url of the next page
def get_next_page(page_url):
	page_li = soup.find_all("a",class_="box");
	for li in page_li:
		page_li_value = li.string
		page_li_url = li.get('href')
		page_li_value = page_li_value.lstrip()
		page_li_value = page_li_value.rstrip()
		match = re.search(r'\D+',page_li_value)
		if match:
			match = match.group()
			next = match
			if next:
				next_page_url = "www.healthcaremagic.com" + page_li_url
				return next_page_url

#this function retrives the title, url and number of each category for the specific url
def get_values(page_url):
	ul = soup.find("ul",class_="itemListUL anchorListing")
	all_li = ul.find_all("li")
	for li in all_li:
		title = li.a.string
		title = title.lstrip()
		title = title.rstrip()
		url = "http://www.healthcaremagic.com"+li.a.get('href')
		url = url.lstrip()
		url = url.rstrip()
		match = re.search(r'\d+',url)
		match = match.group()
		number = match
		d = [title,url,number]
		categories.append(d)

#next_page_url = get_next_page(page_url)
#get_values(page_url)