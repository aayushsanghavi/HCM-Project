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

#url of the desired webpage
page_urls = []
number_of_questions = []
questions_per_page = 20

#this code creates a file questions.csv and stores all the information retrived
file = open('questions.csv','wb')
write = csv.writer(file,delimiter=",")

#this piece of code opens the categories.csv file and retrives previously stored information
file = open('categories.csv','rb')
read = csv.reader(file)
for row in read:
	number = int(row[3])
	number_of_questions.append(number)
	url = row[1]
	page_urls.append(url)

#this function retrives the title and url of each question of each category
def get_values(page_url):
	page = urllib.urlopen(page_url)
	soup = BeautifulSoup(page,'lxml')
	page.close()
	
	all_div = soup.find_all("div",class_="questionBox linePadding10")
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

#this code loops through all pages and calls the get_values function to retrive the data
for i in range(len(page_urls)):
	page = 0
	for page in range(number_of_questions[i]):
		url = page_urls[i]+"/"+str(page)
		try:			
			get_values(url)
		except Exception, e:
			logger.error('Failed to get_values',exc_info=True)
		page += 20