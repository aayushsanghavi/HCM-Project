#importing python modules and libraries
import urllib2
import re
import csv
from bs4 import BeautifulSoup

#url of the desired webpage
page_urls = []
number_of_questions = []
questions_per_page = 20
url_regex = re.compile(ur'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')
questions = []

#this piece of code opens the categories.csv file and retrives previously stored information
file = open('categories.csv','rb')
read = csv.reader(file)
for row in read:
	row = str(row)
	match = re.search(r'\d+ questions',row)
	if match:
		match = match.group()
		value = match
		number = re.search(r'\d+',value)
		number = number.group()
		number_of_questions.append(number)

	match = re.search(url_regex,row)
	if match:
		match = match.group()
		url = match
		page_urls.append(url)

#this function retrives the title and url of each question of each category
def get_values(page_url):
	page = urllib2.urlopen(page_url)
	soup = BeautifulSoup(page,'lxml')
	page.close()
	
	all_div = soup.find_all("div",class_="questionBox linePadding10")
	for div in all_div:
		a = div.find("a",class_="questionTitle")
		title = a.string
		title = title.lstrip()
		title = title.rstrip()
		url = "http://www.healthcaremagic.com"+a.get('href')
		url = url.lstrip()
		url = url.rstrip()
		d = [title,url]
		questions.append(d)

#this function goes to all pages and calls get_values function to retrive the date
def get_next_page():
	for i in range(len(page_urls)):
		pages = number_of_questions[i]/questions_per_page
		for page in range(pages):
			url = page_urls[i]+str(page)
			get_values(url)

get_next_page()