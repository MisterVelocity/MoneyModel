class InvestmentAccount():
    def __init__(self, params):
        self.balance = 0
        self.monthlyDividends = 0

        self.updateParameters(params)
    
    def updateParameters(self, params):
        self.active = params['active']

        if not self.active:
            return 
        
        self.balance = params['initial balance']

        self.apy = params['yearly interest rate']
        self.monthlyInterest = self.apy/12

        self.capitalGainsTax = params['capital gains tax']

        self.minimumBalance = params['minimum in account']

        self.calculateMonthlyDividends()

    def cycleMonth(self):
        if not self.active:
            return
        self.monthlyGrowth()
        self.calculateMonthlyDividends()

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        self.balance -= self.calculateWithdrawal(amount)

    def canWithdraw(self, amount = None, amountRange = None):
        if amount is None and amountRange is None:
            return None

        maxVal = self.getMaxWithdrawal()

        if amount is not None:
            return amount <= maxVal
        
        if amountRange[0] <= maxVal <= amountRange[1]:
            return maxVal

        return 0 if maxVal < amountRange[0] else amountRange[1]

    def getMaxWithdrawal(self):
        return -(self.minimumBalance - self.balance)*(1-self.capitalGainsTax)

    def calcualateLeftover(self, amount):
        return self.balance - self.calculateWithdrawal(amount)

    def calculateWithdrawal(self, amount):
        return amount / (1-self.capitalGainsTax)
    
    def monthlyGrowth(self):
        self.balance *= (1+self.monthlyInterest)
    
    def calculateMonthlyDividends(self):
        self.monthlyDividends = self.balance * self.monthlyInterest