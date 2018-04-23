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


r=requests.get("https://www.yelp.com/search?find_loc=San+Mateo,+CA,+United+States&start=10")
soup=BeautifulSoup(r.content,"lxml")
for link in soup.find_all("div",{"class":"biz-listing-large"}):
    #print link


    name = link.find("a",{"class":"biz-name js-analytics-click"})
    if not name:
        names = ''
    else:
        names = name.text
    print names
    
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
    # print 'Reviews : ',revs
    # print 'No. of Reviews :', norevs

    ob.execute("INSERT INTO Rests(NAME,CUISINE,RATING,ADDRESS,PHONE,BUDGET) VALUES (?,?,?,?,?,?)",(names,cuisines.strip(),ratings,address.strip(),phone.strip(),budget))
    ob.commit()


ob.close()
