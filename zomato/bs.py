from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
import selenium
from bs4 import BeautifulSoup
import re
import time

def load_page(url):
	driver = webdriver.Firefox()
	driver.get(url) #GoogleImages Link
	try:
		element1 = '//a[@class= "item default-section-title everyone empty"]'
		time.sleep(5)
		driver.find_element_by_xpath(element1).click()
		time.sleep(10)
		elements='//div[@class = "load-more bold ttupper tac cursor-pointer fontsize2"]'
		print "about to look for element"
		
		def find(driver):
		    e = driver.find_element_by_xpath(elements)
		    if e:
		    	print 'element found'
		    	while e:
		    		e = driver.find_element_by_xpath(elements)	
		    		time.sleep(0.5)
		    		driver.find_element_by_xpath(elements).click()    	

		    else:
		    	print 'no element'
		        find(driver)
		find(driver)	
	except selenium.common.exceptions.StaleElementReferenceException:
		find(driver)
	except selenium.common.exceptions.TimeoutException:
		print 'Time out'
	except selenium.common.exceptions.NoSuchElementException:
		return driver.page_source
f=open('test.txt','w')
f.write(load_page("https://www.zomato.com/chennai/hotel-saravana-bhavan-anna-nagar-west/reviews").encode("utf-8"))


def reviewParser(reviews_html):
	#soup = BeautifulSoup(open("C:\\example.html"))  # for windows
	#soup = BeautifulSoup(open(r"/Users/subashgandyer/Desktop/Projects/Yoday/FlaskApp/scraper/zomato/test.txt").read())
	soup = BeautifulSoup(open(reviews_html).read())
	# for city in soup.find_all('span', {'class' : 'city-sh'}):
	#     print(city)

	print 'Starting to scrape the reviews .... '

	reviews_txt = soup.findAll('div',{'itemprop':'description'})
	if reviews_txt:
		for reviews1 in reviews_txt:
			reviews = reviews1.text
			if reviews:
				reviews = reviews.strip()
				print 'Review  = ', reviews
			else:
				reviews = ''
				print 'Review  = ', reviews
			if reviews1:
				review_ratings = reviews1.findAll('div',{'aria-label':re.compile('Rated')})
				if review_ratings:
					for review in review_ratings:
						review_rating = review.get('aria-label')
						if review_rating:
							print 'Review Rating = ', review_rating
						else:
							review_rating = ''
							print 'Review Rating = ', review_rating
				else:
					review_rating = ''
					print 'Review Rating = ', review_rating
			else:
				review_rating = ''
				print 'Review Rating = ', review_rating
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

	#### Write to the database now

	return rest_name, rest_loc, reviews_txt, review_rating


def main():
	print ' Starting to scrape the reviews ...'
	for url in urls:
		reviews_html=load_page(url)
		rname, rloc, rtxt, rrating = reviewParser(reviews_html)
		print 'Ending the scraper for reviews'
	return 0

if __name__ == '__main__':
	main()