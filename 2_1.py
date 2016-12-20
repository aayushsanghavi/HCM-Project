#importing python modules and libraries
import urllib
import re
import csv
import logging
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf8')
logger = logging.getLogger(__name__)
handler = logging.FileHandler('logfile_2_1.log')
logger.addHandler(handler)

questions_per_page = 20

#this function retrives the title and url of each question of each category
def get_values(page_url):
	page = urllib.urlopen(page_url)
	soup = BeautifulSoup(page,'lxml')
	page.close()
	
	all_div = soup.find_all("div",class_="questionBox linePadding10")
	num = len(all_div)
	for div in all_div:
		a = div.find("a",class_="questionTitle")
		title = a.string
		if title:
			title = title.encode('ascii','ignore')
			title = title.lstrip()
			title = title.rstrip()

			url = "http://www.healthcaremagic.com" + a.get('href')
			url = url.encode('ascii','ignore')
			url = url.lstrip()
			url = url.rstrip()
		
		d = [title,url]
		write.writerow(d)

	if (num == questions_per_page):
		return 1
	else:
		return 0

#opens the categories.csv file and retrives previously stored information
file2 = open('categories.csv','rb')
read = csv.reader(file2)
for row in read:
	file = row[0]+" questions.csv"
	#this creates a file for each category and stores all the questions retrived
	file1 = open(file,'wb')
	write = csv.writer(file1,delimiter=",")
	page = 0
	loops = int(row[3])/questions_per_page
	#loops through all pages and questions
	for i in range(loops):
		url = row[1]+"/"+str(page)
		try:
			keep_doing = get_values(url)
			if not keep_doing:
				break
		except Exception, e:
			logger.error('Error on page %s',url)
			logger.error('Failed to get_values',exc_info=True)
		page += 20
	
	#if it reached the last page
	if i == loops-1:
		page += 1
		url = row[1]+"/"+str(page)
		try:
			keep_doing = get_values(url)
		except Exception, e:
			logger.error('Error on page %s',url)
			logger.error('Failed to get_values',exc_info=True)
	
	file1.close()
file2.close()