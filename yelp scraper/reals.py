import requests
import sqlite3
from bs4 import BeautifulSoup

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

ob=sqlite3.connect("San_Mateo_reals.db")
ob.execute("DROP TABLE IF EXISTS Rests1")
ob.execute('''CREATE TABLE Rests1 (COUNTER TEXT,NAME TEXT,RATING TEXT,ADDRESS TEXT,PHONE TEXT,BUDGET TEXT,CUISINE TEXT, URL TEXT);''')
 

def scraper(i):
    rest_count = (i-1+1) * 10 + 1
    print rest_count
    #r=requests.get("https://www.yelp.com/search?find_loc=San+Mateo,+CA,+United+States&start=450")
    r=requests.get("https://www.yelp.com/search?find_desc=Restaurants&find_loc=San+Mateo,+CA,+United+States&start=0")
    # https://www.yelp.com/search?find_desc=Restaurants&find_loc=San+Mateo,+CA,+United+States&start=10
    print r
    soup=BeautifulSoup(r.content,"lxml")
    #print soup
    for link in soup.find_all("div",{"class":"biz-listing-large"}):
        #print link


        name = link.find("a",{"class":"biz-name js-analytics-click"})
        if not name:
            names = ''
            url = ''
        else:
            names = name.text
            url = name.get('href')
            url = 'https://www.yelp.com' + url 
        print names
        print url


        
        rat = link.find("i")
        if not rat:
            ratings = ''
        else:
            ratings = rat.get("title")
        print ratings

        cus = link.find("span",{"class":"category-str-list"})
        if not cus:
            cuisines = ''
        else:
            cuisines = cus.text
        print cuisines


        adr = link.find("address")
        if not adr:
            address = ''
        else:
            address = adr.text
        print address


        bud = link.find("span",{"class":"business-attribute price-range"})
        if not bud:
            budget = ''
        else:
            budget = bud.text
        print budget



        ph = link.find("span",{"class":"biz-phone"})
        if not ph:
            phone = ''
        else:
            phone = ph.text  
        print phone

        # rev = link.find("p",{"class":"snippet"})
        # print rev, type(rev)
        # if not rev:
        #     revs = ' '
        # else:
        #     revs = rev.text
        # print revs

        # revs = link.find("span",{"class":"review-count rating-qualifier"})
        # norevs = revs.text
        # if norevs == '':
        #     norevs = ''
        # print norevs


        print 'Name : ',names
        print 'Rating : ',ratings
        print 'Phone : ', phone
        print 'Cuisine : ', cuisines
        print 'Address : ', address
        print 'Budget : ', budget
        print 'Phone : ', phone
        print 'URL :', url
        # print 'Reviews : ',revs
        # print 'No. of Reviews :', norevs
        #ob.execute("INSERT INTO Rests(COUNTER,NAME,CUISINE,RATING,ADDRESS,PHONE,BUDGET,URL) VALUES (?,?,?,?,?,?,?,?)",(rest_count,names,cuisines.strip(),ratings,address.strip(),phone.strip(),budget,url))

        ob.execute("INSERT INTO Rests1(COUNTER,NAME,CUISINE,RATING,ADDRESS,PHONE,BUDGET,URL) VALUES (?,?,?,?,?,?,?,?)",(rest_count,names,cuisines.strip(),ratings,address.strip(),phone.strip(),budget,url))
        rest_count += 1
        ob.commit()

def main():
    pages = 2
    for page in range(pages):
        scraper(page)
    
    ob.close()

if __name__ == '__main__':
    main()
