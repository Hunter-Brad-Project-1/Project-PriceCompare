from bs4 import BeautifulSoup
import requests
import sys

def priceprocess(string):
    index = -1
    if string == "":
        return 0
    for i in range(0, len(string)-1):
        if string[i] == ' ':
            index = i
    return float(string[index+2:])

def ratingprocess(string):
    index = -1
    if string == "":
        return 0
    for i in range(0, len(string)):
        if string[i] == ' ':
            index = i
            break
    if index == -1:
        return 0
    return float(string[0:index])/5.0

SORTING_MODE = 1
#1 - Price + ShippingPrice / 2 - Price / 3 - Rating

class Product:
    price = ""
    rating = 0
    name = ""
    shipPrice = 0
    url = ""
    rating = 0
    distributor = ""
    def __init__(self, name, price, shipPrice, url, rating, distributor = "N/A"):
        self.name = name
        self.price = price
        self.rating = rating
        self.shipPrice = shipPrice
        self.distributor = distributor
        self.url = url
    def __lt__(self, other):
        if SORTING_MODE == 1:
            return self.price + self.shipPrice < other.price + other.shipPrice
        if SORTING_MODE == 2:
            return self.price < other.price
        if SORTING_MODE == 3:
            return self.rating < other.rating
        return False
    def getPrice(self):
        return self.price
    def getName(self):
        return self.name
    def getRating(self):
        return self.rating
    def getShipPrice(self):
        return self.shipPrice
    def getTotalPrice(self):
        return self.price + self.shipPrice
    def toString(self):
        return "Name: " + self.name + "\nPrice: " + str(self.price) + "\nRating: " + str(self.rating) + "\nShipping Price: " + str(self.shipPrice) + "\nDistributor: " + str(self.distributor)


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

        bookUrl = bookListing.find(class_="s-item__link")["href"]

        bookDistributor = bookListing.find(class_="s-item__subtitle").text

        bookRating = bookListing.find(class_="b-starrating")
        if bookRating and bookRating.find(class_="clipped"):
            bookRating = ratingprocess(bookRating.find(class_="clipped").text)
        else:
            bookRating = 0
        print(bookRating)
        
        if bookDistributor[0:2] == "by":
            bookDistributor = bookDistributor[3:]
        else:
            bookDistributor = "N/A"
        
        bookPrice = 0
        if bookListing.find(class_="s-item__price").text[-1:] != "g":
            bookPrice = priceprocess(bookListing.find(class_="s-item__price").text)

        shippingPrice = 0
        if bookListing.find(class_="s-item__shipping s-item__logisticsCost").text[-1:] != "g":
           shippingPrice = priceprocess(bookListing.find(class_="s-item__shipping s-item__logisticsCost").text)            

        Products.append(Product(bookName, bookPrice, shippingPrice, bookUrl, bookRating, bookDistributor))
        
        countGood += 1
    if countGood == 10:
        break

Products = sorted(Products)

for i in Products:
    print("" + str(i.name) + " at " + str(i.price))




