#importing python modules and libraries
import urllib
import re
import csv
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf8')

#url of the desired webpage
page_urls = []
number_of_questions = []
questions_per_page = 20
url_regex = re.compile(ur'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')

#this code creates a file questions.csv and stores all the information retrived
file = open('questions.csv','wb')
write = csv.writer(file,delimiter=",")

#this piece of code opens the categories.csv file and retrives previously stored information
file = open('categories.csv','rb')
read = csv.reader(file)
for row in read:
	number = row[3]
	number_of_questions.append(number)
	url = row[1]
	page_urls.append(url)

"""	row = str(row)
	match = re.search(r'([\d]+) questions',row)
	if match:
		match = match.group(1)
		value = match
		number = re.search(r'\d+',value)
		number = number.group()
		number_of_questions.append(number)

	match = re.search(url_regex,row)
	if match:
		match = match.group()
		url = match
		page_urls.append(url)"""

#this function retrives the title and url of each question of each category
def get_values(page_url):
	page = urllib.urlopen(page_url)
	soup = BeautifulSoup(page,'lxml')
	page.close()
	
	all_div = soup.find_all("div",class_="questionBox linePadding10")
	for div in all_div:
		a = div.find("a",class_="questionTitle")
		title = a.string
		title = title.encode('ascii','ignore')
		title = title.lstrip()
		title = title.rstrip()

		url = "http://www.healthcaremagic.com" + a.get('href')
		url = url.lstrip()
		url = url.rstrip()
		
		d = [title,url]
		write.writerow(d)

#this code loops through all pages and calls the get_values function to retrive the data
for i in range(len(page_urls)):
	pages = int(number_of_questions[i])/int(questions_per_page)
	for page in range(pages):
		url = page_urls[i]+str(page)
		get_values(url)