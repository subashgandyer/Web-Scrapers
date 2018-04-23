# import selenium
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium import webdriver
# import os
# import time
# #driver = webdriver.Chrome("C:\\selenium\\webdriver\\chrome\\chromedriver.exe")
# #driver = webdriver.Chrome("/Users/subashgandyer/bin")
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
import selenium
import BeautifulSoup


# # driver.get("https://www.zomato.com")
# driver.maximize_window()

# element1 = '//a[@class= "item default-section-title everyone empty"]'

# driver.find_element_by_xpath(element1).click()

# elements='//div[@class = "load-more bold ttupper tac cursor-pointer fontsize2"]'

# try:
# 	element_present=EC.presence_of_element_located((By.LINK_TEXT,"Load More"))
# 	WebDriverWait(driver,5000).until(element_present)
# 	driver.find_element_by_xpath(elements).click()
# # while(driver.find_element_by_xpath(elements)):
# 	# 	driver.find_element_by_xpath(elements).click()

# 	print 'control came'
# except selenium.common.exceptions.StaleElementReferenceException:
# 	print 'end of load more'
# except selenium.common.exceptions.TimeoutException:
# 	print 'Time out'






# ff = webdriver.Firefox()
# ff.get("https://www.zomato.com/chennai/hotel-saravana-bhavan-anna-nagar-west/reviews") #GoogleImages Link
# try:
#    element = WebDriverWait(ff, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.load-more.bold.ttupper.tac.cursor-pointer.font-size2:first-child')))
# except selenium.common.exceptions.TimeoutException:
# 	print 'Time out'
# finally:
#     ff.quit()
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