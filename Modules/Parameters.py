from Functions import getDefaultsJSON, createNullDictionary
from Modules import City, Date, Finances, InvestmentAccount, Properties

class Parameters():
    def __init__(self):
        self.defaults = getDefaultsJSON()
        self.getSubClasses()
        self.userInputs = createNullDictionary(self.defaults)

    def getSubClasses(self):
        self.date = Date(self.defaults['start month add'])
        self.city = City(self.defaults['city'])

        self.appendToDefaults()

    def appendToDefaults(self):
        self.defaults['properties']['minimum property price'] = self.city.propertyInfo['price'][0]
        self.defaults['properties']['maximum property price'] = self.city.propertyInfo['price'][1]
        self.defaults['properties']['interest rate'] = round(
            (self.city.propertyInfo['interest'][0] + self.city.propertyInfo['interest'][1])/2,
            3
        )
        self.defaults['finances']['expenses'] = self.city.expenses

        self.defaults['start date'] = [self.date.startMonth, self.date.startYear]
        self.defaults['end date'] = [self.date.endMonth, self.date.endYear]

    def updateCity(self, city):
        if city == self.city.city:
            return
        self.city.updateInfo(city)
        self.appendToDefaults()
    
    def updateDate(self, month, year):
        if self.date.monthToDex[month] == self.date.startMonth \
        and int(year) == self.date.startYear:
            return
        self.date.updateStartEndDates(month, year)