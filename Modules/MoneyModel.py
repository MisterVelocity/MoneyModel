import pandas as pd
from Functions import formatNumberAsString as fs

class MoneyModel():
    def __init__(self, finances, investmentAccount, properties, startDate, endDate, months):
        self.finances = finances
        self.investmentAccount = investmentAccount
        self.properties = properties

        self.months = months

        self.startMonth = startDate[0]
        self.startYear = startDate[1]

        self.currentMonth = startDate[0]
        self.currentYear = startDate[1]

        self.endMonth = endDate[0]
        self.endYear = endDate[1]

        self.initOutputStruct()
        self.getNumberOfMonths()
        self.conductMethod()
        self.outputResults()

    def initOutputStruct(self):
        self.numRows = 0

        cols = ['Month', 'Year', 'Chk. Acc. Balance', 'Sav. Acc. Balance']

        if self.investmentAccount.active:
            cols.extend(
                [
                    'Inv. Acc. Balance', 
                    'Dividends from Inv. Acc.'
                ]
            )

        if self.properties.active:
            cols.extend(
                [
                    'Total # Properties',
                    '# Properties Paid Off', 
                    'Total Mortgage Balance', 
                    'Total Property Payment', 
                    'Profit from Properties'
                ]
            )

        cols.extend(
            [
                'Expenses',
                'Employment Income',
                'Total Monthly Net Income',
                'To Savings Account'
            ]
        )

        if self.investmentAccount.active:
            cols.append('To Investment Account')

        self.outFile = pd.DataFrame(columns = cols)

    def getNumberOfMonths(self):
        # # of years subtracted by one since final year will maybe be a portion of the year
        nYears = self.endYear - self.startYear
        nMonths = nYears * 12

        # Account for first year
        nMonths -= self.startMonth-1

        # Account for last year
        nMonths += self.endMonth

        self.nMonths = nMonths

    def conductMethod(self):
        for month in range(self.nMonths):
            self.currentMonth += 1
            if self.currentMonth > 12:
                self.currentMonth = 1
                self.currentYear += 1

            # First, let investment account accrue interest
            self.investmentAccount.cycleMonth()

            # Now get profit from properties and check if one can be bought
            self.properties.cycleMonth(self.investmentAccount)

            # Now pay all expenses, get paycheck
            self.finances.cycleMonth(
                self.investmentAccount, 
                self.properties.taxableProfit, 
                self.properties.totalMonthlyNetProfit
            )

            # Collect current data
            self.collectData()

    def collectData(self):
        jobIncome = self.finances.totalMonthlyIncome
        dividends = self.investmentAccount.monthlyDividends
        propertyProfit = self.properties.totalMonthlyNetProfit
        totalIncome = jobIncome + dividends + propertyProfit

        row = [
            self.months[self.currentMonth],
            self.currentYear,
            fs(self.finances.checkingAccount),
            fs(self.finances.savingsAccount)
        ]

        if self.investmentAccount.active:
            row.extend(
                [
                    fs(self.investmentAccount.balance),
                    fs(self.investmentAccount.monthlyDividends)
                ]
            )
        if self.properties.active:
            row.extend(
                [
                    self.properties.numberOfProperties,
                    self.properties.numberPropertiesPaidOff,
                    fs(self.properties.totalMortgages),
                    fs(self.properties.totalMonthlyPayment),
                    fs(self.properties.totalMonthlyNetProfit)
                ]
            )

        row.extend(
            [
                fs(self.finances.totalExpensesThisMonth), 
                fs(jobIncome),
                fs(totalIncome),
                fs(self.finances.toSavingsAccount)
            ]
        )

        if self.investmentAccount.active:
            row.append(fs(self.finances.toInvestmentAccount))
        
        self.outFile.loc[self.numRows] = row
        self.numRows += 1

    def outputResults(self):
        self.outFile.to_csv('Results.csv', index = False)

    