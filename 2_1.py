#importing python modules and libraries
import re
import sys
import csv
import logging
from urllib import request
from bs4 import BeautifulSoup

questions_per_page = 20
logger = logging.getLogger(__name__)
handler = logging.FileHandler('logfile_2_1.log')
logger.addHandler(handler)

#this function retrives the title and url of each question of each category
def get_values(page_url):
	page = request.urlopen(page_url).read().decode("utf-8", "ignore")
	soup = BeautifulSoup(page, "html.parser")
	all_div = soup.find_all("div", class_="questionBox linePadding10")

	for div in all_div:
		a = div.find("a")
		title = a.string.strip()
		url = "http://www.healthcaremagic.com" + a.get('href').strip()
		write.writerow([title, url])

#opens the categories.csv file and retrives previously stored information
read = csv.reader(open('categories.csv','r'))
for row in read:
	#this creates a file for each category and stores all the questions retrived
	write = csv.writer(open(row[0] + " questions.csv", "w"), delimiter=",")
	pages = int(int(row[3]) / questions_per_page) + 1

	page_num = 0
	for i in range(pages):
		try:
			url = row[1] + "/" + str(page_num)
			get_values(url)
		except Exception as e:
			logger.error('Error on page %s', url)
			logger.error('Failed to get_values', exc_info=True)
		page_num += 20
