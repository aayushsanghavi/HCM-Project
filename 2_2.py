#importing python modules and libraries
import urllib2
import re
import csv
from bs4 import BeautifulSoup

d = {}
r = {}

def to_number(variable):
	variable = variable.encode('ascii','ignore')
	variable = variable.lstrip()
	variable = variable.rstrip()
	variable = int(variable)
	return variable

def to_string(variable):
	variable = variable.encode('ascii','ignore')
	variable = variable.lstrip()
	variable = variable.rstrip()
	return variable

def get_values(page_url):
	page = urllib2.urlopen(page_url)
	soup = BeautifulSoup(page,'lxml')
	page.close()
	
	main_div = soup.find("div",class_="outerBox")	
	outer_div = main_div.find("div",class_="questionDivWrapper")
	div = outer_div.find("div",class_="questionDivWrapper")
	inner_div = div.find("div",class_="postQuestion")	
	
	write.writerow("Question and answers")	
	#question title
	h1 = outer_div.find("h1",class_="OrangeH1")
	title = h1.string
	title = to_string(title)
	d['question_title'] = title

	#question statement
	question_div = inner_div.find("div",class_="paragraph")
	question = question_div.text
	question = to_string(question)
	d['question_statement'] = question

	#question asked on
	spans = inner_div.find_all("span",class_="greyText")
	date = spans[0].b.string
	date = to_string(date)
	d['question_date'] date

	#number of answers
	answers = spans[2].string
	answers = to_number(answers)
	d['number_of_answers'] = answers

	#number of views
	views = spans[4].string
	views = to_number(views)
	d['number_of_views'] = views

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
			d[title] = content
	
	answers_divs = main_div.find_all("div",class_="answerWrapper")
	for answers_div in answers_divs:
		doctor_info = answers_div.find("div",class_="doctorResponse")
		if doctor_info:
			#doctor title
			title = doctor_info.span.string
			title = to_string(title)
			d['doctor_title'] = title
			
			#doctor name and url
			span = doctor_info.find("span",class_="lightBlue")
			name = span.a.string
			name = to_string(name)
			d['doctor_name'] = name

			url = "http://www.healthcaremagic.com"
			url += span.a.get('href')
			d['doctor_url'] = url
			
			#doctor id
			match = re.search(r'\d+',url)
			match = match.group()
			number = match
			number = to_number(number)
			d['doctor_id'] = number
			
			#doctors who agree with the answer
			p = answers_div.find("p",style="color:#19730e;padding-top:2px;")
			if p:
				agree = p.string
				match = re.search(r'\d+',agree)
				match = match.group()
				number = match
				number = to_number(number)
				d['doctors_agreeing'] = number

		user_info = answers_div.find("span",class_="userResponse")
		if user_info:
			#user name
			user_info = answers_div.find("span",class_="userResponse")
			name = user_info.string
			name = to_string(name)
			d['user_name'] = name
		
		#doctor/user answer
		answer = answers_div.find("div",class_="paragraph")
		doctorResponse = answer.text
		doctorResponse = to_string(doctorResponse)
		d['answer_text'] = doctorResponse

		#answer date
		date_div = answers_div.find("div",class_="postedText")
		date = date_div.text
		date = date.replace("Answered:","")
		date = to_string(date)
		d['answer_date'] = date

	write.writerow(d)
	write.writerow("Related and recent questions")
	
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
				r['doctor_title'] = title
				url = doctor_info.get('style')

				match = re.search(r'/icon/\d+',url)
				if match:
					match = match.group()		
					match = re.search(r'\d+',match)
					if match:			
						match = match.group()
						number = match
						number = to_number(number)
						r['doctor_id'] = number

			#related question information
			question_info = div.find("div",style="float:left; width: 88%; padding-left: 20px;")
			question = question_info.a.string
			question = to_string(question)
			r['related_question_statement'] = question

			#related question url
			url = "http://www.healthcaremagic.com"
			url += question_info.a.get('href')
			r['related_question_url'] = url
			
			#related question id
			match = re.search(r'\d+',url)
			match = match.group()
			number = match
			number = to_number(number)
			r['related_question_id'] = number

	#people also viewed information
	people_viewed = main_div.find("div",class_="FullDiv anchorListing")
	if people_viewed:
		all_li = people_viewed.find_all("li")
		for li in all_li:

			#viewed question
			title = li.a.string
			title = to_string(title)
			r['people_viewed_question'] = title
			
			#url
			url = "http://www.healthcaremagic.com"			
			url += li.a.get('href')
			r['people_viewed_url'] = url

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
				r['doctor_title'] = title
				
				#doctor url
				url = doctor_info.get('style')

				#doctor id
				match = re.search(r'/icon/\d+',url)
				match = match.group()			
				match = re.search(r'\d+',match)
				match = match.group()
				number = match
				number = to_number(number)
				r['doctor_id'] = number

			question_info = div.find("div",style="float:left; width: 88%; padding-left: 20px;")

			#recent question statement
			question = question_info.a.string
			question = to_string(question)
			r['recent_question_statement'] = question
			
			#recent question url
			url = "http://www.healthcaremagic.com"		
			url += question_info.a.get('href')
			r['recent_question_url'] = url
			
			#question id
			match = re.search(r'\d+',url)
			match = match.group()
			number = match
			number = to_number(number)
			r['recent_question_id'] = number

	write.writerow(r)

#this code creates a file answers.csv and stores all the information retrived
file = open('answers.csv','wb')
write = csv.writer(file,delimiter=",")

#this piece of code opens the questions.csv file and retrives previously stored information
file = open('questions.csv','rb')
read = csv.reader(file)
for row in read:
	get_values(row[1])
	d.clear()
	r.clear()