import urllib
import requests
from bs4 import BeautifulSoup
import os
r=requests.get("https://www.yelp.com/biz_photos/cloudz-hookah-lounge-san-jose")
soup=BeautifulSoup(r.content,"lxml")
pa="/home/se/PycharmProjects"

if not os.path.exists("/home/se/PycharmProjects/cloudz-hookah-lounge"):
    os.makedirs("/home/se/PycharmProjects/cloudz-hookah-lounge")
i=0
for a in soup.find_all("img",{"class":"photo-box-img"}):
    fullfilename = os.path.join("/home/se/PycharmProjects/cloudz-hookah-lounge", "img"+str(i)+".jpg")
    urllib.urlretrieve("https:"+a.get("src"), fullfilename)
    i+=1