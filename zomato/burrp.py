import requests
import time
import sqlite3
from itertools import count
import re
import os
import urllib2
from bs4 import BeautifulSoup
base_url = "http://www.burrp.com"

rest_name = " "
rest_url = " "
address = " "
region = " "
location = " "
votes = " "
operating_hours = " "
budget  = " "
rest_counter = 0
rating = 0.0
coords = 0.0
food_rating = 0.0
service_rating = 0.0
ambience_rating = 0.0
value_rating = 0.0
music_rating = 0.0
feats = []
cuisines = []
#global counter

conn = sqlite3.connect('burrp_chennai1.db')

def burrp_spider(city, max_pages):
	
	print 'Inside burrp_spider function'
	DIR = "/Users/subashgandyer/Desktop/Projects/Yoday/FlaskApp/scraper/burrp/"
	sleep_counter = 0
	page = 53
	rest_counter = 1040	
	global counterid
	while page <= max_pages:
		if sleep_counter != 20:
			url = "http://www.burrp.com/"+city+"/search.html?q=restaurants&page="+str(page)
			source_code = requests.get(url)
			plain_text = source_code.text
			soup = BeautifulSoup(plain_text)
			for link in soup.findAll('h1',{'class':'lead-heading'}):
				print 'Extracted full link === ', link
				
				# Restaurant_Name = link.string			
				# print 'Restaurant Name = ', Restaurant_Name
				
				href = link.find('a')			
				Restaurant_URL = base_url + href.get('href')
				Restaurant_Name = href.string
				print 'Restaurant Name = ', Restaurant_Name
				print 'Restaurant link = ', Restaurant_URL
				
				rest_counter += 1
				get_restaurant_information(Restaurant_URL, Restaurant_Name, rest_counter)

				#get_menu_information(Restaurant_URL, Restaurant_Name, rest_counter, counterid)


				#get_images(Restaurant_URL, Restaurant_Name)

			page += 1
			sleep_counter += 1
		else:
			sleep_counter = 0
			time.sleep(3)



def get_images(rest_url, rest_name):
	print rest_url, rest_name
	DIR = "/Users/subashgandyer/Desktop/Projects/Yoday/FlaskApp/scraper/burrp/"
	cnt = 0
	source_code = requests.get(rest_url)
	plain_text = source_code.text
	soup = BeautifulSoup(plain_text)
	
	try:
	    os.makedirs(rest_name)
	except OSError:
	    if os.path.isdir(rest_name):
	        # We are nearly safe
	        pass
	    else:
	        # There was an error on creation, so make sure we know about it
	        raise

	for imagelink in soup.findAll('div',{'class':'gallery-pane'}):
		#print imagelink
		for data in imagelink.findAll('a',{'class':'idsclass'}):
			images = data.get('href')
			print images
			cnt += 1
			raw_img = urllib2.urlopen(images).read()
			save_path = os.path.expanduser('~/Desktop/Projects/Yoday/FlaskApp/scraper/burrp/'+rest_name+'/')
			print save_path
			completeName = os.path.join(save_path)
			print completeName
			f = open(completeName+rest_name+"_"+str(cnt)+".jpg", 'wb')
			f.write(raw_img)
			f.close()
		
			print ' Done data printing ... '
			print ' '
			print ' '

def get_restaurant_information(rest_url, rest_name, rest_counter):
	print rest_url
	operating_hours = " "
	location = ''
	budget = ''
	coords = 0.0
	votes = 0
	cuisines_list = []
	feats_list = []
	address = '	'
	feats = []
	food_rating = 0.0
	service_rating = 0.0
	ambience_rating = 0.0
	music_rating = 0.0
	value_rating = 0.0 
	source_code = requests.get(rest_url)
	plain_text = source_code.text
	soup = BeautifulSoup(plain_text)
	for link in soup.findAll('div',{'class':'rattingBlock'}):
		for rating_link in link.find('div',{'class':'badge'}):
			rating = rating_link.string
			print 'Rating = ', rating
		votes_list = []
		if (not link):
			for votes_link in link.find('span',{'itemprop':'ratingCount'}):
				votes = votes_link.string
				print 'Votes = ', votes
				votes_list.append(votes)



	for name_link in soup.findAll('div',{'class':'rest_ino_head_sect'}):
		print 'Name' ,name_link
		for logo_link in name_link.findAll('span',{'class':'rest_logo_box'}):
			logo_image = [a['src'] for a in name_link.findAll("img", {"src": re.compile("burrpimg.com")})]
			print logo_image
			# for img in logo_image:
			# 	raw_img = urllib2.urlopen(img).read()
			# 	f = open(rest_name+"_logo.jpg", 'wb')
			# 	f.write(raw_img)
			# 	f.close()

		for address_link in name_link.findAll('span',{'itemprop':'addressLocality'}):
			location = address_link.find('a').string
			print 'Location = ', location

		for address_region in name_link.findAll('span',{'itemprop':'addressRegion'}):
			region = address_region.find('a').string
			print 'Region = ', region


	for addresss in soup.findAll('div',{'class':'bar'}):
		address = addresss.string
		print 'Address = ', address

	for coordss in soup.findAll('a', {'class':'btn-map'}):
		coords = coordss.get('href')
		print 'Co-ordinates = ', coords

	
	for operating_hourss in soup.findAll('div', {'class':'bordered-box'}):
		operating_hours = operating_hourss.string
		if operating_hours:
			print 'Operating hours = ', operating_hours
		else:
			operating_hours = "No data found"
	# except:
	# 	print 'Caught the exception in operating_hours'

	for Budget in soup.findAll('span',{'itemprop':'priceRange'}):
		budget = Budget.string
		print 'Budget = ', budget


	cuisines_list = ""
	for cuisines in soup.findAll('span',{'itemprop':'servesCuisine'}):
		print cuisines
		cuisine = cuisines.findAll('a')
		print cuisine
		for cuis in cuisine:
			cuisine = cuis.string
			#cuisines_list.append(cuisine)
			print 'Cuisine(s) = ', cuisine
			cuisines_list = cuisines_list +'#'+ cuisine
		
		print cuisines_list

	# for recoss in soup.findAll('div',{'class':'tab-pane'}):
	# 	recos = recoss.string
	# 	print "Recommendations = ", recos

	feats_list = ""
	print 'Features in this restaurant \n'
	for features in soup.findAll('div',{'class':'rest_feat'}):
		features = features.select('span')
		for feat in features:
			feats = feat.string
			print feats
			#feats_list.append(feats)
			feats_list = feats_list +'#'+feats

	print feats_list
	rating = 0.0
	cnt = 0
	ratings_list = []
	for ratingss in soup.findAll('div',{'class':'sum_cell'}):
		for ratings in ratingss.select('input'):
			
			rates = ratings.get('value')
			print rates
			ratings_list.append(rates)
			if cnt == 0:
				food_rating = rates
				print 'food_rating:', food_rating
			elif cnt == 1:
				service_rating = rates
				print 'service_rating:', service_rating
			elif cnt == 2:
				ambience_rating = rates
				print 'ambience_rating: ', ambience_rating
			elif cnt == 3:
				music_rating = rates
				print 'music_rating : ', music_rating
			elif cnt == 4:
				value_rating = rates
				print 'value_rating :', value_rating

			cnt += 1

	print ' '
	print ' '
	print ' '
	print "Printing all the values in the console before inserting to the database ...... "
	print 'Restaurant Number : ',rest_counter
	print 'Restaurant Name : ', rest_name
	if rating:
		print 'Rating : ', rating
	else:
		rating = 0.0
	if votes:
		print 'Votes : ', votes_list
	else:
		votes_list = 0
	if location:
		print 'Location : ', location
	else:
		location = ''
	if address:
		print 'Address : ', address
	else:
		address = ''
	if operating_hours:
		print 'Operating Hours : ', operating_hours
	else:
		operating_hours = "No data found"
	if coords:
		print 'Co-ordinates : ', coords
	else:
		coords = ''
	if budget:
		print 'Budget : ', budget
	else:
		budget = ''
	if cuisines_list:
		print 'Cuisine(s) : ', cuisines_list
	else:
		cuisines_list = ''
	if feats_list:
		print 'Feature(s) : ', feats_list
	else:
		feats_list = 'No data found'
	#if ratings_list:
	
	# try:
	# 	if len(ratings_list[0])!=0:
	# 		print 'Food Rating : ', ratings_list[0]
	# 		food_rating = ratings_list[0]
	# except (IndexError, ValueError):
	# 	food_rating = 0.0 
	# try:
	# 	if len(ratings_list[1])!=0:
	# 		print 'Service Rating : ', ratings_list[1]
	# 		service_rating = ratings_list[1]
	# except (IndexError, ValueError):
	# 	service_rating = 0.0 
	# try:
	# 	if len(ratings_list[2])!=0:
	# 		print 'Ambience Rating : ', ratings_list[2]
	# 		ambience_rating = ratings_list[2]
	# except (IndexError, ValueError):
	# 	ambience_rating = 0.0 
	# try:
	# 	if len(ratings_list[3])!=0:
	# 		print 'Music Rating : ', ratings_list[3]
	# 		music_rating = ratings_list[3]
	# except (IndexError, ValueError):
	# 	music_rating = 0.0 
	# try:
	# 	if len(ratings_list[4])!=0:
	# 		print 'Value Rating : ', ratings_list[4]
	# 		value_rating = ratings_list[4]
	# except (IndexError, ValueError):
	# 	value_rating = 0.0 

	



	# if len(ratings_list) !=0:
	# 	for i in range(len(ratings_list)):
	# 		if ratings_list[i]:
	# 			if i==0:
	# 				food_rating = ratings_list[i]
	# 			else:
	# 				food_rating = 0.0
	# 			if i==1:
	# 				service_rating = ratings_list[i]
	# 			else:
	# 				service_rating = 0.0
	# 			if i==2:
	# 				ambience_rating = ratings_list[i]
	# 			else:
	# 				ambience_rating = 0.0
	# 			if i==3:
	# 				music_rating = ratings_list[i]
	# 			else:
	# 				music_rating = 0.0
	# 			if i==4:
	# 				value_rating = ratings_list[i]
	# 			else:
	# 				value_rating = 0.0
	


	# if ratings_list[0]:
	# 	if len(ratings_list[0])!=0:
	# 		print 'Food Rating : ', ratings_list[0]
	# 		food_rating = ratings_list[0]
	# else: 
	# 	food_rating = 0.0 
	# if ratings_list[1]:
	# 	if len(ratings_list[1])!=0:
	# 		print 'Service Rating : ', ratings_list[1]
	# 		service_rating = ratings_list[1]
	# else:
	# 	service_rating = 0.0 
	# if ratings_list[2]:
	# 	if len(ratings_list[2])!=0:
	# 		print 'Ambience Rating : ', ratings_list[2]
	# 		ambience_rating = ratings_list[2]
	# else:
	# 	ambience_rating = 0.0 
	# if ratings_list[3]:
	# 	if len(ratings_list[3])!=0:
	# 		print 'Music Rating : ', ratings_list[3]
	# 		music_rating = ratings_list[3]
	# else:
	# 	music_rating = 0.0 
	# if ratings_list[4]:
	# 	if len(ratings_list[4])!=0:
	# 		print 'Value Rating : ', ratings_list[4]
	# 		value_rating = ratings_list[4]
	# else:
	# 	value_rating = 0.0 


	# if not food_rating:
	# 	food_rating = 0.0
	# if not service_rating:
	# 	service_rating = 0.0
	# if not ambience_rating:
	# 	ambience_rating = 0.0
	# if not music_rating:
	# 	music_rating = 0.0
	# if not value_rating:
	# 	value_rating = 0.0


	conn.execute("INSERT INTO REST_GENERAL_NEW VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (rest_counter, rest_name,rating, votes_list, location, address, operating_hours, coords, budget, cuisines_list, feats_list, food_rating, service_rating, ambience_rating, music_rating, value_rating))

	conn.commit()
	#conn.close()


def get_menu_information1(rest_url, rest_name):
	print rest_url
	source_code = requests.get(rest_url)
	plain_text = source_code.text
	soup = BeautifulSoup(plain_text)
	link = soup.findAll('div',{'id':'search_cont'})
	#print link
	for dish_cat in link:
		#print dish_cat
		if dish_cat != None:
			dish_cats = dish_cat.find('h1')
			#print dish_cats
			if dish_cats != None:
				dish_cats = dish_cats.find('span').string
				#dish_cat = dish_cat.string
				print 'MENU CATEGORY \n', dish_cats

				#for i in link:
				for menu_link in dish_cat.findAll('div',{'class':'menu_con'}):
					#print a
					for menu_item in menu_link.findAll('div',{'class':'menu_item'}):
						#print b
						for menu in menu_item.findAll('div',{'class':'item_name'}):
							menu = menu.find('span').string
							print menu
						for price in menu_item.findAll('div',{'class':'item_price'}):
							price = price.find('span').string
							print price
		

def get_menu_information(rest_url, rest_name, rest_counter, counterid):
	print rest_url
	menu_cat_lists = []
	source_code = requests.get(rest_url)
	plain_text = source_code.text
	soup = BeautifulSoup(plain_text)
	h1link = soup.findAll('h1',{'class':'menu_trig'})
	#print type(h1link), len(h1link[0])
	#print h1link
	print ' '
	print ' '
	print ' '
	print ' '

	if h1link:
		for data in h1link:
			print data
			menu_cat = data.select('span')[0].string
			print menu_cat
			menu_cat_lists.append(menu_cat)


		print 'Printing Menu Cateogries ....'
		print menu_cat_lists
	

	h2link = soup.findAll('div',{'class':'menu_con'})
	#print type(h2link), len(h2link)
	#print h2link
	print ' '
	print ' '
	print ' '
	print ' '

	if h2link:
		for data in h2link:
			print data
			menu_item = data.select('span')[0].string
			print menu_cat
			menu_cat_lists.append(menu_cat)


		print 'Printing Menu Cateogries ....'
		print menu_cat_lists
	

	link = soup.findAll('div',{'id':'search_cont'})
	#print link
	menu_list = []
	
	for dish_cat in link:
		print dish_cat
		if dish_cat != None:
			dish_cats = dish_cat.find('h1')
			#print dish_cats
			if dish_cats != None:
				dish_cats = dish_cats.find('span').string
				menu_list.append(dish_cats)
				#dish_cat = dish_cat.string
				#print 'MENU CATEGORY \n', dish_cats

				#for i in link:
				main_menu_lists = []
				menu_cat_list = []
				menu_cat_counter = 0
				for menu_link in dish_cat.findAll('div',{'class':'menu_con'}):
					
					print 'Category Menu = ', menu_cat_lists[menu_cat_counter]
					#menu_cat_list = []
					main_menu_list = []
					for menu_item in menu_link.findAll('div',{'class':'menu_item'}):	
						menu_item_list = []
						for menu in menu_item.findAll('div',{'class':'item_name'}):
							menus = menu.find('span').string
							desc = menu.find('div').string.strip()
							print menus
							print desc
							menu_item_list.append(menus)
							menu_item_list.append(desc)
						for price in menu_item.findAll('div',{'class':'item_price'}):
							price = price.find('span').string
							print price
							menu_item_list.append(price)
							print 'Printing Menu Items .....'
							print menu_item_list
							main_menu_list.append(menu_item_list)
						

						print 'Printing the values of menu items'
						print ' '
						print ' '
						print ' '

						print 'Rest_Count : ', rest_counter
						print 'Rest Name : ', rest_name
						print 'Menu Category : ', menu_cat_lists[menu_cat_counter]
						print 'Menu Item Name : ', menus
						print 'Menu Description : ', desc
						print 'Menu Price : ', price
						if menus:
							print 'Menus : ', menus
						else:
							menus = 'No data found'


						if desc:
							print 'Description : ', desc
						else:
							desc = 'No data found'

						if price:
							print 'Price : ', price
						else:
							price = 0.0


						counterid += 1
						conn.execute("INSERT INTO REST_MENU VALUES (?, ?, ?, ?, ?, ?, ?)",(counterid,rest_counter, rest_name, menu_cat_lists[menu_cat_counter], menus,desc,price))

					print 'Main Menu List --- Second stage list\n', main_menu_list
					menu_cat_list.append(main_menu_list)
					menu_cat_counter += 1
					
				print 'FULL MENU LIST \n', menu_cat_list
				

	print 'Menu Categories LIST\n', menu_cat_lists	
	

	conn.commit()
	#conn.close()
		

def main():
	
	global sleep_counter
	global DIR
	global counterid
	counterid = 61
	print 'Starting to scrape Burrp !!!!'

	
	print "Opened database successfully"

	# conn.execute('''CREATE TABLE RATINGS
	#        (ID INT PRIMARY KEY     NOT NULL,
	#        RES_NAME       TEXT    NOT NULL,
	#        RES_ID 		  INT  	  NOT NULL,
	#        DISH_NAME      TEXT     NOT NULL,
	#        SENTIMENT      CHAR(10)  NOT NULL)''')
	# print "Table created successfully"

	# conn.execute('''DROP TABLE IF EXISTS REST_GENERAL_NEW''')

	# conn.execute('''CREATE TABLE REST_GENERAL_NEW
	#        (ID 				INT 		NOT NULL,
	#        RES_NAME       	TEXT   		NOT NULL,
	#        RATINGS			REAL,	
	#        VOTES 			INTEGER,
	#        LOCATION      	TEXT,
	#        ADDRESS 			TEXT,
	#        OPERATING_HOURS 	TEXT,
	#        COORDS 			TEXT,
	#        BUDGET 			TEXT,
	#        CUISINES 		TEXT,
	#        FEATURES 		TEXT,
	#        FOOD_RATING 		REAL,
	#        SERVICE_RATING 	REAL,
	#        AMBIENCE_RATING 	REAL,
	#        MUSIC_RATING 	REAL,
	#        VALUE_RATING 	REAL)''')
	# print "Table created successfully"
	conn.commit()

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
	
	burrp_spider('chennai', 89)

	conn.close()






if __name__ == '__main__':
	main()
