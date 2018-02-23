import urllib2
from bs4 import BeautifulSoup
from lxml import html
import requests

#CREATED BY : NICHOLAS RIANTO PUTRA, SCRAPE SCHEDULE FROM TIKET.COM
def online_schedule(url):
	#scrape html page
	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page, 'html.parser')
	search_result = soup.find('div', attrs= {'class': 'search-list'})
	schedule_json = []

	#get available schedule
	available_schedule = soup.find_all('tr', attrs={'class': 'item-list '})
	for schedule in available_schedule:
		#get schedule info
		train_name = schedule.find('td', attrs= {'class': 'td1'}).find('div', attrs= {'class': 'h3'}).text.strip()
		departure_time = schedule.find('td', attrs= {'class': 'td2'}).find('div', attrs= {'class': 'h1'}).text.strip()
		arrival_time = schedule.find('td', attrs= {'class': 'td3'}).find('div', attrs= {'class': 'h1'}).text.strip()
		price = schedule.find('td', attrs= {'class': 'td5 td5a'}).find('div', attrs= {'class': 'h3 orange'}).text.strip()
		class_train = schedule.find('td', attrs= {'class': 'td5 td5b'}).find('div', attrs= {'class': 'h4'}).text.strip()
		
		#create dictionary
		temp = {}
		temp['name'] = train_name
		temp['dept_time'] = departure_time
		temp['arr_time'] = arrival_time
		temp['price'] = price
		temp['class'] = class_train
		schedule_json.append(temp)
	return schedule_json
