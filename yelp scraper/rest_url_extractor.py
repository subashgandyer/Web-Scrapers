import requests
import sqlite3
from bs4 import BeautifulSoup
import urllib2
import time
import random

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
pcount = 1

ob=sqlite3.connect("San_Mateo_urls.db")
#ob.execute("DROP TABLE IF EXISTS URLS")
#ob.execute('''CREATE TABLE URLS (COUNTER TEXT,NAME TEXT,RATING TEXT,REVIEWS TEXT,ADDRESS TEXT,PHONE TEXT,BUDGET TEXT,CUISINE TEXT, URL TEXT);''')
 

def get_soup(url,header):
  return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)))


def scraper(review_page_url,pcount,rest_count):
    # rest_count = (pcount-1+1) * 10 + 1
    # print rest_count
    #r=requests.get("https://www.yelp.com/search?find_loc=San+Mateo,+CA,+United+States&start=450")
    #review_page_url = "https://www.yelp.com/search?find_desc=Restaurants&find_loc=San+Mateo,+CA,+United+States&start="+str(rcount-1))
    # https://www.yelp.com/search?find_desc=Restaurants&find_loc=San+Mateo,+CA,+United+States&start=10
    # print r
    # soup=BeautifulSoup(r.content,"lxml")
    #print soup

    header = {'User-Agent': 'Mozilla/5.0'} 
    soup = get_soup(review_page_url,header)

    for link in soup.find_all("div",{"class":"biz-listing-large"}):
        #print link


        name = link.find("a",{"class":"biz-name js-analytics-click"})
        if not name:
            names = ''
            url = ''
        else:
            names = name.text
            if names:
                urls = name.get('href')
                if urls:
                    url = 'https://www.yelp.com' + urls
                else:
                    url = ''
            else:
                url = ''

        # if len(url) > 100:
        #     pcount -= 1
        #     continue
        #print names
        #print url


        revcount = link.find("span",{"class":"review-count rating-qualifier"})
        if not revcount:
            nreviews = ''
        else:
            nreviews = revcount.text
            if nreviews:
                nreviews = nreviews.strip()
            else:
                nreviews = ''
        #print nreviews

        
        rat = link.find("i")
        if not rat:
            ratings = ''
        else:
            ratings = rat.get("title")
        #print ratings

        cuisines_list = []
        cus = link.find("span",{"class":"category-str-list"})
        if not cus:
            cuisines = ''
        else:
            cuisines_txt = cus.findAll("a")
            if cuisines_txt:
                for i in cuisines_txt:
                    cuisi = i.string
                    if cuisi:
                        cuisine = cuisi.strip()
                        cuisines_list.append(cuisine)
                    else:
                        cuisines = ''
                cuisines = ','.join(cuisines_list)

            else:
                cuisines = ''

        #print cuisines


        adr = link.find("address")
        if not adr:
            address = ''
        else:
            address = adr.text
            if address:
                address = address.strip()
            else:
                address = ''
        #print address


        bud = link.find("span",{"class":"business-attribute price-range"})
        if not bud:
            budget = ''
        else:
            budget = bud.text
        #print budget



        ph = link.find("span",{"class":"biz-phone"})
        if not ph:
            phone = ''
        else:
            phone = ph.text
            if phone:
                phone = phone.strip()
            else:
                phone = ''  
        #print phone

        

        print '#################'
        print ' Restaurant # '+str(pcount)
        print '#################'
        print 'Name : ',names
        print 'Rating : ',ratings
        print 'Reviews :', nreviews
        print 'Cuisine : ', cuisines
        print 'Address : ', address
        print 'Budget : ', budget
        print 'Phone : ', phone
        print 'URL :', url
        print ' '
        print ' '
        # print 'Reviews : ',revs
        # print 'No. of Reviews :', norevs
        #ob.execute("INSERT INTO Rests(COUNTER,NAME,CUISINE,RATING,ADDRESS,PHONE,BUDGET,URL) VALUES (?,?,?,?,?,?,?,?)",(rest_count,names,cuisines.strip(),ratings,address.strip(),phone.strip(),budget,url))

        ob.execute("INSERT INTO URLS(COUNTER,NAME,CUISINE,RATING,REVIEWS,ADDRESS,PHONE,BUDGET,URL) VALUES (?,?,?,?,?,?,?,?,?)",(pcount,names,cuisines,ratings,nreviews,address,phone,budget,url))
        pcount += 1
        rest_count += 1
        ob.commit()


def main():
    pages = 100
    pcount = 61
    rest_count = 62
    #link_count = 1
    #global pcount
    # for page in range(pages):
    #     scraper(page+1)
    #     page += 10
    pagecount = 1
    
    for page in range(pages):
        if pagecount > 2:
            time.sleep(random.randint(4,10))
            print ' Sleeping for a long time .... '
            pagecount = 1
        review_page_url = "https://www.yelp.com/search?find_desc=Restaurants&find_loc=San+Mateo,+CA,+United+States&start="+ str(pcount-1)
        scraper(review_page_url,pcount,rest_count)
        pcount += 10
        rest_count += 10
        pagecount += 1
    
    ob.close()

if __name__ == '__main__':
    main()
