import requests
import time
import sqlite3
from itertools import count
import re
import os
import urllib2
from bs4 import BeautifulSoup
import time
import unicodedata
base_url = "http://www.zomato.com"


conn = sqlite3.connect('zomato_chennai_1.db')

phone_number = ''
highlights = ''
known_for = ''
reco_dishes = ''
coords = ''

def get_soup(url,header):
  return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)))


def get_other_info(url):
	phone = ''
	highlights = ''
	known_for = ''
	reco_dishes = ''
	coords = ''
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


	coordss = []
	coords_txt = soup.find('div',{'id':'res-map-canvas'})
	#print coords_txt
	if coords_txt:
		coords_list = coords_txt.findAll('meta')
		if coords_list:
			for i in coords_list:
				#print i
				coords = i.get('content')
				coordss.append(coords)
			coords = ','.join(coordss)
			print 'Coords =', coords
		else:
			coords = ''
	else:
		coords = ''
		print 'Coords =', coords

	# reviews_txt = soup.findAll('div',{'itemprop':'description'})
	# if reviews_txt:
	# 	for reviews1 in reviews_txt:
	# 		reviews = reviews1.text.strip()
	# 		print 'Review  = ', reviews
	# 		if reviews1:
	# 			review_rating = reviews1.findAll('div',{'aria-label':re.compile('Rated')})
	# 			for review in review_rating:
	# 				review_rating = review.get('aria-label')
	# 				print 'Review Rating = ', review_rating
	# 		else:
	# 			review_rating = ''
	# else:
	# 	review_rating = ''
	# 	print 'Review Rating = ', review_rating
		


	# res_name_txt = soup.find('h1',{'class':'res-name left mb0'})
	# if res_name_txt:
	# 	rest_name = res_name_txt.find('a')
	# 	rest_name = rest_name.string.strip()
	# 	print 'Rest Name = ', rest_name
	# else:
	# 	rest_name = ''
	# 	print 'Rest Name = ', rest_name


	# res_loc_txt = soup.find('div',{'class':'mb5 pt5 clear'})
	# if res_loc_txt:
	# 	rest_loc = res_loc_txt.find('a')
	# 	rest_loc = rest_loc.string.strip()
	# 	print 'Rest Location = ', rest_loc
	# else:
	# 	rest_loc = ''
	# 	print 'Rest Location = ', rest_loc

	return phone, highlights, known_for, reco_dishes, coords



def zomato_spider(city, max_pages):
	
	print 'Inside zomato_spider function'
	DIR = "/Users/subashgandyer/Desktop/Projects/Yoday/FlaskApp/scraper/zomato/"
	sleep_counter = 0
	page = 67
	rest_counter = 2010
	global counterid
	while page <= max_pages:
		if sleep_counter != 5:
			
			url = "https://www.zomato.com/"+city+"/restaurants?page="+str(page)
			print 'Printing URL .....   ', url
			header = {'User-Agent': 'Mozilla/5.0'} 
			soup = get_soup(url,header)
			#print 'Printing soup .....   \n',soup

			for link in soup.findAll('div',{'class':'search-snippet-card'}):
				
				#print 'Extracted full link === ', link

				### Restaurant URL and Name
				rest_name_txt = link.find('a',{'class':'result-title'})
				if rest_name_txt:
					#rest_name = rest_name_txt.string.strip()
					#rest_name1 = rest_name_txt.string.strip()
					#print 'Scraped soup text = \n', rest_name_txt, type(rest_name_txt)
					rest_name_txt1 = rest_name_txt.text.strip()
					
					#print 'Rest name = ', rest_name_txt1, type(rest_name_txt1)
					if isinstance(rest_name_txt1, unicode):
						#rest_name_txt2 = str(rest_name_txt1)
						#decoded_str = rest_name_txt1.decode("windows-1252")          
						#print 'Second = \n', decoded_str
						encoded_str = unicodedata.normalize('NFKD', rest_name_txt1).encode('ascii', 'ignore')
						#encoded_str = rest_name_txt1.encode('ascii', 'ignore')
						#print encoded_str
					#decoded_str = rest_name_txt.string.strip().decode("windows-1252")
					#rest_name = decoded_str.encode("utf8")
					
					# if isinstance(rest_name_txt1, str):
					# 	#print 's is a string object'
					# elif isinstance(rest_name_txt1, unicode):
					#     #print 's is a unicode object'



					rest_name = encoded_str
					#print 'Third = \n', rest_name
					#rest_name = rest_name.string.strip()
					#print rest_name
					if rest_name:
						print ' '
						print ' '
						print 'RESTAURANT # ', rest_counter
						print '----------------'
						print 'Restaurant Name = ', rest_name
					else:
						rest_name = ''
						print 'Restaurant Name = ', rest_name

					rest_link = rest_name_txt.get('href').strip()
					#decoded_str = rest_link.decode("windows-1252")
					#rest_link = decoded_str.encode("utf8")
					
					if isinstance(rest_link, unicode):
						#rest_name_txt2 = str(rest_name_txt1)
						#decoded_str = rest_name_txt1.decode("windows-1252")          
						#print 'Second = \n', decoded_str
						rest_link = unicodedata.normalize('NFKD', rest_link).encode('ascii', 'ignore')
						#encoded_str = rest_name_txt1.encode('ascii', 'ignore')
						#print rest_link
					else:
						rest_link = rest_link

					#rest_link = rest_link.encode('ascii', 'ignore').strip()

					if rest_link:
						
						print 'Restaurant URL = ', rest_link
					else:
						rest_link = ''
						print 'Restaurant URL = ', rest_link

					
				else:
					rest_link = ''
					rest_name = ''

				### Restaurant Location
				location_txt = link.find('a',{'class':'ln24 search-page-text mr10 zblack search_result_subzone left'})
				if location_txt:
					rest_location = location_txt.string
					if rest_location:
						rest_location = rest_location.strip()
						print 'Restaurant Location = ', rest_location
					else:
						rest_location = ''
						print 'Restaurant Location = ', rest_location
				else:
					rest_location = ''
					print 'Restaurant Location = ', rest_location




				### Restaurant Address
				address_txt = link.find('div',{'class':'search-result-address'})
				if address_txt:
					rest_address = address_txt.string
					if rest_address:
						rest_address = rest_address.strip()
						print 'Restaurant Address = ', rest_address
					else:
						rest_address = ''
						print 'Restaurant Address = ', rest_address
				else:
					rest_address = ''
					print 'Restaurant Address = ', rest_address


				### Restaurant Rating
				rating_txt = link.find('div',{'class':'rating-popup'})
				if rating_txt:
					rest_rating = rating_txt.string
					if rest_rating:
						rest_rating = rest_rating.strip()
						print 'Restaurant Rating = ', rest_rating
					else:
						rest_rating = ''
						print 'Restaurant Rating = ', rest_rating
				else:
					rest_rating = ''
					print 'Restaurant Rating = ', rest_rating

				### Restaurant Votes
				votes_txt = link.find('span',{'class':re.compile('rating-votes')})
				if votes_txt:
					rest_votes = votes_txt.string
					if rest_votes:
						rest_votes = rest_votes.strip()
						if rest_votes:
							rest_votes = rest_votes.split(' ')[0]
							print 'Restaurant Votes = ', rest_votes
						else:
							rest_votes = ''
							print 'Restaurant Votes = ', rest_votes
					else:
						rest_votes = ''
						print 'Restaurant Votes = ', rest_votes
				else:
					rest_votes = ''
					print 'Restaurant Votes = ', rest_votes
				
				### Restaurant Reviews
				reviews_txt = link.find('a',{'class':'search-result-reviews'})
				if reviews_txt:
					rest_reviews = reviews_txt.string.strip()
					if rest_reviews:
						rest_reviews = rest_reviews.split(' ')[0]
						print 'Restaurant Reviews = ', rest_reviews
				else:
					rest_reviews = ''
					print 'Restaurant Reviews = ', rest_reviews


				### Getting Cuisines, Cost, Opening hours...
				div_txt = link.find('div',{'class':'search-page-text clearfix row'})
				#print div_txt
				rest_cuisines_txt = div_txt.find('div',{'class':'clearfix'})
				if rest_cuisines_txt:
					cuisines_txt = rest_cuisines_txt.find('span',{'class':'col-s-11 col-m-12 nowrap pl0'})
					#print cuisines_txt
					if cuisines_txt:
						cuisines_list = cuisines_txt.findAll('a')
						#print cuisines_list
						# print 'Restaurant Cuisine(s) = \n'
						cuisines = []
						for i in cuisines_list:
							cuisine = i.string.strip()
							cuisines.append(cuisine)

						#print cuisines
						cuisines = ','.join(cuisines)
						print 'Cuisines = ', cuisines
					else:
						cuisines = ''
						print 'Cuisines = ', cuisines
				else:
					cuisines = ''
					print 'Cuisines = ', cuisines

				budget_txt = div_txt.find('span',{'class':'col-s-11 col-m-12 pl0'})
				if budget_txt:
					rest_budget = budget_txt.string.strip()
					print 'Restaurant Budget = ', rest_budget
					# if rest_budget:
					# 	rest_budget = rest_budget[1:]
					# 	print rest_budget
				else:
					rest_budget = ''
					print 'Restaurant Budget = ', rest_budget


				hours_txt = div_txt.find('div',{'class':'col-s-11 col-m-12 pl0 search-grid-right-text '})
				#print type(hours_txt), hours_txt
				if hours_txt:
					rest_hours = hours_txt.string
					#print rest_hours
					if rest_hours:
						rest_hours = rest_hours.strip()
						print 'Restaurant Operating Hours = ', rest_hours
					else:
						rest_hours = ''
						print 'Restaurant Operating Hours = ', rest_hours
				else:
					rest_hours = ''
					print 'Restaurant Operating Hours = ', rest_hours
				
				rest_id = 'R' + str(rest_counter)
				phone_number = ' '
				known_for = ' '
				reco_dishes = ' '
				rest_coords = ' '
				rest_highlights = ' '


				phone_number, rest_highlights, known_for, reco_dishes, rest_coords = get_other_info(rest_link)

				conn.execute("INSERT INTO REST_INFO(ID, RES_ID, RES_NAME, RATINGS, VOTES, REVIEWS, LOCATION, ADDRESS, OPERATING_HOURS, BUDGET, CUISINES, REST_URL, HIGHLIGHTS, PHONE_NUMBER, KNOWN_FOR, RECO_DISHES, COORDS) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (rest_counter, rest_id, rest_name,rest_rating, rest_votes, rest_reviews, rest_location, rest_address, rest_hours, rest_budget, cuisines, rest_link, rest_highlights, phone_number, known_for, reco_dishes, rest_coords))

				conn.commit()
				rest_counter += 1

			page += 1
			sleep_counter += 1
			
		else:
			sleep_counter = 0
			print 'Sleeeeeeeeeeping for 5 seconds'
			print ' '
			print ' '
			print ' '
			time.sleep(5)


def main():
	
	global sleep_counter
	global DIR
	global counterid
	counterid = 1
	print 'Starting to scrape Zomato !!!!'
	
	print "Opened database successfully"

	# conn.execute('''DROP TABLE IF EXISTS REST_INFO''')

	# conn.execute('''CREATE TABLE REST_INFO
	#        (ID 				INT 			NOT NULL,
	#        RES_ID			TEXT   		NOT NULL,
	#        RES_NAME       	TEXT   		NOT NULL,
	#        RATINGS			TEXT,	
	#        VOTES 			TEXT,
	#        REVIEWS          TEXT,
	#        LOCATION      	TEXT,
	#        ADDRESS 			TEXT,
	#        OPERATING_HOURS 	TEXT,
	#        COORDS 			TEXT,
	#        BUDGET 			TEXT,
	#        CUISINES 		TEXT,
	#        HIGHLIGHTS 		TEXT,
	#        PHONE_NUMBER 	TEXT,
	#        KNOWN_FOR 		TEXT,
	#        RECO_DISHES	 	TEXT,
	#        REST_URL			TEXT,
	#        PRIMARY KEY(ID,RES_ID,RES_NAME,LOCATION))''')
	# print "Table created successfully"
	# conn.commit()

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
	start_time = time.time()
	zomato_spider('chennai', 100)
	end_time = time.time()
	print 'Total time running is .... ', end_time - start_time
	conn.close()






if __name__ == '__main__':
	main()
