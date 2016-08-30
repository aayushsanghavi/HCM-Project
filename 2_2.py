#importing python modules and libraries
import urllib2
import re
import csv
from bs4 import BeautifulSoup

#url of the desired webpage
page_url = "http://www.healthcaremagic.com/questions/Is-there-any-Vaccination-for-AIDS/56"

#this function retrives the title, url and number of each category and number of questions asked
def get_values(page_url):
	page = urllib2.urlopen(page_url)
	soup = BeautifulSoup(page,'lxml')
	page.close()
	
	#this segment of code retrives title, url and number of each category
	outer_div = soup.find("div",class_="questionDivWrapper")
	div = outer_div.find("div",class_="questionDivWrapper")

	h1 = outer_div.find("h1",class_="OrangeH1")
	title = h1.string
	title = title.lstrip()
	title = title.rstrip()

	inner_div = div.find("div",class_="postQuestion")	
	question_div = inner_div.find("div",class_="paragraph")
	question = question_div.text
	question = question.lstrip()
	question = question.rstrip()
	
	spans = inner_div.find_all("span",class_="greyText")
	date = spans[0].b.string
	date = date.lstrip()
	date = date.rstrip()

	answers = spans[2].string
	answers = answers.lstrip()
	answers = answers.rstrip()

	views = spans[4].string
	views = views.lstrip()
	views = views.rstrip()

	question_related_info = inner_div.find("div",class_="anchorBox")
	rows = question_related_info.find_all("div",class_="row")
	for row in rows:
		row_div = row.find("span",class_="leftMeta")
		title = row_div.string
		title = title.lstrip()
		title = title.rstrip()

		content_div = row.find_all("div",class_="right")
		for div in content_div:
			content = div.a.string+", "
		content = content.rstrip(", ")

get_values(page_url)