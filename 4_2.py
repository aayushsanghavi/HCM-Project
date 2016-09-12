#importing python modules and libraries
import urllib2
import re
import csv
from bs4 import BeautifulSoup

d = {}

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

#this function retrives the title, url and number of each category and number of questions asked
def get_values(page_url):
	page = urllib2.urlopen(page_url)
	soup = BeautifulSoup(page,'lxml')
	page.close()
	
	main_div = soup.find("div",class_="DocBox")	
	div1 = main_div.find("div",style="width:100%;float:left;margin:0px;")
	div2 = main_div.find("div",class_="FullDiv")
	div3 = main_div.find("div",style="width:100%;float:left;margin-top:10px;")
	div4 = main_div.find("div",id="listOfreviews")
	div5 = main_div.find_all("div",class_="hpInWrap")
	div6 = main_div.find("div",class_="FullDiv relatedFullTextList")

	h1 = div1.find("h1",class_="OrangeH1")
	title = h1.span.string
	title = to_string(title)
	title = title.replace("  ","")
	d['doctor_name'] = title
	
	if div2:
		div = div2.find("div",style="float: left; width: 54%;")
		if div:
			doctor_level = div.text
			doctor_level = to_number(doctor_level)
			d['doctor_level'] = doctor_level

		div = div2.find("div",class_="userView")
		if div:
			views = div.text
			views = to_number(views)
			d['number_of_views'] = views

		span = div2.find("span",style="color: #777; float: left; font-size: 14px; margin-top: 1px;padding-left: 9px;")
		if span:
			span = span.find("span")
			agree = span.string
			agree = to_number(agree)
			d['number_of_doctors_agreeing'] = agree

		span = div2.find("span",style="color: #777; float: left; font-size: 14px; margin-top: 1px;padding-left: 7px;")
		if span:
			span = span.find("span")
			helpful = span.string
			helpful = to_number(helpful)
			d['number_of_helpful_answers'] = helpful

		span = div2.find("span",style="color: #777; float: left; font-size: 14px; padding-left: 12px;")
		if span:
			spans = span.find_all("span",style="color: #2990b1;font-size: 18px;font-weight: bold;")
			answered = spans[0].string
			answered = to_number(answered)
			d['number_of_questions_answered'] = answered
			answered = spans[1].string
			answered = to_number(answered)
			d['number_of_premium_questions_answered'] = answered

		div = div2.find("div",class_="bubbleStatus")
		if div:
			status = div.text
			status = to_string(status)
			d['profile_status'] = status

	if div3:
		div = div3.find("div",class_="row",id="contactDetailsDiv")
		if div:
			labels = div.find_all("div",class_="label")
			values = div.find_all("div",class_="value")
			for i in range(len(labels)):
				labels[i] = labels[i].text
				values[i] = values[i].text
				d[labels[i]] = values[i]

		inner_div = div3.find("div",class_="row",id="professionalDetailsDiv")
		if inner_div:
			div = inner_div.find("div",class_="row")
			labels = div.find_all("div",class_="label")
			values = div.find_all("div",class_="value")
			for i in range(len(labels)):
				labels[i] = labels[i].text
				values[i] = values[i].text
				d[labels[i]] = values[i]
		
			div = inner_div.find("div",id="officeDetailsDiv")
			if div:
				labels = div.find_all("div",class_="label").text
				values = div.find_all("div",class_="label").text
				for i in range(len(labels)):
					label[i] = label[i].to_string(label[i])
					value[i] = value[i].to_string(value[i])
					d[label[i]] = value[i]
			
			div = inner_div.find("div",id="graduationDetailsDiv")
			if div:
				labels = div.find_all("div",class_="label")
				values = div.find_all("div",class_="value")
				for i in range(len(labels)):
					labels[i] = labels[i].text
					values[i] = values[i].text
					labels[i] = to_string(labels[i])
					values[i] = to_string(values[i])
					d[labels[i]] = values[i]

			div = inner_div.find("div",id="otherDetailsDiv")
			if div:
				labels = div.find_all("div",class_="label")
				values = div.find_all("div",class_="value")
				for i in range(len(labels)):
					labels[i] = labels[i].text
					values[i] = values[i].text
					labels[i] = to_string(labels[i])
					values[i] = to_string(values[i])
					d[labels[i]] = values[i]

	if div5:
		n = 1
		inner_divs = div5[0].find_all("div",class_="smallPQIcon")
		for inner_div in inner_divs:
			title = inner_div.a.string
			title = to_string(title)
			d["premium_question_"+str(n)] = title

			url = "http://www.healthcaremagic.com" + inner_div.a.get('href')
			url = url.lstrip()
			url = url.rstrip()
			d["premium_question_url_"+str(n)] = url

			match = re.search(r'\d+',url)
			if match:
				match = match.group()
				number = match
				number = to_number(number)
				d["premium_question_id_"+str(n)] = number
			n += 1
		
		n = 1
		inner_divs = div5[1].find_all("div",class_="smallQIcon")
		for inner_div in inner_divs:
			title = inner_div.a.string
			title = to_string(title)
			d["public_question_"+str(n)] = title

			url = "http://www.healthcaremagic.com" + inner_div.a.get('href')
			url = url.lstrip()
			url = url.rstrip()
			d["public_question_url_"+str(n)] = url

			match = re.search(r'\d+',url)
			if match:
				match = match.group()
				number = match
				number = to_number(number)
				d["public_question_id_"+str(n)] = number
			n += 1

		n = 1
		inner_divs = div6.find_all("div",class_="FullDiv linePadding5 borderBottom")
		for inner_div in inner_divs:
			a = inner_div.find("a")
			title = a.string
			title = to_string(title)
			d["related_answer"+str(n)] = title

			url = "http://www.healthcaremagic.com" + a.get('href')
			url = url.lstrip()
			url = url.rstrip()
			d["related_answer_url_"+str(n)] = url

			match = re.search(r'\d+',url)
			if match:
				match = match.group()
				number = match
				number = to_number(number)
				d["related_answer_id_"+str(n)] = number
			n += 1

	write.writerows(d.items())

#this code creates a file categories.csv and stores all the information retrived
file = open('doctorsInfo.csv','wb')
write = csv.writer(file,delimiter=",")

#this piece of code opens the categories.csv file and retrives previously stored information
file = open('doctors.csv','rb')
read = csv.reader(file)
for row in read:
	get_values(row[2])
	d.clear()