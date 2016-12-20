#importing python modules and libraries
import urllib2
import re
import csv
from bs4 import BeautifulSoup
import sys
import logging
reload(sys)
sys.setdefaultencoding('utf8')

#log file setup
logger = logging.getLogger(__name__)
handler = logging.FileHandler('logfile_2_2.log')
logger.addHandler(handler)

r = {}

#these functions do type conversions
def to_string(variable):
	variable = variable.encode('ascii','ignore')
	variable = variable.lstrip()
	variable = variable.rstrip()
	return variable

def to_number(variable):
	variable = to_string(variable)
	variable = int(variable)
	return variable

#the main function that retrives the required data
def get_values(page_url):
	d = []
	#opens the requested page
	page = urllib2.urlopen(page_url)
	soup = BeautifulSoup(page,'lxml')
	page.close()
	
	main_div = soup.find("div",class_="outerBox")	
	outer_div = main_div.find("div",class_="questionDivWrapper")
	div = outer_div.find("div",class_="questionDivWrapper")
	inner_div = div.find("div",class_="postQuestion")
	
	#question title
	h1 = outer_div.find("h1",class_="OrangeH1")
	title = h1.string
	title = to_string(title)
	d.append(title)

	#question statement
	question_div = inner_div.find("div",class_="paragraph")
	question = question_div.text
	question = to_string(question)
	d.append(question)

	#question asked on
	spans = inner_div.find_all("span",class_="greyText")
	date = spans[0].b.string
	date = to_string(date)
	d.append(date)

	#number of answers
	answers = spans[2].string
	answers = to_number(answers)
	d.append(answers)

	#number of views
	views = spans[4].string
	views = to_number(views)
	d.append(views)

	#some question tags
	question_related_info = inner_div.find("div",class_="anchorBox")
	if question_related_info:
		rows = question_related_info.find_all("div",class_="row")
		for row in rows:
			row_div = row.find("span",class_="leftMeta")
			title = row_div.string
			title = to_string(title)

			content = ''
			div = row.find("div",class_="right")
			all_a = div.find_all("a")
			for a in all_a:
				content += a.string + ", "
			content = content.rstrip(", ")
			r[title] = content
	
		d.append(r)
		r.clear()

	#answer content
	answers_divs = main_div.find_all("div",class_="answerWrapper")
	for answers_div in answers_divs:
		doctor_info = answers_div.find("div",class_="doctorResponse")
		if doctor_info:
			#doctor title
			title = doctor_info.span.string
			title = to_string(title)
			d.append(title)
			
			#doctor name and url
			span = doctor_info.find("span",class_="lightBlue")
			name = span.a.string
			name = to_string(name)
			d.append(name)

			url = "http://www.healthcaremagic.com"
			url += span.a.get('href')
			url = to_string(url)
			d.append(url)
			
			#doctor id
			match = re.search(r'/([\d]+)',url)
			if match:
				match = match.group(1)
				number = match
				number = to_number(number)
				d.append(number)
			
			#doctors who agree with the answer
			p = answers_div.find("p",style="color:#19730e;padding-top:2px;")
			if p:
				agree = p.string
				match = re.search(r'\d+',agree)
				if match:
					match = match.group()
					number = match
					number = to_number(number)
					d.append(number)

		user_info = answers_div.find("span",class_="userResponse")
		if user_info:
			#user name
			user_info = answers_div.find("span",class_="userResponse")
			name = user_info.string
			name = to_string(name)
			d.append(name)
		
		#doctor/user answer
		answer = answers_div.find("div",class_="paragraph")
		doctorResponse = answer.text
		doctorResponse = to_string(doctorResponse)
		d.append(doctorResponse)

		#answer date
		date_div = answers_div.find("div",class_="postedText")
		date = date_div.text
		date = date.replace("Answered:","")
		date = to_string(date)
		d.append(date)
	
	#related questions
	related_questions_div = main_div.find("div",class_="FullDiv relatedFullTextList")
	if related_questions_div:
		inner_div = related_questions_div.find_all("div",class_="FullDiv linePadding5 borderBottom")
		for div in inner_div:
			#doctor information
			doctor_info = div.find("div",class_="doctorPhotoSmall")
			title = doctor_info.get('title')
			if title:
				title = to_string(title)
				d.append(title)
				url = doctor_info.get('style')
				url = to_string(url)

				match = re.search(r'/icon/([\d]+)',url)
				if match:
					match = match.group(1)		
					number = match
					number = to_number(number)
					d.append(number)

			#related question information
			question_info = div.find("div",style="float:left; width: 88%; padding-left: 20px;")
			if question_info:
				question = question_info.a.string
				question = to_string(question)
				d.append(question)

				#related question url
				url = "http://www.healthcaremagic.com"
				url += question_info.a.get('href')
				url = to_string(url)
				d.append(url)
				
				#related question id
				match = re.search(r'\d+',url)
				if match:
					match = match.group()
					number = match
					number = to_number(number)
					d.append(number)

	#people also viewed information
	people_viewed = main_div.find("div",class_="FullDiv anchorListing")
	if people_viewed:
		all_li = people_viewed.find_all("li")
		for li in all_li:

			#viewed question
			title = li.a.string
			title = to_string(title)
			d.append(title)
			
			#url
			url = "http://www.healthcaremagic.com"			
			url += li.a.get('href')
			url = to_string(url)
			d.append(url)

	#recent questions information
	recent_questions_div = main_div.find("div",class_="FullDiv aList")
	if recent_questions_div:
		inner_div = recent_questions_div.find_all("div",class_="FullDiv linePadding5 borderBottom")
		for div in inner_div:
			doctor_info = div.find("div",class_="doctorPhotoSmall")
			title = doctor_info.get('title')
			if title:
				
				#doctor who answered
				title = to_string(title)
				d.append(title)
				
				#doctor url
				url = doctor_info.get('style')
				url = to_string(url)

				#doctor id
				match = re.search(r'/icon/([\d]+)',url)
				if  match:
					match = match.group(1)		
					number = match
					number = to_number(number)
					d.append(number)

			question_info = div.find("div",style="float:left; width: 88%; padding-left: 20px;")

			#recent question statement
			question = question_info.a.string
			question = to_string(question)
			d.append(question)
			
			#recent question url
			url = "http://www.healthcaremagic.com"		
			url += question_info.a.get('href')
			url = to_string(url)
			d.append(url)
			
			#question id
			match = re.search(r'\d+',url)
			if match:
				match = match.group()
				number = match
				number = to_number(number)
				d.append(number)

	write.writerow(d)
	del d

#opens the categories.csv file and retrives category name and url
file3 = open('categories.csv','rb')
read = csv.reader(file3)

for row in read:
	file = row[0]+" questions.csv"
	#this creates a file for each category and stores all the questions retrived
	file2 = open(file,'rb')
	questions = csv.reader(file2)

	file = row[0]+" answers.csv"
	#this code creates a file answers.csv and stores all the information retrived
	file1 = open(file,'wb')
	write = csv.writer(file1,delimiter=",")

	#creates a temporary file that stores entries which had problems being retrived in the first try
	temp = open('temp.csv','wb')
	temp_write = csv.writer(temp,delimiter=",")

	for question in questions:
		try:
			get_values(question[1])	
		except Exception, e:
			logger.error('Error on page %s',question[1])
			logger.error('Failed to get_values',exc_info=True)
			temp_a = []
			#write the entry with errors to temp
			temp_a.append(question[1])		
			temp_write.writerow(temp_a)
			del temp_a
		r.clear()

	file2.close()
	temp.close()

	#open temp and run the get_values function again to retrive the lost entries
	file2 = open('temp.csv','rb')
	questions = csv.reader(file2)
	for question in questions:
		try:
			get_values(question[0])	
		except Exception, e:
			logger.error('Error on page %s',question[0])
			logger.error('Failed to get_values',exc_info=True)
		r.clear()

	file1.close()
	temp.close()

## To note that in very few cases the url causes infinite redirection loops
## Those entries will not be extracted but will be logged.