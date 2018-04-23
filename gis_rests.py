from bs4 import BeautifulSoup
import requests
import re
import urllib2
import os
import time
import csv


def get_soup(url,header):
  return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)))


def scraper(image_type, query1):
	#image_type = "Idly"
	# you can change the query for the image  here  
	#query1 = "Idly"
	query= query1.split()
	query='+'.join(query)

	# BASE_URL = 'https://www.google.co.in/search?q='+query+'&source=lnms&tbm=isch'

	# BASE_PATH = os.path.join(query1, query1)

	# if not os.path.exists(BASE_PATH):
	# 	os.makedirs(BASE_PATH)

	url=url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
	print url
	header = {'User-Agent': 'Mozilla/5.0'} 
	soup = get_soup(url,header)
	f = open("content.txt",'w')
	f.write(str(soup))
	f.close



	
	images = [a['src'] for a in soup.find_all("img", {"src": re.compile("gstatic.com")})]
	


	
	cnt = 0

	for img in images:
	  while cnt < 1:
		  raw_img = urllib2.urlopen(img).read()
		  #add the directory for your image here 
		  #DIR="D:\subash\scraper\\"+image_type+"\\"
		  # cntr = len([i for i in os.listdir(DIR) if image_type in i]) + 1
		  # print cntr
		  f = open(DIR + image_type +".jpg", 'wb')
		  #f = open(DIR + image_type + "_"+ str(cntr)+".jpg", 'wb')
		  f.write(raw_img)
		  f.close()
		  cnt += 1


def main():
	counter = 0
	your_list = []
	
	# with open('cuisine_test.csv', 'rb') as f:
	# 	reader = csv.reader(f)
	
	# your_list = list(reader)
	

	# Jiya fill this your_list with the list of cuisines or restaurant names and run this code
	your_list = [['saravana bhavan'], ['hotel sangeetha'], ['Pantry d\'or']]
	dirname = 'rests'

	try:
	    os.makedirs(dirname)
	except OSError:
	    if os.path.isdir(dirname):
	        # We are nearly safe
	        pass
	    else:
	        # There was an error on creation, so make sure we know about it
	        raise

	
	for i in range(len(your_list)):
		counter += 1
		if counter == 95:
			print 'Its time to go to sleep for a while'
			time.sleep(2)
			counter = 0
		
		scraper(your_list[i][0],your_list[i][0])

if __name__ == '__main__':
	global counter
	global your_list
	DIR="D:\subash\scraper\\"+"rests"+"\\"
	main()