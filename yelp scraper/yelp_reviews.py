import requests
import sqlite3
from bs4 import BeautifulSoup
from review_urls import review_urls
import time
import random
import urllib2
import unicodedata

name=[]
rating=[]
address=[]
budget=[]
cusine=[]
review=[]
phone=[]
nrev=[]
j=0
page_count = 1
rest_count = 1
review_count = 1
npages = 1
rcount = 1
nextPageFlag = True

ob=sqlite3.connect("San_Mateo_reviews.db")
#ob.execute("DROP TABLE IF EXISTS Reviews")
#ob.execute('''CREATE TABLE Reviews (COUNTER TEXT,REST_NAME TEXT,REVIEWER_NAME TEXT,REVIEW_RATING TEXT,REVIEW_DATE TEXT,REVIEW_TEXT TEXT);''')

def get_soup(url,header):
  return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)))


def scraper(review_page_url, rcount):
    global nextPageFlag
    
    review_count = rcount
    #url = "https://www.yelp.com/biz/apple-fritter-san-mateo"
    ################review_page_url = "https://www.yelp.com/biz/apple-fritter-san-mateo?start="+str(rcount-1)
    print str(rcount) +'   '+review_page_url
    header = {'User-Agent': 'Mozilla/5.0'} 
    soup = get_soup(review_page_url,header)
    yesmore_txt = soup.find("span",{"class":"pagination-label responsive-hidden-small pagination-links_anchor"})
    print 'YESMORE TEXT =',yesmore_txt
    if yesmore_txt:
        nextPageFlag = True
    else:
        nextPageFlag = False
    print 'YESMORE FLAG =', nextPageFlag
    #print soup

    ### Restaurant Name ###
    rest_name_txt = soup.find("h1",{"class":"biz-page-title"})
    if rest_name_txt:
        rest_name = rest_name_txt.text
        if rest_name:
            rest_name = rest_name.strip()
            if isinstance(rest_name, unicode):
                rest_name = unicodedata.normalize('NFKD', rest_name).encode('ascii', 'ignore')
            else:
                rest_name = rest_name
        else:
            rest_name = ''
    else:
        rest_name = ''
    #print rest_name
        

    for link in soup.find_all("div",{"class":"review review--with-sidebar"}):
        #print link


        ### Reviewer Name ###
        reviewer_name = link.find("a",{"class":"user-display-name"})
        if not reviewer_name:
            reviewer_name = ''
            # url = ''
        else:
            reviewer_name = reviewer_name.text
            
        #print reviewer_name
        


        ### Review Rating ###
        review_rat = link.find("div",{"class":"rating-very-large"})
        if not review_rat:
            review_rating = ''
        else:
            review_rats = review_rat.find("i")
            if review_rats:
                review_rating = review_rats.get("title")
            else:
                review_rating = ''
    
        
        #print review_rating


        ### Review Date ###
        review_date_txt = link.find("span",{"class":"rating-qualifier"})
        if not review_date_txt:
            review_date = ''
        else:
            review_date = review_date_txt.text
            if review_date:
                review_date = review_date.strip()
            else:
                review_date = ''
        
        #print review_date


        ### Review Text ###
        review_txt = link.find("p")
        if not review_txt:
            review_text = ''
        else:
            review_text = review_txt.text
        
        #print review_text


        print '#########'
        print 'Review Count = ', review_count
        print 'Restaurant Name =', rest_name
        print 'Reviewer Name : ',reviewer_name
        print 'Review Rating : ',review_rating
        print 'Review Date : ', review_date
        print 'Review Text : ', review_text
        print ' '
        print ' '

       

        ob.execute("INSERT INTO Reviews(COUNTER,REST_NAME,REVIEWER_NAME,REVIEW_RATING,REVIEW_DATE,REVIEW_TEXT) VALUES (?,?,?,?,?,?)",(review_count,rest_name,reviewer_name,review_rating,review_date,review_text.strip()))
        #rest_count += 1
        review_count += 1
        ob.commit()

       

        
def pageParser(url,rcount):
    global nextPageFlag
    while nextPageFlag:
        print 'New page starting ...  ', nextPageFlag
        review_page_url = url + "?start="+str(rcount-1)
        

        scraper(review_page_url,rcount)
        rcount += 20
        time.sleep(random.randint(2,5))
    
    nextPageFlag = True
    return 0
    

def main():
    global nextPageFlag
    #pages = 1
    rcount = 1
    review_count = 1
    #urls = ['https://www.yelp.com/biz/mi-tequila-restaurant-millbrae','https://www.yelp.com/biz/sweet-and-natural-san-bruno-3','https://www.yelp.com/biz/koi-palace-express-san-francisco-2','https://www.yelp.com/biz/noodles-and-dim-sum-millbrae']
    #urls = ['https://www.yelp.com/biz/all-spice-san-mateo-2','https://www.yelp.com/biz/cobani-gyro-and-kebab-san-mateo','https://www.yelp.com/biz/charm-thai-eatery-san-mateo-2']
   

    for i in range(len(review_urls)):
        rcount = 1
        if isinstance(review_urls[i][0], unicode):
            rest_link = unicodedata.normalize('NFKD', review_urls[i][0]).encode('ascii', 'ignore')
        else:
            rest_link = review_urls[i][0]
        pageParser(rest_link,rcount)
        time.sleep(random.randint(5,10))
        

   

    ob.close()

if __name__ == '__main__':
    main()
