#importing python modules and libraries
import urllib2
import re
import csv
from bs4 import BeautifulSoup
import httplib
import logging
import sys
reload(sys)
sys.setdefaultencoding('utf8')
logger = logging.getLogger(__name__)
handler = logging.FileHandler('logfile_4_2.log')
logger.addHandler(handler)

#url of the desired webpage
page_url = "http://www.healthcaremagic.com/doctors"

#this code creates a file doctors.csv and stores all the information retrived
file = open('doctors.csv','wb')
write = csv.writer(file,delimiter=",")

def to_string(title):
	title = title.encode('ascii', 'ignore')
	title = title.lstrip()
	title = title.rstrip()
	return title

#this function retrives the next page url and the data from that page
def get_next_page(page_link):
	page = urllib2.urlopen(page_link)
	soup = BeautifulSoup(page,'lxml')
	div = soup.find("div",id="dataDiv")
	page.close()
	get_values(div)
	
	#this segment of code retrives the url of the next page
	pagination = div.find("div",id="paginationDiv")
	if pagination:
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
		
#this function retrives the title, url, id, specialisation, number of reviews and location of each doctor
def get_values(content):
	all_div = content.find_all("div",id="singleDiv")
	for div in all_div:
		inner_div = div.find("div",style="float:left;width:100%;padding-bottom:5px;")
		spans = div.find_all("span",style="font-size:11px;")
		review_div = div.find("div",style="font-size:11px;width:90%;")

		title = inner_div.a.string
		if title:
			title = title.replace("  ","")
			title = to_string(title)
		
		url = "http://www.healthcaremagic.com" + inner_div.a.get('href')
		if url:
			url = to_string(url)
		
		match = re.search(r'\d+',url)
		if match:
			match = match.group()
			number = match
			number = int(number)
		
		specialisation = inner_div.span.string
		if specialisation:
			specialisation = to_string(specialisation)
		
		location = ""
		for span in spans:
			location += str(span.text)
		if location:
			location = to_string(location)

		reviews = "0"
		if review_div:
			reviews = to_string(reviews)
		reviews = int(reviews)

		d = [title,specialisation,url,number,location,reviews]
		write.writerow(d)

def patch_http_response_read(func):
    def inner(*args):
        try:
            return func(*args)
        except httplib.IncompleteRead, e:
            return e.partial

    return inner
httplib.HTTPResponse.read = patch_http_response_read(httplib.HTTPResponse.read)

#this loop extracts all the required information from all the pages
continue_extraction = True
while continue_extraction:
	try:
		next_page = get_next_page(page_url)	
	except Exception, e:
		logger.error('Error on page %s',page_url)
		logger.error('Failed to get_next_page',exc_info=True)		
	if next_page == None:
		continue_extraction = False
	else:
		page_url = next_page