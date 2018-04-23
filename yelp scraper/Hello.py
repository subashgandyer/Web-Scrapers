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

ob=sqlite3.connect("testdb.db")
ob.execute("DROP TABLE IF EXISTS test1")
ob.execute('''CREATE TABLE test1 (NAME TEXT,RATING TEXT,ADDRESS TEXT,PHONE TEXT,BUDGET TEXT,CUSINE TEXT,REVIEW TEXT,REVIEWCOUNT TEXT);''')
r=requests.get("https://www.yelp.com/search?find_loc=San+Jose,+CA&start=90")
soup=BeautifulSoup(r.content,"lxml")
for link in soup.find_all("a",{"class":"biz-name js-analytics-click"}):
    name.append(link.text)
    j=j+1

for rat in soup.find_all("i"):
     rating.append(rat.get("title"))

for cus in soup.find_all("span",{"class":"category-str-list"}):
    cusine.append(cus.text)

for adr in soup.find_all("address"):
     address.append(adr.text)

for bud in soup.find_all("span",{"class":"business-attribute price-range"}):
    budget.append(bud.text)

for ph in soup.find_all("span",{"class":"biz-phone"}):
    phone.append(ph.text)

for rev in soup.find_all("p",{"class":"snippet"}):
    review.append(rev.text)

for rev in soup.find_all("span",{"class":"review-count rating-qualifier"}):
    nrev.append(rev.text)

for i in range (0,j):
   ob.execute("INSERT INTO test1(NAME,CUSINE,RATING,ADDRESS,PHONE,BUDGET,REVIEW,REVIEWCOUNT) VALUES (?,?,?,?,?,?,?,?)",(name[i],cusine[i].strip(),rating[i],address[i].strip(),phone[i].strip(),budget[i],review[i].strip(),nrev[i].strip()))
   i=i+1
i=1
op=ob.execute("SELECT NAME,CUSINE,RATING,ADDRESS,PHONE,BUDGET,REVIEW,REVIEWCOUNT from test1")
for k in op:
    print i,".Name    -",k[0]
    print "   Cusine  -",k[1]
    print "   Rating  -",k[2]
    print "   Address -",k[3]
    print "   Phone   -",k[4]
    print "   Budget  -",k[5]
    print "   Review  -",k[6].strip()
    print "   NO.OF Reviews-",k[7]
    print "\n\n"
    i=i+1

