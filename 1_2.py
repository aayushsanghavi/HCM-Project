import re
import csv
from urllib import request
from bs4 import BeautifulSoup

def get_next_page(page_link):
	page = request.urlopen(page_url).read().decode("utf-8", "ignore")
	soup = BeautifulSoup(page, "html.parser")
	get_values(soup)

	page_li = soup.find_all("a", class_="box")
	for li in page_li:
		page_li_url = li.get('href')
		page_li_value = li.string.strip()
		match = re.search(r'\D+', page_li_value)
		if match: return "http://www.healthcaremagic.com" + page_li_url
	return None

#this function retrives the title, url and number of each category for the specific url
def get_values(soup):
	ul = soup.find("ul",class_="itemListUL anchorListing")
	all_li = ul.find_all("li")
	for li in all_li:
		title = li.a.string.strip()
		url = "http://www.healthcaremagic.com" + li.a.get('href').strip()
		number = re.search(r'\d+',url).group().strip()
		outfile.writerow([title, url, number])

outfile = csv.writer(open('topics.csv', 'w'), delimiter=",")
webpages = ["disease-and-conditions", "drugs", "treatments","procedures", "lab-tests"]
#this loop extracts all the required information from all the pages of each category
for webpage in webpages:
	page_url = "http://www.healthcaremagic.com/topics/" + webpage
	while page_url:
		page_url = get_next_page(page_url)
quit()
