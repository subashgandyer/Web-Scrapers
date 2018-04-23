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


ob=sqlite3.connect("San_Mateo_tester.db")
ob.execute("DROP TABLE IF EXISTS Rests")
ob.execute('''CREATE TABLE Rests (NAME TEXT,RATING TEXT,ADDRESS TEXT,PHONE TEXT,BUDGET TEXT,CUSINE TEXT,REVIEW TEXT,REVIEWCOUNT TEXT);''')
r=requests.get("https://www.yelp.com/search?find_loc=San+Mateo,+CA,+United+States&start=0")
soup=BeautifulSoup(r.content,"lxml")
for link in soup.find_all("a",{"class":"biz-name js-analytics-click"}):
    name.append(link.text)
    #j=j+1

for rat in soup.find_all("i"):
     ratings = rat.get("title")
     rating.append(ratings)
     print ratings

for cus in soup.find_all("span",{"class":"category-str-list"}):
    cusines = cus.text
    cusine.append(cusines)
    print cusines

for adr in soup.find_all("address"):
    add = adr.text
    address.append(add)
    print add

for bud in soup.find_all("span",{"class":"business-attribute price-range"}):
    budd = bud.text
    if budd == '':
        budget.append('')
    budget.append(budd)
    print budd

print budget

for ph in soup.find_all("span",{"class":"biz-phone"}):
    pho = ph.text
    phone.append(pho)
    print pho

for rev in soup.find_all("p",{"class":"snippet"}):
    revs = rev.text
    review.append(revs)
    print revs

for rev in soup.find_all("span",{"class":"review-count rating-qualifier"}):
    norevs = rev.text
    nrev.append(rev.text)
    print norevs

# print name
# print rating
# print phone
# print cusine
# print address
# print budget
# print phone
# print review
# print nrev


if not name:
    name = ''
if not rating:
    rating = ''
if not cusine:
    cusine = ''
if not address:
    address = ''
if not budget:
    budget = ''
if not phone:
    phone = ''
if not review:
    review = ''
if not nrev:
    nrev = ''

for i in range (len(name)):
   ob.execute("INSERT INTO Rests(NAME,CUSINE,RATING,ADDRESS,PHONE,BUDGET,REVIEW,REVIEWCOUNT) VALUES (?,?,?,?,?,?,?,?)",(name[i],cusine[i].strip(),rating[i],address[i].strip(),phone[i].strip(),budget[i],review[i].strip(),nrev[i].strip()))
   i=i+1
i=1
op=ob.execute("SELECT NAME,CUSINE,RATING,ADDRESS,PHONE,BUDGET,REVIEW,REVIEWCOUNT from Rests")
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
ob.commit()
ob.close()
