import sys
from Modules import Parameters
from Functions import getDefaultsJSON, validateInteger, validateFloat
from UI import loadUI
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load interface and get basic values
        self.uiSetUp()

        # Set all widget actions
        self.setWidgetActions()

        # Get default inputs
        self.params = Parameters()

        # Hide all error labels 
        self.hideAllErrorLabels()
    
    def uiSetUp(self):
        self.ui = loadUI('MoneyModel.ui', self)

        if not self.ui: # Something went wrong, just leave
            sys.exit()

        self.setCentralWidget(self.ui)
        self.setFixedSize(self.ui.size())

        self.pageCount = self.ui.stackedWidget.count()
        self.goToPage(0)

    def setWidgetDefaults(self, whichPage):
        # Date and city page
        if whichPage == 1:
            self.fillIterableWidget(
                self.ui.cityComboBox, self.params.city.cities
            )
            self.fillIterableWidget(
                self.ui.monthComboBox, self.params.date.dexToMonth
            )
            self.fillIterableWidget(
                self.ui.yearComboBox, 
                range(self.params.date.currentYear, self.params.date.currentYear + 16)
            )
            self.ui.monthComboBox.setCurrentIndex(
                self.params.date.startMonth - 1
            )

        # People and salaries page
        elif whichPage == 2:
            self.fillIterableWidget(
                self.ui.peopleListWidget,
                self.params.defaults['finances']['salaries'],
                'key'
            )
            self.ui.peopleListWidget.setCurrentRow(0)
            self.cycleHasJob()

        # Expenses page
        elif whichPage == 3:
            self.fillIterableWidget(
                self.ui.expensesListWidget,
                self.params.defaults['finances']['expenses'],
                'key'
            )
            self.ui.minMiscExpenseTextEdit.setText(str(
                self.params.defaults['finances']['miscellaneous expense range'][0]
            ))
            self.ui.maxMiscExpenseTextEdit.setText(str(
                self.params.defaults['finances']['miscellaneous expense range'][1]
            ))
            self.ui.expensesListWidget.setCurrentRow(0)

        # Financial account information page
        elif whichPage == 4:
            self.ui.checkingCurrentBalanceTextEdit.setText(str(
                self.params.defaults['finances']['checking account']['initial balance']
            ))
            self.ui.checkingMaxBalanceTextEdit.setText(str(
                self.params.defaults['finances']['checking account']['maximum balance']
            ))
            self.ui.savingsCurrentBalanceTextEdit.setText(str(
                self.params.defaults['finances']['savings account']['initial balance']
            ))
            self.ui.savingsMaxBalanceTextEdit.setText(str(
                self.params.defaults['finances']['savings account']['maximum balance']
            ))

        # Investment property information page
        elif whichPage == 5:
            self.ui.propertiesActiveCheckBox.setChecked(
                self.params.defaults['properties']['active']
            )
            if self.params.defaults['properties']['property type'] == 'vacation':
                self.ui.vacationCheckBox.setChecked(True)
            elif self.params.defaults['properties']['property type'] == 'residential':
                self.ui.residentialCheckBox.setChecked(True)
            
            self.ui.monthsBetweenPurchaseTextEdit.setText(str(
                self.params.defaults['properties']['months between purchase']
            ))
            self.ui.minPropertyPriceTextEdit.setText(str(
                self.params.defaults['properties']['minimum property price']
            ))
            self.ui.maxPropertyPriceTextEdit.setText(str(
                self.params.defaults['properties']['maximum property price']
            ))
            self.ui.percentProfitToAccountTextEdit.setText(str(
                self.params.defaults['properties']['% profit to accounts']
            ))
            self.ui.mortgageInterestRateTextEdit.setText(str(
                self.params.defaults['properties']['interest rate']
            ))
            self.ui.maxNumberOfPropertiesTextEdit.setText(str(
                self.params.defaults['properties']['max # properties']
            ))
            self.ui.residentialProfitTextEdit.setText(str(
                self.params.defaults['properties']['residential desired monthly net']
            ))
            self.cyclePropertiesActive()

        # Investment account information page
        elif whichPage == 6:
            self.ui.investmentAccountActiveCheckBox.setChecked(
                self.params.defaults['investment account']['active']
            )
            self.ui.investmentAccountStartingBalanceTextEdit.setText(str(
                self.params.defaults['investment account']['initial balance']
            ))
            self.ui.investmentAccountInterestRateTextEdit.setText(str(
                self.params.defaults['investment account']['yearly interest rate']
            ))
            self.ui.capitalGainsTaxTextEdit.setText(str(
                self.params.defaults['investment account']['capital gains tax']
            ))
            self.ui.minimumInInvestmentAccountTextEdit.setText(str(
                self.params.defaults['investment account']['minimum in account']
            ))
            self.ui.percentIncomeToAccountTextEdit.setText(str(
                self.params.defaults['finances']['% income to investment account']
            ))

    def fillIterableWidget(self, widg, iterable, keyOrVal = 'val'):
        widg.clear()
        if isinstance(iterable, dict):
            if keyOrVal == 'val':
                iterable = iterable.values()
            elif keyOrVal == 'key':
                iterable = iterable.keys()
            for i in iterable:
                widg.addItem(i)
            
        elif isinstance(iterable, list):
            widg.addItems(iterable)

        elif isinstance(iterable, range):
            for a in iterable:
                widg.addItem(str(a))

    def setJobInformation(self, newPerson, oldPerson):
        if oldPerson is not None:
            # Make sure entries were made/are valid
            if not self.checkPeopleAndSalaries():
                return
            
            # They were valid, update that person's info
            oldPerson = oldPerson.text()
            if oldPerson in self.params.defaults['finances']['salaries']:
                hasJob = self.ui.hasJobCheckbox.isChecked()
                pp = self.ui.propertyPrimaryCheckbox.isChecked()
                if hasJob:
                    salary = self.ui.salaryTextEdit.text()
                    muj = ''
                    swj = ''
                else:
                    salary = ''
                    muj = self.ui.monthsUntilJobTextEdit.text()
                    swj = self.ui.salaryWhenJobStartedTextEdit.text()

                self.params.defaults['finances']['salaries'][oldPerson] = {
                    "has job": hasJob,
                    "months before getting job": muj,
                    "salary when job started": swj,
                    "gross salary": salary,
                    "is primary for property purchase": pp
                    }
        
        # Fill in information for newly selected person
        if newPerson is not None:
            newPerson = newPerson.text()
            vals = self.params.defaults['finances']['salaries'][newPerson]

            self.ui.propertyPrimaryCheckbox.setChecked(
                    vals['is primary for property purchase']
                )
            if vals['has job']:
                self.ui.hasJobCheckbox.setChecked(True)
                self.ui.monthsUntilJobTextEdit.setText('')
                self.ui.salaryWhenJobStartedTextEdit.setText('')
                self.ui.salaryTextEdit.setText(str(vals['gross salary']))
            else:
                self.ui.hasJobCheckbox.setChecked(False)
                self.ui.salaryTextEdit.setText('')
                self.ui.monthsUntilJobTextEdit.setText(str(vals['months before getting job']))
                self.ui.salaryWhenJobStartedTextEdit.setText(
                    str(vals['salary when job started'])
                )
    
    def setExpenseInformation(self, newExpense, oldExpense):
        if oldExpense is not None:
            oldExpense = oldExpense.text()
            if oldExpense in self.params.defaults['finances']['expenses']:
                self.params.defaults['finances']['expenses'][oldExpense] = \
                self.ui.expenseAmountTextEdit.text()
                
        if newExpense is not None:
            newExpense = newExpense.text()
            self.ui.expenseAmountTextEdit.setText(str(
                self.params.defaults['finances']['expenses'][newExpense]
            ))

    def setWidgetActions(self):
        # Navigation buttons
        self.ui.nextButton.clicked.connect(self.nextPage)
        self.ui.backButton.clicked.connect(self.previousPage)
        self.ui.runButton.clicked.connect(self.startRun)

        # Title page
        self.ui.beginButton.clicked.connect(self.nextPage)

        # People and salaries page
        self.ui.peopleListWidget.currentItemChanged.connect(
            self.setJobInformation
        )
        self.ui.hasJobCheckbox.stateChanged.connect(self.cycleHasJob)
        self.ui.addPersonButton.clicked.connect(self.addPerson)
        self.ui.removePersonButton.clicked.connect(self.removePerson)

        # Expenses page
        self.ui.expensesListWidget.currentItemChanged.connect(
            self.setExpenseInformation
        )
        self.ui.addExpenseButton.clicked.connect(self.addExpense)
        self.ui.removeExpenseButton.clicked.connect(self.removeExpense)

        # Investment Property Information page
        self.ui.propertiesActiveCheckBox.stateChanged.connect(
            self.cyclePropertiesActive
        )
        self.ui.residentialCheckBox.stateChanged.connect(
            lambda state: self.cyclePropertyType(state, 'residential')
        )
        self.ui.vacationCheckBox.stateChanged.connect(
            lambda state: self.cyclePropertyType(state, 'vacation')
        )

        # Investment account information page
        self.ui.investmentAccountActiveCheckBox.stateChanged.connect(
            self.cycleInvestmentAccountActive
        )
    
    def cyclePropertiesActive(self):
        state = self.ui.propertiesActiveCheckBox.isChecked()
        self.ui.residentialCheckBox.setEnabled(state)
        self.ui.vacationCheckBox.setEnabled(state)
        self.ui.monthsBetweenPurchaseTextEdit.setEnabled(state)
        self.ui.minPropertyPriceTextEdit.setEnabled(state)
        self.ui.maxPropertyPriceTextEdit.setEnabled(state)
        self.ui.percentProfitToAccountTextEdit.setEnabled(state)
        self.ui.mortgageInterestRateTextEdit.setEnabled(state)
        self.ui.maxNumberOfPropertiesTextEdit.setEnabled(state)

        if state and self.ui.residentialCheckBox.isChecked():
            self.ui.residentialProfitTextEdit.setEnabled(True)
        else:
            self.ui.residentialProfitTextEdit.setEnabled(False)

    def cyclePropertyType(self, state, which):
        # So we don't recursively call this function
        self.ui.residentialCheckBox.blockSignals(True)
        self.ui.vacationCheckBox.blockSignals(True)

        if which == 'residential':
            self.ui.vacationCheckBox.setChecked(not state)
            self.ui.residentialProfitTextEdit.setEnabled(state)
        else:
            self.ui.residentialCheckBox.setChecked(not state)
            self.ui.residentialProfitTextEdit.setEnabled(not state)            

        self.ui.residentialCheckBox.blockSignals(False)
        self.ui.vacationCheckBox.blockSignals(False)
    
    def cycleInvestmentAccountActive(self):
        state = self.ui.investmentAccountActiveCheckBox.isChecked()
        self.ui.investmentAccountStartingBalanceTextEdit.setEnabled(state)
        self.ui.investmentAccountInterestRateTextEdit.setEnabled(state)
        self.ui.capitalGainsTaxTextEdit.setEnabled(state)
        self.ui.minimumInInvestmentAccountTextEdit.setEnabled(state)
        self.ui.percentIncomeToAccountTextEdit.setEnabled(state)

    def addPerson(self):
        self.params.defaults['finances']['total persons'] += 1
        numPeople = self.params.defaults['finances']['total persons']
        self.params.defaults['finances']['salaries'][f'person {numPeople}'] = {
            'has job': False,
            'months before getting job': '',
            'salary when job started': '',
            'gross salary': '',
            'is primary for property purchase': False
        }
        self.fillIterableWidget(
            self.ui.peopleListWidget,
            self.params.defaults['finances']['salaries'],
            'key'
        )
        self.ui.peopleListWidget.setCurrentRow(numPeople - 1)
    
    def removePerson(self):
        person = self.ui.peopleListWidget.currentItem().text()
        del self.params.defaults['finances']['salaries'][person]
        self.params.defaults['finances']['total persons'] -= 1
        self.fillIterableWidget(
            self.ui.peopleListWidget,
            self.params.defaults['finances']['salaries'],
            'key'
        )
        self.ui.peopleListWidget.setCurrentRow(0)

    def addExpense(self):
        a = 1
        while True:
            name = f'New Expense {a}'
            if name not in self.params.defaults['finances']['expenses']:
                break
            a += 1
        self.params.defaults['finances']['expenses'][name] = 0
        self.fillIterableWidget(
            self.ui.expensesListWidget,
            self.params.defaults['finances']['expenses'],
            'key'
        )
        self.ui.expensesListWidget.setCurrentRow(
            len(self.params.defaults['finances']['expenses']) - 1
        )
    
    def removeExpense(self):
        expense = self.ui.expensesListWidget.currentItem().text()
        del self.params.defaults['finances']['expenses'][expense]
        self.fillIterableWidget(
            self.ui.expensesListWidget,
            self.params.defaults['finances']['expenses'],
            'key'
        )

    def cycleHasJob(self):
        state = self.ui.hasJobCheckbox.isChecked()
        self.ui.salaryTextEdit.setEnabled(state)
        self.ui.monthsUntilJobTextEdit.setEnabled(not state)
        self.ui.salaryWhenJobStartedTextEdit.setEnabled(not state)
        

    def nextPage(self):
        currentIndex = self.ui.stackedWidget.currentIndex()

        if not self.checkInputs(currentIndex):
            return
        
        newIndex = currentIndex + 1
        self.setWidgetDefaults(newIndex)
        self.goToPage(newIndex)
    
    def previousPage(self):
        currentIndex = self.ui.stackedWidget.currentIndex()
        newIndex = currentIndex - 1
        self.goToPage(newIndex)
    
    def goToPage(self, newIndex):
        if newIndex < 0 or newIndex > self.pageCount-1:
            return
        
        self.ui.stackedWidget.setCurrentIndex(newIndex)

        if newIndex == 0:
            self.ui.backButton.hide()
            self.ui.runButton.hide()
            self.ui.nextButton.hide()
        else:
            self.ui.backButton.show()
            self.ui.runButton.show()
            self.ui.nextButton.show()

        if newIndex == 1:
            self.ui.backButton.setEnabled(False)
        else:
            self.ui.backButton.setEnabled(True)

        if newIndex == self.pageCount - 1:
            self.ui.runButton.setEnabled(True)
            self.ui.nextButton.setEnabled(False)
        else:
            self.ui.runButton.setEnabled(False)
            self.ui.nextButton.setEnabled(True)

    def startRun(self):
        pass

    def checkInputs(self, whichPage):
        # Splash page, nothing to do
        if whichPage == 0:
            return True
        
        # City and date page
        if whichPage == 1: 
            self.ui.dateAndCityErrorLabel.setText('')
            return self.checkCityAndDate()

        # People and salaries page
        elif whichPage == 2:
            self.ui.peopleAndSalariesErrorLabel.setText('')
            return self.checkPeopleAndSalaries()
        
        else:
            return True
    
    def hideAllErrorLabels(self):
        for label in self.ui.findChildren(QLabel):
            if label.objectName().endswith('ErrorLabel'):
                label.setText('')

    def activateErrorLabel(self, reason):
        # Date and city reasons
        if reason == 'invalid date':
            self.ui.dateAndCityErrorLabel.setText(
                'Current Year Selected:\nMust Choose Current or Future Month!'
            )
        
        # People and salaries reasons
        elif reason == 'must have salary':
            self.ui.peoplAndSalariesErrorLabel.setText(
                'Person has job!\nMust provide salary!'
            )
        elif reason == 'salary float':
            self.ui.peopleAndSalariesErrorLabel.setText(
                'Salary Input Must be Float!'
            )
        elif reason == 'must have muj':
            self.ui.peopleAndSalariesErrorLabel.setText(
                'Person does not have job!\nMust provide Months Until Getting Job!'
            )
        elif reason == 'muj int':
            self.ui.peopleAndSalariesErrorLabel.setText(
                'Months Until Job Input Must Be Integer!'
            )
        elif reason == 'must have swj':
            self.ui.peopleAndSalariesErrorLabel.setText(
                'Person does not have job!\nMust provide Salary When Job Started!'
            )
        elif reason == 'swj float':
            self.ui.peopleAndSalariesErrorLabel.setText(
                'Salary When Job Started Input Must be Float!'
            )

    def updateParams(self, whichPage):
        # City and date page
        if whichPage == 1:
            self.params.updateDate(
                self.ui.monthComboBox.currentText(),
                self.ui.yearComboBox.currentText()
            )
            self.params.updateCity(self.ui.cityComboBox.currentText())
        
    def checkCityAndDate(self):
        # Check that the date is ok
        month = self.ui.monthComboBox.currentText()
        year = self.ui.yearComboBox.currentText()

        if not self.params.date.checkDate(month, year):
            self.activateErrorLabel('invalid date')
            return False
        
        self.params.updateDate(month, year)
        self.params.updateCity(self.ui.cityComboBox.currentText())

        return True

    def checkPeopleAndSalaries(self):
        if self.ui.hasJobCheckbox.isChecked():
            salary = self.ui.salaryTextEdit.text()
            if len(salary) == 0 :
                self.activateErrorLabel('must have salary')
                return False
            elif not validateFloat(salary):
                self.activateErrorLabel('salary float')
                return False    
            return True
        else:
            muj = self.ui.monthsUntilJobTextEdit.text()
            if len(muj) == 0:
                self.activateErrorLabel('must have muj')
                return False
            elif not validateInteger(muj):
                self.activateErrorLabel('muj int')
                return False
            
            swj = self.ui.salaryWhenJobStartedTextEdit.text()
            if len(swj) == 0:
                self.activateErrorLabel('must have swj')
                return False
            elif not validateFloat(swj):
                self.activateErrorLabel('swj float')
                return False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    
