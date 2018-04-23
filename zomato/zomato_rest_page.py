import requests
import time
import sqlite3
from itertools import count
import re
import os
import urllib2
from bs4 import BeautifulSoup
from urls import urls
base_url = "http://www.zomato.com"


conn = sqlite3.connect('zomato_chennai.db')

def get_soup(url,header):
  return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)))


def zomato_spider_rest_page(url):
	
	print 'Inside zomato_spider_rest_page function'
	DIR = "/Users/subashgandyer/Desktop/Projects/Yoday/FlaskApp/scraper/zomato/"
	sleep_counter = 0
	page = 1
	rest_counter = 1
	global counterid
	#url = "https://www.zomato.com/"+city+"/restaurants?page="+str(page)
	#url = "https://www.zomato.com/chennai/pantry-dor-anna-nagar-east"
	#url = "https://www.zomato.com/chennai/abs-absolute-barbecues-t-nagar"
	print 'Printing URL .....   ', url
	header = {'User-Agent': 'Mozilla/5.0'} 
	soup = get_soup(url,header)
	#print 'Printing soup .....   \n',soup

	phone_txt = soup.find('div',{'id':'resinfo-phone'})
	if phone_txt:
		phone = phone_txt.find('span',{'itemprop':'telephone'})
		if phone:
			phone = phone.string.strip()
			print 'Restaurant Phone = ', phone
		else:
			phone = ''
			print 'Restaurant Phone = ', phone
	else:
		phone = ''
		print 'Restaurant Phone = ', phone



	for link in soup.findAll('div',{'class':'res-info-highlights'}):
		
		#print 'Extracted full link === ', link
		if link:	
			highlights_list = link.findAll('div',{'class':'res-info-feature-text'})
			#print highlights_list
			#print 'Restaurant Highlight(s) = \n'
			if highlights_list:
				highlights = []
				for i in highlights_list:
					highlight = i.string.strip()
					highlights.append(highlight)
				print highlights
				
				highlights = ','.join(highlights)
				print 'Highlights = ', highlights
			else:
				highlights = ''


			known_for_txt = soup.find('div',{'class':'res-info-known-for-text mr5'})
			if known_for_txt:
				known_for = known_for_txt.string.strip()
				print 'Known For =  ', known_for
			else:
				known_for = ''
		else:
			highlights = ''
			known_for = ''



	reco_dishes_txt = soup.find('div',{'class':'res-info-dishes-text order-dishes'})
	if reco_dishes_txt:
		reco_dishes = reco_dishes_txt.string.strip()
		print 'Recommended Dishes =  ', reco_dishes
	else:
		reco_dishes = ''
		print 'Recommended Dishes =  ', reco_dishes


	reviews_txt = soup.findAll('div',{'itemprop':'description'})
	if reviews_txt:
		for reviews1 in reviews_txt:
			reviews = reviews1.text.strip()
			print 'Review  = ', reviews
			if reviews1:
				review_rating = reviews1.findAll('div',{'aria-label':re.compile('Rated')})
				for review in review_rating:
					review_rating = review.get('aria-label')
					print 'Review Rating = ', review_rating
			else:
				review_rating = ''
	else:
		review_rating = ''
		print 'Review Rating = ', review_rating
		


	res_name_txt = soup.find('h1',{'class':'res-name left mb0'})
	if res_name_txt:
		rest_name = res_name_txt.find('a')
		rest_name = rest_name.string.strip()
		print 'Rest Name = ', rest_name
	else:
		rest_name = ''
		print 'Rest Name = ', rest_name


	res_loc_txt = soup.find('div',{'class':'mb5 pt5 clear'})
	if res_loc_txt:
		rest_loc = res_loc_txt.find('a')
		rest_loc = rest_loc.string.strip()
		print 'Rest Location = ', rest_loc
	else:
		rest_loc = ''
		print 'Rest Location = ', rest_loc

	conn.execute("UPDATE REST_INFO SET PHONE_NUMBER=?, HIGHLIGHTS=?, KNOWN_FOR=?, RECO_DISHES=? WHERE RES_NAME=? AND LOCATION=?", (phone, highlights, known_for, reco_dishes, rest_name, rest_loc))
		




def main():
	
	global sleep_counter
	global DIR
	global counterid
	counterid = 1
	print 'Starting to scrape Zomato Restaurant\'s Highlights,  !!!!'

	
	print "Opened database successfully"

	

	#conn.execute('''DROP TABLE IF EXISTS REST_MENU''')
	# conn.execute('''CREATE TABLE REST_MENU
	#        (ID 					INT 	NOT NULL,
	#        RES_COUNTER 			INT 	NOT NULL,
	#        RES_NAME       			TEXT   	NOT NULL,
	#        MENU_CATEGORY_NAME 	  	TEXT,
	#        MENU     				TEXT,
	#        DESCRIPTION				TEXT,
	#        PRICE 					REAL,
	#        PRIMARY KEY(ID, RES_COUNTER, RES_NAME, MENU))''')
	# print "Table created successfully"
	# conn.commit()
	
	# for url in urls:
	# 	zomato_spider_rest_page(url)

	zomato_spider_rest_page('https://www.zomato.com/chennai/paradise-perungudi')
	conn.close()






if __name__ == '__main__':
	main()
