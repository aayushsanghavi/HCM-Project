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

print "From categories.csv - "
category = raw_input("Category name : ");
link = raw_input("Enter the category link : ");
number_of_questions = input("Number of questions in this category are : ");
print "From the incompletely extracted file "
page = input("The last extracted entry was : ");

#opens the categories.csv file and retrives previously stored information
file = category+" questions_part.csv"
#creates a file for each category and stores all the questions retrived
file1 = open(file,'wb')
write = csv.writer(file1,delimiter=",")
loops = (number_of_questions-page)/questions_per_page
for i in range(loops):
	url = link+"/"+str(page)
	try:
		keep_doing = get_values(url)
		if not keep_doing:
			break
	except Exception, e:
		logger.error('Error on page %s',url)
		logger.error('Failed to get_values',exc_info=True)
	page += 20
	
	if i == loops-1:
		page += 1
		url = link+"/"+str(page)
		try:
			keep_doing = get_values(url)
		except Exception, e:
			logger.error('Error on page %s',url)
			logger.error('Failed to get_values',exc_info=True)
	
file1.close()