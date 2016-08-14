#importing python modules and libraries
import urllib2
import re
from bs4 import BeautifulSoup

#url of the desired webpage
page_url = "http://www.healthcaremagic.com/community"

categories = []

#this function retrives the title, url and number of each category
def get_values(page_url):
	page = urllib2.urlopen(page_url)
	soup = BeautifulSoup(page,'lxml')
	page.close()
	categories_a = soup.find_all("a",class_="questionTitle")
	for category_a in categories_a:
		title = category_a.string
		title = title.lstrip()
		title = title.rstrip()
		url = "http://www.healthcaremagic.com"+category_a.get('href')
		url = url.lstrip()
		url = url.rstrip()
		match = re.search(r'\d+',url)
		match = match.group()
		number = match
		d = [title,url,number]
		categories.append(d)

get_values(page_url)