#importing python modules and libraries
import urllib2
import re
import csv
from bs4 import BeautifulSoup

#url of the desired webpage
page_url = "http://www.healthcaremagic.com/questions/Suffering-from-fever/39"

#this function retrives the title, url and number of each category and number of questions asked
def get_values(page_url):
	page = urllib2.urlopen(page_url)
	soup = BeautifulSoup(page,'lxml')
	page.close()
	
	main_div = soup.find("div",class_="outerBox")	
	outer_div = main_div.find("div",class_="questionDivWrapper")
	div = outer_div.find("div",class_="questionDivWrapper")
	inner_div = div.find("div",class_="postQuestion")	

	h1 = outer_div.find("h1",class_="OrangeH1")
	title = h1.string
	title = title.lstrip()
	title = title.rstrip()

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

		content = ''
		div = row.find("div",class_="right")
		all_a = div.find_all("a")
		for a in all_a:
			content += a.string + ", "
		content = content.rstrip(", ")
	
	answers_divs = main_div.find_all("div",class_="answerWrapper")

	for answers_div in answers_divs:
		doctor_info = answers_div.find("div",class_="doctorResponse")
		if doctor_info:
			#doctor title
			title = doctor_info.span.string
			title = title.lstrip()
			title = title.rstrip()
			print title
			
			#doctor name and url
			span = doctor_info.find("span",class_="lightBlue")
			name = span.a.string
			name = name.lstrip()
			name = name.rstrip()
			print name
			url = span.a.get('href')
			print url
			
			#doctor id
			match = re.search(r'\d+',url)
			match = match.group()
			number = match
			print number
			
			#agreement
			p = answers_div.find("p",style="color:#19730e;padding-top:2px;")
			if p:
				agree = p.string
				match = re.search(r'\d+',agree)
				match = match.group()
				number = match
				print number

		else:
			user_info = answers_div.find("span",class_="userResponse")
			name = user_info.string
			name = name.lstrip()
			name = name.rstrip()
			print name
		
		#doctor/user answer
		answer = answers_div.find("div",class_="paragraph")
		doctorResponse = answer.text
		doctorResponse = doctorResponse.lstrip()
		doctorResponse = doctorResponse.rstrip()	
		print doctorResponse

		#answer date
		date_div = answers_div.find("div",class_="postedText")
		date = date_div.text
		date = date.lstrip("Answered:")
		date = date.lstrip()
		date = date.rstrip()
		print date

get_values(page_url)