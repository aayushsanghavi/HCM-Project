import re
import sys
import csv
import logging
from urllib import request
from bs4 import BeautifulSoup

# retrives the next page url and the data from that page
def get_next_page(page_link):
	page = request.urlopen(page_url).read().decode("utf-8", "ignore")
	soup = BeautifulSoup(page, "html.parser")
	div = soup.find("div", style="width:100%; float:left;")
	get_values(div)

	# retrives the url of the next page
	page_li = div.find("div", id="paginationDiv").find_all("a", class_="box")
	for li in page_li:
		page_li_value = li.string.strip()
		page_li_url = li.get('href').strip()
		match = re.search(r'Next', page_li_value)
		if match: return "http://www.healthcaremagic.com" + page_li_url
	return None

# retrives the title, url and number of each category for the specific url
def get_values(content):
	all_div = content.find_all("div",class_="queriesBox")
	for div in all_div:
		inner_div = div.find("div",class_="smallPQIcon")
		title = inner_div.a.string.strip()
		url = "http://www.healthcaremagic.com" + inner_div.a.get('href').strip()
		match = re.search(r'/([\d]+)',url)
		number = match.group(1)
		write.writerow([title, url, number])

page_url = "http://www.healthcaremagic.com/premiumquestions"
write = csv.writer(open('premiumQuestions.csv','w'), delimiter=",")
# extracts all the required information from all the pages
while page_url:
	page_url = get_next_page(page_url)
