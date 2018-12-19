import re
import sys
import csv
import logging
from datetime import date
from urllib import request
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
handler = logging.FileHandler('logfile_3_3.log')
logger.addHandler(handler)

def get_date():
	today = date.today()
	day = today.strftime("%A")[:3]
	month = today.strftime("%B")[:3]
	return day + ", " + today.strftime("%d") + " " + month + " " + today.strftime("%Y")

def get_values(row):
	question_id, title, page_url = row
	page = request.urlopen(page_url).read().decode("utf-8", "ignore")
	soup = BeautifulSoup(page, "html.parser")

	main_div = soup.find("div", class_="contentwrapper")
	questions = main_div.find_all("div", class_="leftarrow-box")
	answers = main_div.find_all("div", class_="rightarrow-box")
	doc_div = main_div.find("div", class_="doctor-details mt-0")
	inner_spans = doc_div.find_all("span")
	rating_div = doc_div.find("div",class_="innerDiv")

	# posted in category
	category = doc_div.find("a").string.strip()
	# doctor name
	name = doc_div.find("h5").find("a").string.strip()
	# doctor speciality
	speciality = doc_div.find("p").string.strip()
	# doctor practicing since
	practicing = inner_spans[0].text
	# number of questions answered
	answered = re.search(r"\d+", inner_spans[1].text).group()
	# star rating
	stars = re.search(r"\d+", rating_div.get("style")).group()
	stars = int(stars) / 20

	d = [question_id, category, name, speciality, practicing, answered, stars]

	# user acceptance
	acceptance = main_div.find("div", class_="col-lg-8").find("h4").string.strip()
	if "accepted" in acceptance: d.append("Yes")
	else: d.append("No")

	for question, answer in zip(questions, answers):
		# question description
		question_text = question.find("div", class_="card").text.strip()
		# question time
		question_date = question.find("div", class_="userrow").find("span").string.strip()
		if "ago" in question_date: question_date = get_date()
		# answer
		answer_text = answer.find("div",class_="card").text.strip()
		# peer review
		peer = answer.find_all("div", class_="userrow right")[1].find("a").string.strip()
		# answer time
		answer_time = answer.find_all("div", class_="userrow right")[0].find("span").string.strip()
		d += [question_text, question_date, answer_text, peer, answer_time]

	write.writerow(d)

# creates a file premiumAuestions.csv and stores all the answers retrived
write = csv.writer(open('premiumAnswers.csv','w'), delimiter=",")
# opens the premiumQuestions.csv file and retrives information about the premium questions
read = csv.reader(open('premiumQuestions.csv','r'))
for row in read:
	try:
		get_values(row)
	except:
		logger.error('Error on page %s', row[1])
		logger.error('Failed to get_values', exc_info=True)
quit()
