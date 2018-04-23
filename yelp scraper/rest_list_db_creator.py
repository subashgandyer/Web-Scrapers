import sqlite3
from bs4 import BeautifulSoup
from rest_list import rest_list
import re

ob=sqlite3.connect("San_Mateo_reviews.db")
#oc = sqlite3.connect("")
ob.execute("DROP TABLE IF EXISTS SanMateoReviewsOnly")
ob.execute('''CREATE TABLE SanMateoReviewsOnly (COUNTER TEXT,REST_NAME TEXT,REVIEWER_NAME TEXT,REVIEW_RATING TEXT,REVIEW_DATE TEXT,REVIEW_TEXT TEXT);''')

cnt = 0
for i in range(len(rest_list)):
	rest_name = rest_list[i][0]
	print rest_name, type(rest_name)
	#rest_name = rest_name.strip()
	#ob.execute("INSERT INTO Reviews(COUNTER,REST_NAME,REVIEWER_NAME,REVIEW_RATING,REVIEW_DATE,REVIEW_TEXT) VALUES (?,?,?,?,?,?)",(review_count,rest_name,reviewer_name,review_rating,review_date,review_text.strip()))
	#ob.execute("SELECT * FROM Reviews WHERE REST_NAME = "rest_name)
	#cursor = ob.execute("SELECT * FROM Reviews")
	cursor = ob.execute('SELECT * FROM SanMateoOnly WHERE REST_NAME LIKE "'+rest_name+'"')
	#cursor = ob.execute("SELECT * FROM Reviews WHERE REST_NAME LIKE ?",(str(rest_name)))

	#print cursor
	
	for row in cursor:
		cnt += 1
	   	#print "REVIEW_ID = ", row[0]
	   	print "RES_NAME = ", row[0]
	   	print "REVIEWER_NAME = ", row[1]
	   	rating = row[2].split(' ')[0]
	   	print "REVIEW_RATING = ", rating
	   	print "REVIEW_DATE = ", row[3]
	   	print "REVIEW_TEXT ", row[4]
	   	#print "%s \t\t %s \t\t %s \t\t %s \t\t %s" % (row[1],row[2],row[3],row[4],row[5])
		print cnt
		ob.execute("INSERT INTO SanMateoReviewsOnly(COUNTER,REST_NAME,REVIEWER_NAME,REVIEW_RATING,REVIEW_DATE,REVIEW_TEXT) VALUES (?,?,?,?,?,?)",(cnt,row[0],row[1],rating,row[3],row[4]))
		ob.commit()
	print cnt


ob.close()