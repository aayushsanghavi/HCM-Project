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
handler = logging.FileHandler('logfile_3_3.log')
logger.addHandler(handler)

#global variables
url = "http://www.healthcaremagic.com"

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

def get_values(page_url):
	d = []
	#opens the requested page
	page = urllib2.urlopen(page_url)
	soup = BeautifulSoup(page,'lxml')
	page.close()
		
	outer_div = soup.find("div",style="float:left; width : 67%;")	
	main_div = outer_div.find("div",style="float:left; width: 100%; font-size: 14px; line-height: 18px; padding-top: 10px;")
	doc_div = main_div.find("div",class_="premiumDocStrip")
	answers = main_div.find_all("div",class_="followupQBox")
	questions = main_div.find_all("div",class_="premiumQBox")
	times = main_div.find_all("span",style="font-size:14px;color:#999;")
	peers = main_div.find_all("a",itemprop="editor")

	#question title
	h1 = outer_div.find("h1",class_="OrangeH1")
	title = h1.string
	title = to_string(title)
	d.append(title)

	#question url
	d.append(page_url)

	#question id
	question_id = re.search(r"\d+",page_url)
	question_id = question_id.group()
	question_id = to_number(question_id)
	d.append(question_id)

	#posted in category
	span = main_div.find("span",class_="premiumTime")
	a = span.find("a")
	category = a.string
	category = to_string(category)
	d.append(category)

	#doctor name
	doc_inner_div = doc_div.find("div",style="width:60%; float:left;line-height:22px; padding-left: 10px;")
	inner_divs = doc_inner_div.find_all("div")
	a = inner_divs[0].find("a")
	name = a.string
	name = to_string(name)
	d.append(name)

	#doctor id
	href = a.get("href")
	doc_id = re.search(r"\d+",href)
	doc_id = doc_id.group()
	doc_id = to_number(doc_id)
	d.append(doc_id)

	#doctor speciality
	span = inner_divs[0].find("span")
	specialist = span.string
	specialist = to_string(specialist)
	d.append(specialist)

	#doctor practicing since
	practicing = inner_divs[1].text
	practicing = re.search(r"\d+",practicing)
	practicing = practicing.group()
	practicing = to_number(practicing)
	d.append(practicing)

	#number of questions answered
	answered = inner_divs[2].text
	answered = re.search(r"\d+",answered)
	answered = answered.group()
	answered = to_number(answered)
	d.append(answered)

	#user rating
	rating = doc_div.find("spna")
	rating = rating.string
	rating = to_string(rating)
	d.append(rating)

	#star rating
	rating = doc_div.find("div",class_="innerDiv")
	style = rating.get("style")
	stars = re.search(r"\d+",style)
	stars = stars.group()
	stars = int(stars)/20
	d.append(stars)

	#user acceptance
	p = main_div.find("p")
	p = p.string
	p = to_string(p)
	yes = re.search(r"accepted",p)
	yes = yes.group()
	if yes == "accepted":
		d.append("Yes")
	else:
		d.append("No")

	j = 0
	for i in range(len(questions)):
		#question description
		question = questions[i].find("div",class_="paragraph")
		question= question.text
		question = to_string(question)
		d.append(question)

		if i>0:
			#question time
			time = times[j].string
			time = to_string(time)
			d.append(time)
			j += 1
		else:
			#posted time
			span = main_div.find("span",class_="premiumTime")
			posted_on = span.find("span")
			posted_on = posted_on.string
			posted_on = to_string(posted_on)
			d.append(posted_on)
			
		#answer
		answer = answers[i].find("div",class_="paragraph")
		answer = answer.text
		answer = to_string(answer)
		d.append(answer)
		
		#peer review
		peer = peers[i].string
		peer = to_string(peer)
		d.append(peer)

		#answer time
		time = times[j].string
		time = to_string(time)
		d.append(time)
		j += 1

	write.writerow(d)
	del d

#opens the premiumQuestions.csv file and retrives information about the premium questions
file1 = open('premiumQuestions.csv','rb')
read = csv.reader(file1)

#creates a file premiumAuestions.csv and stores all the answers retrived
file2 = open('premiumAnswers.csv','wb')
write = csv.writer(file2,delimiter=",")

for row in read:
	page_url = row[1]
	try:
		get_values(page_url)
	except:
		logger.error('Error on page %s',page_url)
		logger.error('Failed to get_values',exc_info=True)

file1.close()
file2.close()
