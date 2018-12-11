import re
import csv
from urllib import request
from bs4 import BeautifulSoup

categories = []
page_url = "http://www.healthcaremagic.com/community"
page = request.urlopen(page_url).read().decode("utf-8", "ignore")
soup = BeautifulSoup(page, "html.parser")
div = soup.find("div", class_="linePadding7")

categories_a = div.find_all("a", class_="questionTitle")
for category_a in categories_a:
    title = category_a.string.strip()
    url = "http://www.healthcaremagic.com" + category_a.get('href').strip()
    number = re.search(r'\d+', url).group()
    categories.append([title, url, number])

#this segment of code retrives the number of questions asked in the category
categories_span = div.find_all("span", style="display: block;font-size:10px; color:#999;")
for i, category_span in enumerate(categories_span):
    questions = category_span.string.strip()
    number = re.search(r'\d+',questions).group()
    categories[i].append(number)

#this code creates a file categories.csv and stores all the information retrived
write = csv.writer(open('categories.csv','w'), delimiter=",")
for category in categories:
	write.writerow(category)
