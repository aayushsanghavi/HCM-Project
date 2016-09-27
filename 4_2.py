#importing python modules and libraries
import urllib2
import re
import csv
import logging
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf8')
logger = logging.getLogger(__name__)
handler = logging.FileHandler('logfile_4_2.log')
logger.addHandler(handler)

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

def get_questions(link,Qtype):
	page = urllib2.urlopen(link)
	soup = BeautifulSoup(page,'lxml')
	page.close()
	inner_divs = soup.find_all("div",class_="queriesBox")

	for inner_div in inner_divs:
		a = inner_div.find("a",class_="smallTitle")
		q = []
		title = a.get('title')
		title = to_string(title)
		q.append(title)

		url = "http://www.healthcaremagic.com" + a.get('href')
		url = to_string(url)
		q.append(url)

		match = re.search(r'/([\d]+)',url)
		if match:
			match = match.group(1)
			number = match
			number = to_number(number)
			q.append(number)

		if Qtype == 0:
			writePQ.writerow(q)
		else:
			writePFQ.writerow(q)
		del q	

	pagination = soup.find("div",id="paginationDiv")
	page_li = pagination.find_all("a",class_="box")
	next_page_url = None
	for li in page_li:
		page_li_value = li.string
		page_li_url = li.get('href')
		page_li_url = to_string(page_li_url)
		page_li_value = to_string(page_li_value)
		match = re.search(r'Next',page_li_value)
		if match:
			match = match.group()
			if match:
				next_page_url = "http://www.healthcaremagic.com" + page_li_url
	return 	next_page_url

def get_values(page_url):
	page = urllib2.urlopen(page_url)
	soup = BeautifulSoup(page,'lxml')
	page.close()
	d = []
	
	main_div = soup.find("div",class_="DocBox")	
	div1 = main_div.find("div",style="width:100%;float:left;margin:0px;")
	div2 = main_div.find("div",class_="FullDiv")
	div3 = main_div.find("div",style="width:100%;float:left;margin-top:10px;")
	div4 = main_div.find("div",id="listOfreviews")
	div5 = main_div.find_all("div",class_="hpInWrap")
	div6 = main_div.find("div",class_="FullDiv relatedFullTextList")

	h1 = div1.find("h1",class_="OrangeH1")
	#doctor name
	title = h1.span.string
	title = to_string(title)
	title = title.replace("  ","")
	d.append(title)
	
	if div2:
		div = div2.find("div",style="float: left; width: 54%;")
		if div:
			#doctor level
			doctor_level = div.text
			doctor_level = to_number(doctor_level)
			d.append(doctor_level)
		else:
			d.append("Not available")

		div = div2.find("div",class_="userView")
		if div:
			#number of views
			views = div.text
			views = to_number(views)
			d.append(views)
		else:
			d.append(0)

		span = div2.find("span",style="color: #777; float: left; font-size: 14px; margin-top: 1px;padding-left: 9px;")
		if span:
			#number of people who agree
			span = span.find("span")
			agree = span.string
			agree = to_number(agree)
			d.append(agree)
		else:
			d.append(0)

		span = div2.find("span",style="color: #777; float: left; font-size: 14px; margin-top: 1px;padding-left: 7px;")
		if span:
			#number of answers found helpful
			span = span.find("span")
			helpful = span.string
			helpful = to_number(helpful)
			d.append(helpful)
		else:
			d.append(0)

		span = div2.find("span",style="color: #777; float: left; font-size: 14px; padding-left: 12px;")
		if span:
			#number of public and premium questions answered
			spans = span.find_all("span",style="color: #2990b1;font-size: 18px;font-weight: bold;")
			answered = spans[0].string
			answered = to_number(answered)
			d.append(answered)
			answered = spans[1].string
			answered = to_number(answered)
			d.append(answered)
		else:
			d.append(0)
			d.append(0)

		div = div2.find("div",class_="bubbleStatus")
		if div:
			#doctor status
			status = div.text
			status = to_string(status)
			d.append(status)
		else:
			d.append("empty")

	if div3:
		#contact details
		div = div3.find("div",class_="row",id="contactDetailsDiv")
		if div:
			labels = div.find_all("div",class_="label")
			values = div.find_all("div",class_="value")
			for i in range(len(labels)):
				labels[i] = labels[i].text
				values[i] = values[i].text
				labels[i] = to_string(labels[i])
				values[i] = to_string(values[i])
				r[labels[i]] = values[i]

		inner_div = div3.find("div",class_="row",id="professionalDetailsDiv")
		if inner_div:
			#professional details
			div = inner_div.find("div",class_="row")
			if div:
				labels = div.find_all("div",class_="label")
				values = div.find_all("div",class_="value")
				for i in range(len(labels)):
					labels[i] = labels[i].text
					values[i] = values[i].text
					labels[i] = to_string(labels[i])
					values[i] = to_string(values[i])
					r[labels[i]] = values[i]
		
			div = inner_div.find("div",id="officeDetailsDiv")
			if div:
				#office details
				labels = div.find_all("div",class_="label")
				values = div.find_all("div",class_="value")
				for i in range(len(labels)):
					labels[i] = labels[i].text
					values[i] = values[i].text
					labels[i] = to_string(labels[i])
					values[i] = to_string(values[i])
					r[labels[i]] = values[i]
			
			div = inner_div.find("div",id="graduationDetailsDiv")
			if div:
				#graduation details
				labels = div.find_all("div",class_="label")
				values = div.find_all("div",class_="value")
				for i in range(len(labels)):
					labels[i] = labels[i].text
					values[i] = values[i].text
					labels[i] = to_string(labels[i])
					values[i] = to_string(values[i])
					r[labels[i]] = values[i]

			div = inner_div.find("div",id="otherDetailsDiv")
			if div:
				#other details
				labels = div.find_all("div",class_="label")
				values = div.find_all("div",class_="value")
				for i in range(len(labels)):
					labels[i] = labels[i].text
					values[i] = values[i].text
					labels[i] = to_string(labels[i])
					values[i] = to_string(values[i])
					r[labels[i]] = values[i]

		d.append(r)

	if div5:
		if len(div5)>=1:
			#premium questions answered
			a = div5[0].find("a",class_="moreAnchor")
			if a:
				page_url = "http://www.healthcaremagic.com" + a.get('href')
				continue_extraction = True
				while continue_extraction:
					try:					
						next_page = get_questions(page_url,0)
						if next_page == None:
							continue_extraction = False
						else:
							page_url = next_page
					except Exception, e:
						logger.error('Error on page %s',
							"http://www.healthcaremagic.com" + a.get('href'))
						logger.error('Falied to run get_questions [premium questions]',
							exc_info=True)
			else:
				inner_divs = div5[0].find_all("div",class_="queriesBox")
				for inner_div in inner_divs:
					q = []
					a = inner_div.find("a",class_="smallTitle")
					title = a.get('title')
					q.append(title)

					url = "http://www.healthcaremagic.com" + a.get('href')
					url = to_string(url)
					q.append(url)

					match = re.search(r'/([\d]+)',url)
					if match:
						match = match.group(1)
						number = match
						number = to_number(number)
						q.append(number)

					writePQ.writerow(q)
					del q
		
		if len(div5)==2:
			#public questions answered
			a = div5[1].find("a",class_="moreAnchor")
			if a:
				continue_extraction = True
				page_url = "http://www.healthcaremagic.com" + a.get('href')
				while continue_extraction:
					try:
						next_page = get_questions(page_url,1)
						if next_page == None:
							continue_extraction = False
						else:
							page_url = next_page
					except Exception, e:
						logger.error('Error on page %s',
							"http://www.healthcaremagic.com" + a.get('href'))
						logger.error('Failed to get_questions [public questions]',
							exc_info=True)
			else:
				inner_divs = div5[1].find_all("div",class_="queriesBox")
				for inner_div in inner_divs:
					q = []
					a = inner_div.find("a",class_="smallTitle")
					title = a.get('title')
					q.append(title)

					url = "http://www.healthcaremagic.com" + a.get('href')
					url = to_string(url)
					q.append(url)

					match = re.search(r'/([\d]+)',url)
					if match:
						match = match.group(1)
						number = match
						number = to_number(number)
						q.append(number)

					writePFQ.writerow(q)
					del q
		
	if div6:
		#other related questions
		inner_divs = div6.find_all("div",class_="FullDiv linePadding5 borderBottom")
		for inner_div in inner_divs:
			a = inner_div.find("a")
			title = a.string
			title = to_string(title)
			d.append(title)
			
			url = "http://www.healthcaremagic.com" + a.get('href')
			url = to_string(url)
			d.append(url)
			
			match = re.search(r'/([\d]+)',url)
			if match:
				match = match.group(1)
				number = match
				number = to_number(number)
				d.append(number)
	
	write.writerow(d)
	del d

#this code creates a file doctorsInfo.csv and stores all the information retrived
file = open('doctorsInfo.csv','wb')
write = csv.writer(file,delimiter=",")

#this code opens the doctors.csv file and retrives previously stored information
file = open('doctors.csv','rb')
read = csv.reader(file)

for row in read:
	try:
		#this creates separate files for premium and public forum questions answered by the doctor
		pqFile = row[0]+'-'+row[3]+'-'+'premiumQuestions'+'.csv'
		pfqFile = row[0]+'-'+row[3]+'-'+'publicQuestions'+'.csv'
		pq = open(pqFile,'wb')
		pfq = open(pfqFile,'wb')
		writePQ = csv.writer(pq,delimiter=",")	
		writePFQ = csv.writer(pfq,delimiter=",")	
		
		get_values(row[2])
		pq.close()
		pfq.close()

	except Exception, e:
		logger.error('Error on page %s',row[2])
		logger.error('Failed to get_values',exc_info=True)
	r.clear()

write.close()