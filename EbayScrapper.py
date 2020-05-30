from bs4 import BeautifulSoup
import requests
import sys

class Product:
    name = ""
    price = 0.0
    companyName = ""
    def __init__(self, nm, prc, cpnm = "N/A"):
        self.name = nm
        self.price = prc
        self.companyName = cpnm
    def __lt__(self, other):
        return self.price < other.price


name = input("What is the name of your book?")

page = requests.get("https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw="+name+"&_sacat=0&LH_BIN=1")

html_file = page.content

soup = BeautifulSoup(html_file, 'lxml')

listProducts = soup.find_all(class_='s-item')
countGood = 0

print(len(listProducts))

for i in range(0, len(listProducts)):
    bookListing = listProducts[i]
    if not bookListing.find(class_="s-item__title--tagblock"):
        #print("I found a good one!")
        #print(bookListing.prettify())
        print(bookListing.find(class_="s-item__title").text) #Book Name
        print(bookListing.find(class_="s-item__price").text) #Book Price
        print(bookListing.find(class_="s-item__shipping s-item__logisticsCost").text) #Shipping Price
        countGood += 1
    if countGood == 10:
        break
    print("")



