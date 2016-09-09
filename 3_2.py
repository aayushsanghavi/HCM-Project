#importing python modules and libraries
import urllib2
import re
import csv
from bs4 import BeautifulSoup

#url of the desired webpage
page_url = "http://www.healthcaremagic.com/doctorchatlogs"

#this code creates a file categories.csv and stores all the information retrived
file = open('doctorchatLogs.csv','wb')
write = csv.writer(file,delimiter=",")

#this function retrives the next page url and the data from that page
def get_next_page(page_link):
	page = urllib2.urlopen(page_link)
	soup = BeautifulSoup(page,'lxml')
	content_div = soup.find("div",class_="mainContent")
	div = content_div.find("div", style="width:65%; float:left;")
	page.close()
	get_values(div)
	
	#this segment of code retrives the url of the next page
	pagination = div.find("div",id="paginationDiv")
	page_li = pagination.find_all("a",class_="box")
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
def get_values(content):
	all_div = content.find_all("div",class_="queriesBox")
	for div in all_div:
		inner_div = div.find("div",class_="smallChatIcon")
		title = inner_div.a.string
		title = title.lstrip()
		title = title.rstrip()
		url = "http://www.healthcaremagic.com" + inner_div.a.get('href')
		url = url.lstrip()
		url = url.rstrip()
		match = re.search(r'\d+',url)
		match = match.group()
		number = match
		d = [title,url,number]
		write.writerow(d)

#this loop extracts all the required information from all the pages
continue_extraction = True
while continue_extraction:
	next_page = get_next_page(page_url)
	if next_page == None:
		continue_extraction = False
	else:
		page_url = next_page