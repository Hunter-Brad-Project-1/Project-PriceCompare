class Product:

    price = ""
    rating = 0
    name = ""
    def __init__(self, name, price, shipPrice, url, rating):
        self.name = name
        self.price = price
        self.rating = rating
        self.shipPrice = shipPrice
        self.url = url
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
        return "Name: " + self.name + "\nPrice: " + str(self.price) + "\nRating: " + str(self.rating) + "\nShipping Price: " + str(self.shipPrice)
