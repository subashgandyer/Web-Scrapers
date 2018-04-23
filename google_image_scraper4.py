import urllib
import mechanize
from bs4 import BeautifulSoup
from urlparse import urlparse

def getPic(query):
	try:
		browser = mechanize.Browser()
		print 'First line'
		browser.set_handle_robots(False)
		print 'Second line'

		browser.addheaders = [('User-agent','Mozilla')]
		print 'Third line'

		#htmltext = browser.open("https://www.google.com/search?site=&tbm=isch&source=hp&biw=726&bih=705&q=idly&oq=idly")
		
		htmltext = browser.open("https://www.google.com/search?site=&tbm=isch&source=hp&biw=726&bih=705&q="+query+"&oq="+query)
		print htmltext
		img_urls = []
		soup = BeautifulSoup(htmltext)
		#results = soup.findAll("a")

		results = [a['href'] for a in soup.find_all("a", {"href": re.compile("imgurl")})]
	
		print results

		#results1 = soup.findAll(".rg_meta")

		#print results1
	except:
		print "error"


getPic('idly')
