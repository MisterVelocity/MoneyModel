from random import randint
from math import pow, ceil, floor

class Properties():
    def __init__(self, params, city):
        self.totalMortgages = 0
        self.totalToAccount = 0
        self.totalMonthlyPayment = 0
        self.totalMonthlyNetProfit = 0
        self.totalMonthlyGrossProfit = 0
        self.totalYearlyGrossProfit = 0
        self.taxableProfit = 0
        self.grossIncomeThisYear = 0
        self.numberOfProperties = 0
        self.numberOfPropertiesPaidOff = 0
        self.monthOfLastPropertyPurchase = 0

        self.properties = []

        self.updateParameters(params, city)

    def updateParameters(self, params, city):
        self.active = params['active']

        if not self.active:
            return
        
        # For determining home price and proportional nightly rates and occupancy
        self.minPrice = params['minimum property price']
        self.maxPrice = params['maximum property price']

        self.down = city.propertyInfo['down']
        self.minDown = int(ceil(self.down * self.minPrice/1000)*1000)
        self.maxDown = int(floor(self.down * self.maxPrice/1000)*1000)

        self.occupancyRange = city.propertyInfo['occupancy']
        self.priceRange = city.propertyInfo['price']
        self.dailyRate = city.propertyInfo['daily rate']

        self.propertyTax = city.propertyInfo['propertyTax']
        self.insurance = city.propertyInfo['insurance']
        self.term = city.propertyInfo['term']

        if params['property type'] == 'vacation':
            self.propertyType = VacationRental
        else:
            self.propertyType = ResidentialRental

        self.maxProperties = params['max # properties']
        self.monthsBetweenPurchase = params['months between purchase']
        self.percentToAccount = params['% profit to accounts']
        self.residentialProfit = params['residential desired monthly net']
        self.interestRate = params['interest rate']

    def checkPropertyPurchase(self, investmentAccount):
        # If not enough months have passed since last purchase, or max properties obtained, can't buy
        if (self.monthOfLastPropertyPurchase != 0 \
        and self.monthsElapsed - self.monthOfLastPropertyPurchase < self.monthsBetweenPurchase) \
        or self.numberOfProperties == self.maxProperties:
                return

        # Check that investment account can cover down payment
        canBuy, maxPrice = self.checkInvestmentAccount(investmentAccount)

        if not canBuy:
            return

        # Buy a property
        self.buyProperty(investmentAccount, maxPrice)
        self.monthOfLastPropertyPurchase = self.monthsElapsed

    def checkInvestmentAccount(self, investmentAccount):
        allowableDown = investmentAccount.canWithdraw(amountRange = [self.minDown, self.maxDown])
        
        if allowableDown == 0:
            return False, None
        
        maxPrice = int(round(self.maxPrice * (allowableDown/self.maxDown), 0))

        return True, maxPrice
        
    def buyProperty(self, investmentAccount, maxPrice):
        self.numberOfProperties += 1

        # Get price (sales tax included in total price for simplicity)
        price = randint(self.minPrice, maxPrice)
        down = self.down * price

        # Withdraw down payment from account
        investmentAccount.withdraw(down)

        self.properties.append(self.propertyType(self, price, down, self.interestRate, self.percentToAccount, self.residentialProfit))

        self.getTotals()
    
    def cycleMonth(self, investmentAccount):
        if not self.active:
            return
        
        newYear = False
        self.currentMonth += 1
        self.monthsElapsed += 1
        if self.currentMonth == 13:
            self.currentMonth = 1
            self.currentYear += 1
            newYear = True

        # Check if we can buy a property
        self.checkPropertyPurchase(investmentAccount)

        # Pay all mortgages (track mortgage balance and amount to investment account)
        self.payMortgages()

        # Update yearly income
        self.getIncome(newYear)

        # Get total to account this month and in case anything else changed
        self.getTotals()

    def payMortgages(self):
        for p in self.properties:
            p.payMortgage()

    def getIncome(self, newYear):
        # grossIncomeThisYear is distinct from totalYearlyGrossProfit.
        # totalYearlyGrossProfit tracks the overall gross profit if each property is owned all year.
        # grossIncomeThisYear is a bucket that is zeroed every January for tax purposes given
        # that properties are at times purchased in the middle of the year.
        if newYear:
            self.taxableProfit = self.grossIncomeThisYear
            self.grossIncomeThisYear = 0
        
        for p in self.properties:
            self.grossIncomeThisYear += p.monthlyGrossProfit

    def getTotals(self):
        self.totalMortgages = 0
        self.totalToAccount = 0
        self.totalMonthlyPayment = 0
        self.totalMonthlyNetProfit = 0
        self.totalMonthlyGrossProfit = 0
        self.totalYearlyGrossProfit = 0

        for p in self.properties:
            self.totalMortgages += p.balance
            self.totalToAccount += p.toAccount
            self.totalMonthlyPayment += p.totalPayment
            self.totalMonthlyNetProfit += p.monthlyNetProfit
            self.totalMonthlyGrossProfit += p.monthlyGrossProfit
            self.totalYearlyGrossProfit += p.yearlyGrossProfit


class Property():
    def __init__(self, parent, price, down, interestRate, percentToAccount, residentialProfit):
        self.parent = parent

        self.price = price
        self.down = down
        self.interestRate = interestRate
        self.percentToAccount = percentToAccount

        self.residentialProfit = residentialProfit

        self.calculatePayment()
        self.getOccupancy()
        self.getProfit()
        
        self.toAccount = self.monthlyNetProfit * self.percentToAccount
    
    def calculatePayment(self):
        loan = self.price - self.down

        monthlyRate = self.interestRate/12
        nPayments = self.parent.term * 12

        self.mortgagePayment = loan * (monthlyRate * pow(1+monthlyRate, nPayments)) / (pow(1+monthlyRate, nPayments) -1)
        
        monthlyTax = (self.parent.propertyTax * self.price) / 12
        monthlyInsurance = self.parent.insurance /12

        self.totalPayment = self.mortgagePayment + monthlyInsurance + monthlyTax
        self.balance = loan
    
    def payMortgage(self):
        if self.balance == 0:
            self.toAccount = self.monthlyNetProfit
            return
        
        self.toAccount = self.monthlyNetProfit * self.percentToAccount
        
        toMortgage = self.mortgagePayment + (self.monthlyNetProfit * (1-self.percentToAccount))
        self.balance -= toMortgage

        if self.balance <= 0:
            self.toAccount += abs(self.balance)
            self.balance = 0
            self.totalPayment -= self.mortgagePayment
            self.monthlyNetProfit += self.mortgagePayment
            self.parent.numberPropertiesPaidOff += 1
    

class VacationRental(Property):
    def __init__(self, parent, price, down, interestRate, percentToAccount, _):
        super().__init__(parent, price, down, interestRate, percentToAccount, None)

    def getProfit(self):
        # Nightly rate range
        minRate, maxRate = self.parent.dailyRateRange[0], self.parent.dailyRateRange[1]
        minPrice, maxPrice = self.parent.priceRange[0], self.parent.priceRange[1]

        dailyRate = minRate + (self.price - minPrice) * (maxRate - minRate) / (maxPrice - minPrice)

        self.yearlyGrossProfit = round(dailyRate * 365 * self.occupancy, 2)
        self.monthlyGrossProfit = round(self.yearlyGrossProfit/12, 2)
        self.monthlyNetProfit = round(self.monthlyGrossProfit - self.totalPayment, 2)

    def getOccupancy(self):
        minOcc, maxOcc = self.parent.occupancyRange[0], self.parent.occupancyRange[1]
        minPrice, maxPrice = self.parent.priceRange[0], self.parent.priceRange[1]

        self.occupancy = minOcc + (self.price - minPrice) * (maxOcc - minOcc) / (maxPrice - minPrice)


class ResidentialRental(Property):
    def __init__(self, parent, price, down, interestRate, percentToAccount, residentialProfit):
        super().__init__(parent, price, down, interestRate, percentToAccount, residentialProfit)
    
    def getProfit(self):
        self.monthlyGrossProfit = self.residentialProfit + self.totalPayment
        self.yearlyGrossProfit = round(self.monthlyGrossProfit * 12, 2)
        self.monthlyNetProfit = self.residentialProfit

    def getOccupancy(self):
        self.occupancy = 1

