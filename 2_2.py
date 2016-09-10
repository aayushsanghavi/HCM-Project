#importing python modules and libraries
import urllib2
import re
import csv
from bs4 import BeautifulSoup

d = {}
r = {}

#this function retrives the title, url and number of each category and number of questions asked
def get_values(page_url):
	page = urllib2.urlopen(page_url)
	soup = BeautifulSoup(page,'lxml')
	page.close()
	
	main_div = soup.find("div",class_="outerBox")	
	outer_div = main_div.find("div",class_="questionDivWrapper")
	div = outer_div.find("div",class_="questionDivWrapper")
	inner_div = div.find("div",class_="postQuestion")	
	
	write.writerow("Question and answers")	
	h1 = outer_div.find("h1",class_="OrangeH1")
	title = h1.string
	title = title.encode('ascii','ignore')
	title = title.lstrip()
	title = title.rstrip()
	d['question_title'] = title

	question_div = inner_div.find("div",class_="paragraph")
	question = question_div.text
	question = question.encode('ascii','ignore')
	question = question.lstrip()
	question = question.rstrip()
	d['question_statement'] = question

	spans = inner_div.find_all("span",class_="greyText")
	date = spans[0].b.string
	date = date.encode('ascii','ignore')
	date = date.lstrip()
	date = date.rstrip()
	d['question_date'] date

	answers = spans[2].string
	answers = answers.encode('ascii','ignore')
	answers = answers.lstrip()
	answers = answers.rstrip()
	answers = int(answers)
	d['number_of_answers'] = answers

	views = spans[4].string
	views = views.encode('ascii','ignore')
	views = views.lstrip()
	views = views.rstrip()
	views = int(views)
	d['number_of_views'] = views

	question_related_info = inner_div.find("div",class_="anchorBox")
	if question_related_info:
		rows = question_related_info.find_all("div",class_="row")
		for row in rows:
			row_div = row.find("span",class_="leftMeta")
			title = row_div.string
			title = title.encode('ascii','ignore')
			title = title.lstrip()
			title = title.rstrip()

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
			title = title.encode('ascii','ignore')		
			title = title.lstrip()
			title = title.rstrip()
			d['doctor_title'] = title
			
			#doctor name and url
			span = doctor_info.find("span",class_="lightBlue")
			name = span.a.string
			name = name.encode('ascii','ignore')
			name = name.lstrip()
			name = name.rstrip()
			d['doctor_name'] = name

			url = "http://www.healthcaremagic.com"
			url += span.a.get('href')
			d['doctor_url'] = url
			
			#doctor id
			match = re.search(r'\d+',url)
			match = match.group()
			number = match
			number = int(number)
			d['doctor_id'] = number
			
			#agreement
			p = answers_div.find("p",style="color:#19730e;padding-top:2px;")
			if p:
				agree = p.string
				match = re.search(r'\d+',agree)
				match = match.group()
				number = match
				number = int(number)				
				d['doctors_agreeing'] = number

		user_info = answers_div.find("span",class_="userResponse")
		if user_info:
			user_info = answers_div.find("span",class_="userResponse")
			name = user_info.string
			name = name.encode('ascii','ignore')
			name = name.lstrip()
			name = name.rstrip()
			d['user_name'] = name
		
		#doctor/user answer
		answer = answers_div.find("div",class_="paragraph")
		doctorResponse = answer.text
		doctorResponse = doctorResponse.lstrip()
		doctorResponse = doctorResponse.rstrip()	
		d['answer_text'] = doctorResponse

		#answer date
		date_div = answers_div.find("div",class_="postedText")
		date = date_div.text
		date = date.replace("Answered:","")
		date = date.lstrip()
		date = date.rstrip()
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
				title = title.encode('ascii','ignore')				
				title = title.lstrip()
				title = title.rstrip()
				r['doctor_title'] = title
				url = doctor_info.get('style')

				match = re.search(r'/icon/\d+',url)
				if match:
					match = match.group()		
					match = re.search(r'\d+',match)
					if match:			
						match = match.group()
						number = match
						number = int(number)
						r['doctor_id'] = number

			#question information
			question_info = div.find("div",style="float:left; width: 88%; padding-left: 20px;")
			question = question_info.a.string
			question = question.encode('ascii','ignore')
			question = question.lstrip()
			question = question.rstrip()
			r['related_question_statement'] = question

			url = "http://www.healthcaremagic.com"
			url += question_info.a.get('href')
			r['related_question_url'] = url
			
			match = re.search(r'\d+',url)
			match = match.group()
			number = match
			number = int(number)
			r['related_question_id'] = number

	#people also viewed information
	people_viewed = main_div.find("div",class_="FullDiv anchorListing")
	if people_viewed:
		all_li = people_viewed.find_all("li")
		for li in all_li:
			title = li.a.string
			title = title.encode('ascii','ignore')
			title = title.lstrip()
			title = title.rstrip()
			r['people_viewed_question'] = title
			
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
				title = title.encode('ascii','ignore')
				title = title.lstrip()
				title = title.rstrip()
				r['doctor_title'] = title
				
				url = doctor_info.get('style')
				match = re.search(r'/icon/\d+',url)
				match = match.group()			
				match = re.search(r'\d+',match)
				match = match.group()
				number = match
				number = int(number)
				r['doctor_id'] = number

			question_info = div.find("div",style="float:left; width: 88%; padding-left: 20px;")
			question = question_info.a.string
			question = question.encode('ascii','ignore')
			question = question.lstrip()
			question = question.rstrip()
			r['recent_question_statement'] = question
			
			url = "http://www.healthcaremagic.com"		
			url += question_info.a.get('href')
			r['recent_question_url'] = url
			
			match = re.search(r'\d+',url)
			match = match.group()
			number = match
			number = int(number)
			r['recent_question_id'] = number

	write.writerow(r)

#this code creates a file categories.csv and stores all the information retrived
file = open('answers.csv','wb')
write = csv.writer(file,delimiter=",")

#this piece of code opens the categories.csv file and retrives previously stored information
file = open('questions.csv','rb')
read = csv.reader(file)
for row in read:
	get_values(row[1])
	d.clear()
	r.clear()