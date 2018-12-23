import re
import csv
import logging
from urllib import request
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
handler = logging.FileHandler('logfile_2_2.log')
logger.addHandler(handler)

# the main function that retrives the required data
def get_values(data):
	ques_id, title, page_url = data
	page = request.urlopen(page_url).read().decode("utf-8", "ignore")
	soup = BeautifulSoup(page, "html.parser")

	main_div = soup.find("div", class_="contentwrapper")
	outer_div = main_div.find_all("div", class_="col-md-8")[1]
	inner_div = outer_div.find("div", class_="postQuestion")
	viewed_questions_div = main_div.find_all("div", class_="col-md-12")[1]
	related_questions_div = outer_div.find("div", id="relatedpfq")
	recent_questions_div = outer_div.find("div", id="relatedtags")

	# question text
	question = inner_div.find("div", class_="paragraph").text.strip()

	# question tags
	r = {}
	question_related_info = inner_div.find("div", class_="table-responsive")
	if question_related_info:
		rows = question_related_info.find_all("tr")
		for row in rows:
			columns = row.find_all("td")
			topic = columns[0].string.strip()
			tags = [a.string.strip() for a in columns[1].find_all("a")]
			r[topic] = (", ").join(tags)

	d = [ques_id, question, r]

	# also viewed questions
	if viewed_questions_div:
		for question in viewed_questions_div.find_all("li"):
			question_title = question.a.string.strip()
			question_url = "http://www.healthcaremagic.com" + question.a.get('href')
			d += [question_title, question_url]

	# related questions
	if related_questions_div:
		questions = related_questions_div.find_all("div", class_="card")
		for question in questions:
			question_title = question.button.text.strip()
			question_body = question.find("div", class_="media-body").p.string.strip()
			question_url = "http://www.healthcaremagic.com" + question.find_all("a")[-1].get('href')
			d += [question_title, question_body, question_url]

	# recent questions
	if recent_questions_div:
		for question in recent_questions_div.find_all("div", class_="card"):
			question_title = question.button.text.strip()
			question_body = question.find("div", class_="media-body").p.string.strip()
			question_url = "http://www.healthcaremagic.com" + question.find_all("a")[-1].get('href')
			d += [question_title, question_body, question_url]

	# answer content
	answer_divs = main_div.find_all("div", class_="answerWrapper")
	for answer_div in answer_divs:
		answer_info = answer_div.find_all("div", class_="FullDiv")[1]
		# doctor/user answer
		response = answer_info.find("div", class_="card plantfood").text.strip()

		doctor_info = answer_info.find("div", class_="doctorResponse")
		span = doctor_info.find("span", class_="lightBlue")
		# doctor title
		title = doctor_info.span.string.strip()
		# doctor/user name
		name = span.a.string.strip()
		# doctor/user url
		url = "http://www.healthcaremagic.com" + span.a.get('href')
		# doctor/user id
		id = re.search(r'/([\d]+)', url).group(1)

		if "users" in url: d += [response, name, url, id]
		else: d += [response, title, name, url, id]

	write.writerow(d)

# opens the questions.csv file and retrives previously stored information
read = csv.reader(open('categories.csv','r'))
for row in read:
	file = row[0] + " questions.csv"
	questions = csv.reader(open(file, 'r'))
	file = row[0] + " answers.csv"
	write = csv.writer(open(file, 'w'), delimiter=",")
	# creates a temporary file that stores entries which had problems being retrived in the first try
	temp = csv.writer(open('temp.csv','w'), delimiter=",")

	for question in questions:
		try:
			get_values(question[:3])
		except:
			logger.error('Error on page %s', question[2])
			logger.error('Failed to get_values', exc_info=True)
			temp.writerow([question[2]])

	# open temp and run the get_values function again to retrive the lost entries
	questions = csv.reader(open('temp.csv','r'))
	for question in questions:
		try:
			get_values(question[0])
		except:
			logger.error('Error on page %s',question[0])
			logger.error('Failed to get_values',exc_info=True)

quit()
## To note that in very few cases the url causes infinite redirection loops
## Those entries will not be extracted but will be logged.
