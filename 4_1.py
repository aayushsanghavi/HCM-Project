import re
import csv
import logging
from urllib import request
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
handler = logging.FileHandler('logfile_4_1.log')
logger.addHandler(handler)

# retrives the next page url and the data from that page
def get_next_page(page_link):
	page = request.urlopen(page_url).read().decode("utf-8", "ignore")
	soup = BeautifulSoup(page, "html.parser")
	doctor_list = soup.find_all("div", id="singleDiv")
	for doctor in doctor_list:
		doctor_a = doctor.find("a")
		doctor_name = doctor_a.string.strip()
		doctor_url = "http://www.healthcaremagic.com" + doctor_a.get('href')
		doctor_id = doctor_url.split("/")[-1]
		doctor_page = request.urlopen(doctor_url).read().decode("utf-8", "ignore")
		doctor_soup = BeautifulSoup(doctor_page, "html.parser")
		get_doctor_info(doctor_soup, [doctor_name, doctor_url, doctor_id])

	# retrives the url of the next page
	pagination = soup.find("div", id="paginationDiv")
	page_li = pagination.find_all("a", class_="box")
	for li in page_li:
		page_li_url = li.get('href')
		page_li_value = li.string.strip()
		match = re.search(r'Next', page_li_value)
		if match: return "http://www.healthcaremagic.com" + page_li_url
	return None

# retrives the title, url, id, specialisation, number of reviews and location of each doctor
def get_doctor_info(soup, d):
	labels = soup.find_all("div", class_="label")
	values = soup.find_all("div", class_="value")

	for label, value in zip(labels, values):
		v = value.text.strip()
		l = label.text.strip()
		if v and v != "null": d += [l, v]
	write.writerow(d)

# url of the desired webpage
page_url = "http://www.healthcaremagic.com/doctors"
# creates a file doctors.csv and stores all the information retrived
write = csv.writer(open('doctors.csv', 'w'), delimiter=",")
# extracts all the required information from all the pages
while page_url:
	try:
		page_url = get_next_page(page_url)
	except:
		logger.error('Error on page %s',page_url)
		logger.error('Failed to get_next_page',exc_info=True)
