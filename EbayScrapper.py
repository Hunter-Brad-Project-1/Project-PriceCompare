from bs4 import BeautifulSoup
import requests
import sys

def process(string):
    index = -1
    if string == "":
        return 0
    for i in range(0, len(string)-1):
        if string[i] == ' ':
            index = i
    return float(string[index+2:])

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

Products = []

for i in range(0, len(listProducts)):
    bookListing = listProducts[i]
    if not bookListing.find(class_="s-item__title--tagblock"):
        #print("I found a good one!")
        #print(bookListing.prettify())

        bookName = bookListing.find(class_="s-item__title").text

        bookPrice = 0
        if bookListing.find(class_="s-item__price").text[-1:] != "g":
            bookPrice = process(bookListing.find(class_="s-item__price").text)

        shippingPrice = 0
        if bookListing.find(class_="s-item__shipping s-item__logisticsCost").text[-1:] != "g":
           shippingPrice = process(bookListing.find(class_="s-item__shipping s-item__logisticsCost").text)            

        Products.append(Product(bookName, bookPrice+shippingPrice))
        
        countGood += 1
    if countGood == 10:
        break

Products = sorted(Products)

for i in Products:
    print("" + str(i.name) + " at " + str(i.price))




