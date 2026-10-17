# from Functions import getIntegerInput, getFloatInput, getBoolInput
# from Functions import formatNumberAsString as fs
# from .City import City
# import numpy as np
# import datetime

# now = datetime.datetime.now()

# class Params():
#     def __init__(self):
#         self.city = City('Barcelona')

#         self.months = {
#             1: 'Jan',
#             2: 'Feb',
#             3: 'Mar',
#             4: 'Apr',
#             5: 'May',
#             6: 'Jun',
#             7: 'Jul',
#             8: 'Aug',
#             9: 'Sep',
#             10: 'Oct',
#             11: 'Nov',
#             12: 'Dec'
#         }

#         self.currentMonth = now.month
#         self.currentYear = now.year

#         self.startYear = self.currentYear
#         self.startMonth = self.currentMonth + 3

#         if self.startMonth > 12:
#             self.startMonth -= 12
#             self.startYear += 1

#         self.endMonth = self.startMonth
#         self.endYear = self.startYear + 35

#         # Initialize with default values
#         self.propertyParams = {
#             'active': True,
#             'type': 'vacation',
#             'months between purchase': 24,
#             'minimum property price': 250000,
#             'maximum property price': 400000,
#             '% profit to investment or savings account': 0.8,
#             'interest rate': round(np.average(self.city.propertyInfo['interest']), 5),
#             'max number of properties': 5,
#             'residential rental desired monthly net profit': 500
#         }
#         self.accountParams = {
#             'active': True,
#             'initial balance': 5000,
#             'yearly interest rate': 0.08,
#             'capital gains tax': 0.20,
#             'minimum in account': 20000
#         }
#         self.financeParams = {
#             'persons with job': 1,
#             'total persons': 2,
#             'salaries': {
#                 'Person 1': {
#                     'has job': True,
#                     'months before getting job': None,
#                     'salary when job started': None,
#                     'gross salary': 100000,
#                     'is primary for property purchase': True
#                 },
#                 'Person 2': {
#                     'has job': False,
#                     'months before getting job': 24,
#                     'salary when job started': 40000,
#                     'gross salary': 0,
#                     'is primary for property purchase': False
#                 }
#             },
#             'expenses': self.city.expenses,
#             'miscellaneous expense range': [200, 1500],
#             'taxes': self.city.taxes,
#             'initial checking account balance': 1000,
#             'maximum to carry in checking': 5000,
#             'initial savings account balance': 10000,
#             'maximum to carry in savings': 100000,
#             '% income to investment account': 0.60
#         }

#         self.printDateInfo()
#         self.printCityInfo()
#         self.printFinancialParams()
#         self.printPropertyParams()
#         self.printAccountParams()
    
#     def printDateInfo(self):
#         print('\n\n------------ Starting Date ------------')
#         print(f'{self.months[self.startMonth]} {self.startYear}')

#         print('\nModel will run for 35 years from starting date')

#         print('\nDo you want to change the starting date?')
#         print('(0 = no    1 = yes)')
                    
#         if getBoolInput('\nAnswer: '):
#             self.updateDate()
        
#     def updateDate(self):
#         print(f'\nCurrent: {self.months[self.startMonth]} {self.startYear}')
#         print('\n* Note, if you change the starting date to a year in the future, expenses will be updated')
#         print('to account for inflation that would happen in that time (based on averages).')
#         print('Therefore, expenses displayed later to you will be current for THIS year and updated later.')
#         print('If you choose to change the expenses, please enter what you expect THIS year and they too will be updated')
        
#         year = getIntegerInput(
#             f'\nStarting year (integer, {self.currentYear} <= year < {self.currentYear + 100}): ',
#             validRange = [self.currentYear, self.currentYear + 100]
#         )

#         print('\nWhen prompted, input the number corresponding to the month you wish to start the model in')
#         for key, val in self.months.items():
#             print(f'{key}: {val}')
        
#         valid = False
#         while not valid:
#             month = getIntegerInput(
#                 'Answer (integer on list): ',
#                 validRange = [1, 12]
#             )
            
#             valid = self.checkDateInput(month, year)
#             if not valid:
#                 print('Current year chosen--please choose either this month or one in the future!')

#         self.startMonth = month
#         self.startYear = year
#         self.endMonth = month
#         self.endYear = year + 60

#     def printCityInfo(self):
#         print('\n\n------------ City ------------')
#         print(self.city.city)
#         print('\nCity choice defines expenses, property information, and taxation.')
#         print('\nDo you want to change your city?')
#         print('(0 = no     1 = yes)')

#         if getBoolInput('Answer: '):
#             self.updateCity()
        
#     def updateCity(self):
#         print('\nPlease choose a city from the list and enter its integer when prompted')
#         for key, val in self.city.cities.items():
#             print(f'  {key} = {val}')

#         city = getIntegerInput(
#             'City #: ',
#             validRange = [0, len(self.city.cities) - 1]
#         )
        
#         self.city.city = self.city.cities[city]
#         self.city.updateInfo()
#         self.financeParams['expenses'] = self.city.expenses
#         self.financeParams['taxes'] = self.city.taxes
#         self.propertyParams['interest rate'] = round(np.average(self.city.propertyInfo['interest']), 5)

#     def printFinancialParams(self):
#         print('\n\n------------ Financial Parameters ------------')
#         print('Here are the default values')

#         print('\n--- Salaries ---')
#         sals = self.financeParams['salaries']
#         for key in sals.keys():
#             print(f'\n{key} - ')
#             for key2, val in sals[key].items():
#                 print(f'{key2}: {val}')

#         print('\n--- Expenses ---')
#         print(f'City (taxes and expenses will be based on city): {self.city.city}')
#         exp = self.financeParams['expenses']
#         for key, val in exp.items():
#             print(f'{key}: {val}')
        
#         print('\nMiscellaneous expenses cover potential, unplanned needs every month - doctors, entertainment, etc.')
#         print('Every value in range has an EQUAL chance of happening EVERY month - consider carefully')
#         mRange = self.financeParams['miscellaneous expense range']
#         print(f'Miscellaneous expense range: {fs(mRange[0])} - {fs(mRange[1])}')


#         print('\n--- Checking Account Info ---')
#         print(f'Initial Balance: {fs(self.financeParams["initial checking account balance"])}')
#         print(f'Maximum to Carry in Checking: {fs(self.financeParams["maximum to carry in checking"])}')
        
#         print('\n--- Savings Account Info ---')
#         print(f'Initial Balance: {fs(self.financeParams["initial savings account balance"])}')
#         print(f'Maximum to Carry in Savings: {fs(self.financeParams["maximum to carry in savings"])}')
        
#         print('\n--- Investment Account Contribution ---')
#         print(f'% Total Income to Invesment Account: {self.financeParams["% income to investment account"]*100}%')

#         print('\nDo you want to change the Financial information?')
#         print('(0 = no     1 = yes)')
                    
#         if getBoolInput('Answer: '):
#             self.updateFinancialInfo()
    
#     def updateFinancialInfo(self):
#         print('\n--------- People ---------')
#         people = getIntegerInput(
#             'Number of working-age people (integer): ',
#             validRange = [0, 50]
#         )

#         personsWithJob = getIntegerInput(
#             'Number of people with job (integer): ',
#             validRange = [0, people]
#         )
        
#         print('\n--------- Jobs ---------')
#         jobs = {}

#         primaryFound = False
#         for a in range(1, people+1):
#             print(f'\n------ Person {a} ------')
#             isPrimary = False
#             if not primaryFound:
#                 print('Will this person be the primary for property purchases (taxed accordingly)?')
#                 print('0 = no, 1 = yes')
#                 isPrimary = getBoolInput('Answer: ')
                
#                 if isPrimary:
#                     isPrimary = True
#                     primaryFound = True

#             if a <= personsWithJob:
#                 print(f'\n--- Person with Job {a} ---')
#                 sal = getIntegerInput(
#                     'Gross annual salary (integer): ',
#                     validRange = [1, 5000000]
#                 )
                
#                 jobs[f'Person {a}'] = {
#                     'has job': True,
#                     'months before getting job': None,
#                     'salary when job started': None,
#                     'gross salary': sal,
#                     'is primary for property purchase': isPrimary
#                 }

#             else:
#                 print(f'\n--- Person without job {a-personsWithJob} ---')
#                 months = getIntegerInput(
#                     'Months before getting a job (integer, -1 = "Never"): ',
#                     validRange = [-1, 1000]
#                 )

#                 sal = None
#                 if months != -1:                
#                     sal = getIntegerInput(
#                         'Salary when job started (integer): ',
#                         validRange = [1, 5000000]
#                     )

#                 jobs[f'Person {a}'] = {
#                     'has job': False,
#                     'months before getting job': months,
#                     'salary when job started': sal,
#                     'gross salary': 0,
#                     'is primary for property purchase': isPrimary
#                 }

#         if not primaryFound:
#             print('No primary for property purchases provided!')
#             print('Defaulting to first person in list...')
#             jobs['Person 1']['is primary for property purchase'] = True

#         expenses = self.financeParams['expenses']
#         print('\n--------- Expenses ---------')
#         print(f'The default expenses have been updated to reflect conservative averages in your chosen city ({self.city.city})')
#         print('They are as follows:')
#         for key, val in expenses.items():
#             print(f'  - {key}: {val}')
        
#         if getBoolInput('\nWould you still like to update them? (0 = no, 1 = yes): '):
#             expKeys = expenses.keys()
#             expenses = {}
#             for key in expKeys:
#                 e = getIntegerInput(
#                     f'{key} (integer): ',
#                     validRange = [0, 5000000]
#                 )
                
#                 expenses[key] = e
            
#             print("\nThat's all the default expenses.")

#         while True:
#             if not getBoolInput('\nAdd another expense? (0 = no, 1 = yes): '):
#                 break

#             name = input('\nExpense Name: ')
#             amount = getIntegerInput(
#                 'Expense amount (integer): ',
#                 validRange = [1, 5000000]
#             )
#             expenses[name] = amount
        
#         print('\nMiscellaneous expense range')
#         minMExpense = getIntegerInput(
#             'Minimum misc. expense (integer): ',
#             validRange = [0, 5000000]
#         )
#         maxMExpense = getIntegerInput(
#             'Maximum misc. expense (integer): ',
#             validRange = [minMExpense+1, 5000001]
#         )

#         print('\n--------- Checking Account Info ---------')
#         initialChecking = getIntegerInput(
#             'Initial amount in checking account (integer): ',
#             validRange = [0, 5000000]
#         )
        
#         print('\nMaximum amount to carry in checking account')
#         print('** Any excess will be added to investment account **')
#         maxChecking = getIntegerInput(
#             'Amount (-1 = "No limit"): ',
#             validRange = [-1, np.inf]
#         )

#         print('\n--------- Savings Account Info---------')
#         initialSavings = getIntegerInput(
#             'Initial amount in savings account (integer): ',
#             validRange = [0, 5000000]
#         )
        
#         print('\nMaximum amount to carry in savings account')
#         print('** Any excess will be added to investment account **')
#         maxSavings = getIntegerInput(
#             'Amount (-1 = "No limit"): ',
#             validRange = [-1, np.inf]
#         )

#         print('\n--------- Investment Account ---------')
#         print('Percent of total income to investment account')
#         print('Remaining percentage will be added to savings account')
#         print('IE, if you enter "80", 80% will go to investment account, 20% will go to savings\n')
#         incomeToInvestment = getIntegerInput(
#             'Percentage (integer 0-100): ',
#             validRange = [0, 100]
#         )

#         self.financeParams = {
#             'persons with job': personsWithJob,
#             'total persons': people,
#             'salaries': jobs,
#             'expenses': expenses,
#             'miscellaneous expense range': [minMExpense, maxMExpense],
#             'taxes': self.city.taxes,
#             'initial checking account balance': initialChecking,
#             'maximum to carry in checking': maxChecking if maxChecking != -1 else np.inf,
#             'initial savings account balance': initialSavings,
#             'maximum to carry in savings': maxSavings if maxSavings != -1 else np.inf,
#             '% income to investment account': incomeToInvestment/100
#         }

#     def printPropertyParams(self):
#         print('\n\n------------ Property Parameters ------------')
#         print('Here are the default values')
#         for key, val in self.propertyParams.items():
#             print(f'{key}: {val}')
        
#         print('\nDo you want to purchase properties in the model?')
#         print('Turning this off affects nothing else')

#         propertiesActive = getBoolInput('Answer (0 = no    1 = yes): ')
#         self.propertyParams['active'] = propertiesActive

#         if not self.propertyParams['active']:
#             return
        
#         print('\nDo you want to update the Property information?')
#         print('0 = no    1 = yes')

#         if getBoolInput('Answer: '):
#             self.updatePropertyInfo()
    
#     def updatePropertyInfo(self):
#         print('\nPlease choose property type (will apply to all future properties)')
#         print('0 = "vacation"    1 = "residential"')
#         propertyType = getIntegerInput(
#             'Answer: ',
#             validRange = [0, 1]
#         )

#         if propertyType == 0:
#             propertyType = 'vacation'
#         else:
#             propertyType = 'residential'

#         desiredMonthlyProfit = None
#         if propertyType == 'residential':
#             print('\nDesired monthly NET profit from residential rental')
#             print(f'The current value is {self.propertyParams["residential rental desired monthly net profit"]}')
#             desiredMonthlyProfit = getIntegerInput(
#                 'Answer (integer): ',
#                 validRange = [1, 5000000]
#             )

#         monthsBeforeProperty = getIntegerInput(
#             'Min number of months between property purchase (integer): ',
#             validRange = [0, 720]
#         )
#         maxProperties = getIntegerInput(
#             'Max # of properties to purchase (integer, -1 = "No limit"): ',
#             validRange = [-1, np.inf]
#         )

#         typicalMin = self.city.propertyInfo['price'][0]
#         typicalMax = self.city.propertyInfo['price'][1]
#         print(f'\nThe typical property price range in {self.city.city} is as follows:')
#         print(f'{fs(typicalMin)} - {fs(typicalMax)}')

#         minPrice = getIntegerInput(
#             'Minimum property price (integer): ',
#             validRange = [typicalMin, typicalMax]
#         )
#         maxPrice = getIntegerInput(
#             'Maximum budgeted property price: ',
#             validRange = [minPrice, typicalMax]
#         )
        
#         typicalMin = round(self.city.propertyInfo['interest'][0]*100, 5)
#         typicalMax = round(self.city.propertyInfo['interest'][1]*100, 5)
#         print(f'\nThe typical property interest rate range in {self.city.city} is as follows:')
#         print(f'{typicalMin}% - {typicalMax}%')
#         print(f'Your current value is the average: {self.propertyParams["interest rate"] * 100}%\n')

#         intRate = getFloatInput(
#             'Expected interest rate (float): ',
#             validRange = [typicalMin, typicalMax]
#         )

#         print('\nPercent of net profit to send to investment/savings account every month')
#         print('Remaining profit will go towards mortgage for property')
#         pProfit = getIntegerInput(
#             'Answer: (integer 0-100): ',
#             validRange = [0, 100]
#         )

#         self.propertyParams = {
#             'type': propertyType,
#             'months between purchase': monthsBeforeProperty,
#             'minimum property price': minPrice,
#             'maximum property price': maxPrice,
#             '% profit to investment or savings account': pProfit/100,
#             'interest rate': round(intRate/100,2),
#             'max number of properties': maxProperties if maxProperties != -1 else np.inf,
#             'residential rental desired monthly net profit': desiredMonthlyProfit
#         }
    
#     def printAccountParams(self):
#         print('\n\n------------ Investment Account Parameters ------------')
#         print('Here are the default values')
#         for key, val in self.accountParams.items():
#             print(f'{key}: {val}')
        
#         print('\nDo you want to have an S&P 500-like investment account in the model?')
#         print('Turning this off affects nothing else')

#         accountActive = getBoolInput('Answer (0 = no    1 = yes): ')
#         self.accountParams['active'] = accountActive

#         if not self.accountParams['active']:
#             return

#         print('\nDo you want to update the Account information?')
#         print('0 = no    1 = yes')
#         if getBoolInput('Answer: '):
#             self.updateAccountInfo()
    
#     def updateAccountInfo(self):
#         print('\n')
#         iBalance = getIntegerInput(
#             'Initial investment account balance (integer): ',
#             validRange = [0, 5000000]
#         )
#         apy = getIntegerInput(
#             'Yearly interest rate (integer 0-100): ',
#             validRange = [0, 100]
#         )
#         cgTax = getIntegerInput(
#             'Capital gains tax (integer-100, typical = 20%): ',
#             validRange = [0, 100]
#         )
#         print('\nMinimum investment account balance')
#         print('No limit to your input, but mind that property down payments are taken')
#         print('from investment account. IE, if your input amount is too high, you may never')
#         print('actually purchase a property.\n')
#         minBalance = getIntegerInput(
#             'Answer (integer): ',
#             validRange = [0, np.inf]
#         )

#         self.accountParams = {
#             'initial balance': iBalance,
#             'yearly interest rate': apy/100,
#             'capital gains tax': cgTax/100,
#             'minimum in account': minBalance
#         }
    
#     def checkDateInput(self, month, year):
#         if year > self.currentYear:
#             return True
        
#         if month < self.currentMonth:
#             return False

#         return True
