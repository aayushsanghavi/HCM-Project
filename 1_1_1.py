#importing python modules and libraries
import urllib2
import re
import csv
from bs4 import BeautifulSoup

#url of the desired webpage
page_url = "http://www.healthcaremagic.com/community"

categories = []

#this function retrives the title, url and number of each category and number of questions asked
def get_values(page_url):
	page = urllib2.urlopen(page_url)
	soup = BeautifulSoup(page,'lxml')
	page.close()
	
	#this segment of code retrives title, url and number of each category
	div = soup.find("div",class_="linePadding7")
	categories_a = div.find_all("a",class_="questionTitle")
	for category_a in categories_a:
		title = category_a.string
		title = title.lstrip()
		title = title.rstrip()

		url = "http://www.healthcaremagic.com"+category_a.get('href')
		url = url.encode('ascii','ignore')		
		url = url.lstrip()
		url = url.rstrip()

		match = re.search(r'\d+',url)
		match = match.group()
		number = match
		number = int(number)
		d = [title,url,number]
		categories.append(d)

	#this segment of code retrives the number of questions asked in the category
	i = 0
	categories_span = div.find_all("span",style="display: block;font-size:10px; color:#999;")
	for category_span in categories_span:
		questions = category_span.string
		match = re.search(r'\d+',questions)
		match = match.group()
		number = match
		questions = int(number)
		categories[i].append(questions)
		i += 1

#this runs the function
get_values(page_url)

#this code creates a file categories.csv and stores all the information retrived
file = open('categories.csv','wb')
write = csv.writer(file,delimiter=",")
for category in categories:
	write.writerow(category)