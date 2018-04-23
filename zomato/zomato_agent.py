from bs4 import BeautifulSoup
import requests
import re
import urllib2
import os
import time


def get_soup(url,header):
  return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)))


def scraper(city,page):
	#image_type = "Idly"
	# you can change the query for the image  here  
	#query1 = "Idly"
	# query= query1.split()
	# query='+'.join(query)

	# BASE_URL = 'https://www.google.co.in/search?q='+query+'&source=lnms&tbm=isch'

	# BASE_PATH = os.path.join(query1, query1)

	# if not os.path.exists(BASE_PATH):
	# 	os.makedirs(BASE_PATH)

	# url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
	# print url
	# header = {'User-Agent': 'Mozilla/5.0'} 
	# soup = get_soup(url,header)
	# f = open("content.txt",'w')
	# f.write(str(soup))
	# f.close

	url = "https://www.zomato.com/"+city+"/restaurants?pages="+str(page)
	print 'Printing URL .....   ', url
	header = {'User-Agent': 'Mozilla/5.0'} 
	soup = get_soup(url,header)
	# source_code = requests.get(url)
	# print 'Printing source code .....   \n',source_code
	# plain_text = source_code.text
	# print 'Printing Plain text .....   \n', plain_text
	# soup = BeautifulSoup(plain_text)
	print 'Printing soup .....   \n',soup


	#print soup
	#images = [a['src'] for a in soup.find_all("img", {"src": re.compile("gstatic.com")})]
	#image_content1 = soup.find_all("div", {"ou": "rg_meta"})
	#images = soup.select("div rg_meta")


	#print images
	#print type(images)
	#print len(images)
	#print images[0].attrs
	#print image_content1
	#print images

	# dirname = query1

	# try:
	#     os.makedirs(dirname)
	# except OSError:
	#     if os.path.isdir(dirname):
	#         # We are nearly safe
	#         pass
	#     else:
	#         # There was an error on creation, so make sure we know about it
	#         raise

	# cnt = 0

	# for img in images:
	#   while cnt < 1:
	# 	  raw_img = urllib2.urlopen(img).read()
	# 	  #add the directory for your image here 
	# 	  #DIR="D:\subash\scraper\\"+image_type+"\\"
	# 	  # cntr = len([i for i in os.listdir(DIR) if image_type in i]) + 1
	# 	  # print cntr
	# 	  f = open(image_type +".jpg", 'wb')
	# 	  #f = open(DIR + image_type + "_"+ str(cntr)+".jpg", 'wb')
	# 	  f.write(raw_img)
	# 	  f.close()
	# 	  cnt += 1


def main():
	counter = 0
	page = 1
	city = 'chennai'
	#dishes = ['Idly','Dosa','Veg Burger','Chicken Burger','Briyani','Mutton Briyani','Chilly Chicken','Chicken 65']
	
	
	# dirname = 'dishes'

	# try:
	#     os.makedirs(dirname)
	# except OSError:
	#     if os.path.isdir(dirname):
	#         # We are nearly safe
	#         pass
	#     else:
	#         # There was an error on creation, so make sure we know about it
	#         raise

	
	# for i in dishes:
	# 	counter += 1
	# 	if counter == 95:
	# 		print 'Its time to go to sleep for a while'
	# 		time.sleep(2)
	# 		counter = 0
		
	scraper(city,page)

if __name__ == '__main__':
	global counter
	#DIR="D:\subash\scraper\zomato\\"+"dishes"+"\\"
	main()