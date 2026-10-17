import random

random.seed(42)

class Finances():
    def __init__(self, params, city, date):
        self.city = city
        self.date = date
        self.updateParameters(params)

    def updateParameters(self, params):
        self.expenses = params['expenses']
        self.salaries = params['salaries']

        self.temporaryExpense = 0

        self.personsWithJob = params['persons with job']
        self.totalPeople = params['total persons']

        self.getMonthlyIncome()

        self.miscExpenseRange = params['miscellaneous expense range']

        self.checkingAccount = params['checking account']['initial balance']
        self.maxInChecking = params['checking account']['maximum balance']

        self.savingsAccount = params['savings account']['initial balance']
        self.maxInSavings = params['savings account']['maximum balance']

        self.toInvestmentPercentage = params['% income to investment account']

        # Check if any salaries will be added later to not waste time checking every month
        self.checkForUpdateableSalaries()

        # Calculate inflation rates ahead of time
        self.inflationRates = generateInflationRates(self.date.startYear, self.date.endYear)

        self.getTotals()
    
    def getMonthlyIncome(self):
        for key, person in self.salaries.items():
            sal = person['gross salary']
            
            deductions = calculateTaxes(sal, self.city.taxes)

            netSalary = round(sal - deductions,2)
            netMonthly = round(netSalary/12,2)

            self.salaries[key]['net salary'] = netSalary
            self.salaries[key]['net monthly'] = netMonthly
            self.salaries[key]['tax withheld'] = sal - netSalary
            self.salaries[key]['deductions'] = deductions
    
    def cycleMonth(self, investmentAccount, taxablePropertyProfit, propertyMonthNet):
        self.monthsPassed += 1
        self.currentMonth += 1
        if self.currentMonth == 13:
            self.currentMonth = 1
            self.currentYear += 1
            self.payTaxes(taxablePropertyProfit)
            self.inflation()
            self.getRaise()

        self.checkForNewSalary()
        
        self.getPaycheck()
        self.payExpenses(investmentAccount)
        self.sendMoneyToAccounts(investmentAccount, propertyMonthNet)

    def getPaycheck(self):
        for val in self.salaries.values():
            self.checkingAccount += val['net monthly']
    
    def payExpenses(self, investmentAccount):
        self.totalExpensesThisMonth = self.totalMonthlyExpenses

        self.accountsContribution = 0

        # normal expenses
        self.checkingAccount -= self.totalMonthlyExpenses
        
        # random monthly expense
        randomExpense = random.randint(self.miscExpenseRange[0], self.miscExpenseRange[1])
        self.checkingAccount -= randomExpense
        self.totalExpensesThisMonth += randomExpense

        # If below 0, withdraw from account to have 1k on-hand
        if self.checkingAccount <= 0:
            investmentAccount.withdraw(abs(self.checkingAccount) + 1000)
            self.checkingAccount = 1000
        
        # dedicate half of leftover to temporary expenses if they exist
        if self.temporaryExpense > 0:
            payment = round(self.checkingAccount/2, 2)
            self.temporaryExpense -= payment
            self.checkingAccount -= payment
            self.totalExpensesThisMonth += payment

            if self.temporaryExpense <= 0:
                self.checkingAccount += abs(self.temporaryExpense)
                self.temporaryExpense = 0

        # If surplus over maxInChecking, send to account
        elif self.checkingAccount > self.maxInChecking:
            self.accountsContribution += self.checkingAccount - self.maxInChecking
            self.checkingAccount = self.maxInChecking

    def getTotals(self, which = 'both'):
        if which in ['expenses', 'both']:
            self.totalMonthlyExpenses = 0
            for val in self.expenses.values():
                self.totalMonthlyExpenses += val
        
        if which in ['income', 'both']:
            self.totalMonthlyIncome = 0
            for val in self.salaries.values():
                self.totalMonthlyIncome += val['net monthly']
    
    def inflation(self):
        inflationRate = self.inflationRates[self.currentYear]
        for key in self.expenses.keys():
            self.expenses[key] *= (1+inflationRate)
        
        self.getTotals('expenses')
    
    def getRaise(self):
        for key in self.salaries.keys():
            # Random raise per income, small (20%) chance to get promoted, hard 10% raise
            if random.randint(0, 100) <= 20:
                raiseRate = 0.10
            else:
                raiseRate = random.randint(0, 10)/100

            newSalary = self.salaries[key]['gross salary'] * (1+raiseRate)

            # If new salary would exceed 200k, don't let it (artificial cap on salaries)
            if newSalary > 200000:
                self.salaries[key]['gross salary'] = 200000
            else:
                self.salaries[key]['gross salary'] = newSalary
        
        self.getMonthlyIncome()
        self.getTotals('income')
    
    def sendMoneyToAccounts(self, investmentAccount, propertyProfit):
        totalPool = propertyProfit + self.accountsContribution

        toInvestmentAccount = 0
        toSavingsAccount = 0

        if investmentAccount.active:
            toInvestmentAccount = round(totalPool * self.toInvestmentPercentage, 2)
            toSavingsAccount = round(totalPool * (1-self.toInvestmentPercentage), 2)
        else:
            toSavingsAccount = totalPool

        if self.savingsAccount+toSavingsAccount > self.maxInSavings and investmentAccount.active:
            toInvestmentAccount += (toSavingsAccount + self.savingsAccount) - self.maxInSavings
            toSavingsAccount = self.maxInSavings - self.savingsAccount
        
        self.toSavingsAccount = toSavingsAccount
        self.toInvestmentAccount = toInvestmentAccount

        self.savingsAccount += self.toSavingsAccount
        investmentAccount.deposit(self.toInvestmentAccount)

    def checkForUpdateableSalaries(self):
        self.checkSalaries = False
        for key in self.salaries:
            if not self.salaries[key]['has job'] and self.salaries[key]['months before getting job'] != -1:
                self.checkSalaries = True
            elif self.salaries[key]['has job']:
                self.salaries[key]['salary start'] = [self.date.startMonth, self.date.startYear]

    def checkForNewSalary(self):
        if not self.checkSalaries:
            return
        
        for key in self.salaries:
            if self.salaries[key]['has job']:
                continue
            if self.monthsPassed == self.salaries[key]['months before getting job']:
                self.salaries[key]['has job'] = True
                self.salaries[key]['gross salary'] = self.salaries[key]['salary when job started']
                self.salaries[key]['salary start'] = [self.currentMonth, self.currentYear]

        self.getMonthlyIncome()
    
    def payTaxes(self, taxablePropertyProfit):
        # This function is to square-up taxes for whomever the primary for property
        # purchases is since their taxable salary is increased by the profit from the
        # properties. Therefore, if no property profit, taxes already square
        if taxablePropertyProfit == 0:
            return
        
        primary = None
        for p in self.salaries.values():
            if p['is primary for property purchase']:
                primary = p
        
        if primary is None:
            return
        
        income = primary['gross salary']
        deductions = primary['deductions']
        
        # If less than 12 months have passed, only a portion of first year happened
        if self.monthsPassed < 12:
            income = (income/12) * self.monthsPassed
            deductions = (deductions/12) * self.monthsPassed
        
        combinedIncome = income + taxablePropertyProfit
        actualDeductions = calculateTaxes(combinedIncome, self.city.taxes)
        difference = actualDeductions - deductions

        # If there's a refund add it, otherwise, pay it
        if difference <= 0: 
            self.checkingAccount += abs(difference)
            return
        
        # Take payment out of savings first
        self.savingsAccount -= difference

        # If savings covered it, we're good
        if self.savingsAccount >= 0:
            return
        
        # If not enough in savings, still zero it and check if checking has enough
        leftoverChecking = self.checkingAccount - abs(self.savingsAccount)
        self.savingsAccount = 0
        
        # If enough in checking account, use that, otherwise just add temporary expense
        if leftoverChecking >= 0:
            self.checkingAccount = leftoverChecking
            return
        
        self.temporaryExpense += difference


def calculateTaxes(sal, taxes):
    taxableIncome = sal - taxes['basic allowance']
    deductions = 0

    # Handle taxed on gross deductions
    rates = taxes['taxed on gross']['%']
    caps = taxes['taxed on gross']['cap']

    previousCap = 0.0

    for i, cap in enumerate(caps):
        rate = rates[i]
        if sal > previousCap:
            if sal <= cap:
                deductions += rate * (sal - previousCap)
                break
            else:
                deductions += rate * (cap - previousCap)
                previousCap = cap
        else:
            break
    
    # Handle progressive scale deductions
    for bracket in taxes['tax brackets']:
        lowerBound, upperBound, rate = bracket
        if taxableIncome > lowerBound:
            amountInBracket = min(
                taxableIncome - lowerBound,
                (upperBound - lowerBound) if upperBound != float('inf') else taxableIncome
            )
            deductions += amountInBracket * rate
        else:
            break
    
    return deductions
    

def generateInflationRates(startYear, endYear):
    nYears = endYear - startYear
    current = 0.025
    stdev = 0.005
    minRate, maxRate = 0.0, 0.06
    iYear = startYear

    rates = {startYear: current}

    for _ in range(nYears):
        newRate = rates[iYear] + random.gauss(0, stdev)
        newRate = max(minRate, min(maxRate, newRate))
        iYear += 1
        rates[iYear] = round(newRate, 5)
    
    return rates