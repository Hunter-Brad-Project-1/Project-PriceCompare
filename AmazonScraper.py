import requests
from bs4 import BeautifulSoup
import html5lib

#PRODUCT CLASS
class Product:

    price = ""
    rating = 0
    name = ""
    def __init__(self, name, price, url, rating):
        self.name = name
        self.price = price
        self.rating = rating
        self.url = url
    def getPrice(self):
        return self.price
    def getName(self):
        return self.name
    def getRating(self):
        return self.rating
    def toString(self):
        return "Name: " + self.name + "\nPrice: " + str(self.price) + "\nRating: " + str(self.rating)

doritos = Product('Doritos','$25','www.dorit.os',4)
print(doritos.toString())

#WEBSCRAPER BEGINS
class AmazonWebScraper:
    searchItem = "test"
    parsedContent = "blank"
    def __init__(self, searchTerm):
        self.searchItem = searchTerm

        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64;     x64; rv:66.0) Gecko/20100101 Firefox/66.0",
                   "Accept-Encoding": "gzip, deflate",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1",
                   "Connection": "close", "Upgrade-Insecure-Requests": "1"}

        page = requests.get("https://www.amazon.com/s?k=" + self.searchItem, headers=headers)
        # test if response is good. 200 is all ok
        print(page)

        self.parsedContent = BeautifulSoup(page.content,"html5lib")

        # For debugging:
        #print(parsedContent.prettify())

        # searchPrices = parsedContent.find_all('span')
        # searchPriceElements = parsedContent.findAll('span', attrs={'class':'a-price'})

    def getProducts(self):
        #for divTag in self.parsedContent.find_all('div', attrs={'class':'sg-col-4-of-24 sg-col-4-of-12 sg-col-4-of-36 s-result-item s-asin sg-col-4-of-28 sg-col-4-of-16 AdHolder sg-col sg-col-4-of-20 sg-col-4-of-32'}, recursive = True):
        #    print('Found one.')
        Products = []


        for divTag in self.parsedContent.find_all('div', class_ = 'sg-col-inner', recursive=True):
            #print('Found one.')
            thisName = ''
            thisLinkPart = divTag.find('a', class_ = 'a-link-normal')
            if thisLinkPart is not None:
                thisNameParent = thisLinkPart.find('img')
                if thisNameParent is not None:
                    thisName = thisNameParent.attrs['alt']

            #print("Name: " + thisName)
            thisPriceParent = divTag.find('span', class_ = 'a-price')
            thisPriceString = ''
            if thisPriceParent is not None:
                thisPriceString = thisPriceParent.find('span', class_="a-offscreen").get_text()
            #print("Price: " + thisPriceString)

            thisUrlTag = divTag.find('a', class_="a-link-normal a-text-normal")
            thisUrl = ''
            if thisUrlTag is not None:

                thisUrl = thisUrlTag['href']


            thisUrl = 'amazon.com' + thisUrl
            #print("Url: " + thisUrl)
        Products.append(Product(thisName, thisPriceString, thisUrl, 5))
        return Products
    def getProductsAndPrint(self):

        for thisProduct in getProducts():
            print(thisProduct.toString())


    def printContents(self):
        print(self.parsedContent.prettify())


    # The following are all temporary functions for testing.
    def getLinksTest(self):
        newList = []
        print(newList)
        for link in self.parsedContent.find_all('a'):
            print(link.get('href'))
    def getSpansTest(self):
        for spanTag in self.parsedContent.find_all('span', recursive=True):
            print(spanTag)
    def getDivsTest(self):
        #for divTag in self.parsedContent.find_all('div', attrs={'class':'sg-col-4-of-24 sg-col-4-of-12 sg-col-4-of-36 s-result-item s-asin sg-col-4-of-28 sg-col-4-of-16 AdHolder sg-col sg-col-4-of-20 sg-col-4-of-32'}, recursive = True):
        #    print('Found one.')


        for divTag in self.parsedContent.find_all('div', class_ = 'sg-col-inner', recursive=True):
            print('Found one.')
    def tempTest(self):
        for header in self.parsedContent.find_all('h1'):
            print("Headline 1: ")
            print(header)

        for divTag in self.parsedContent.find_all('div', attrs={'class': "s-desktop-width-max s-desktop-content sg-row"}, recursive=True):
            print('Found one.')
    def getVisibleDivs(self):
        print("got here.")
        for divTag in self.parsedContent.find_all('div',recursive=True):

            print("found a div")
            print(divTag.attrs)
    def allTags(self):
        for tag in self.parsedContent.find_all(True):
            print(tag.name)

testScraper = AmazonWebScraper("doritos")
testScraper.printContents()
#testScraper.getSpans()
testScraper.getProducts()
#testScraper.getVisibleDivs()
#testScraper.allTags()
#testScraper.tempTest()