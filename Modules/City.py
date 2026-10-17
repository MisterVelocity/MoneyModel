import numpy as np

class City():
    def __init__(self, initialCity = 'Barcelona'):
        self.cities = {
        0: 'Barcelona',
        1: 'Berlin', 
        2: 'Geneva', 
        3: 'Paris',
        4: 'Lisbon',
        5: 'Amsterdam',
        6: 'London',
        7: 'Rome'
        }

        self.updateInfo(initialCity)

    def updateInfo(self, city):
        self.city = city
        self.getTaxes()
        self.getExpenses()
        self.getPropertyInfo()

    def getTaxes(self):
        if self.city == 'Barcelona':
            basicAllowance = 5550
            taxedOnGross = {
                '%': [0.0635],
                'cap': [54000]
            }
            brackets = [
            (0, 12450, 0.19),
            (12451, 20200, 0.24),
            (20201, 35200, 0.30),
            (35201, 60000, 0.37),
            (60001, 300000, 0.45),
            (300001, np.inf, 0.47)
            ]
  
        elif self.city == 'Berlin':
            basicAllowance = 10908
            taxedOnGross = {
                '%': [0.2, 0.1],
                'cap': [59850, 87600]
            }
            brackets = [
                (0, 10908, 0),
                (10909, 62809, 0.35),
                (62810, 277825, 0.42),
                (277826, np.inf, 0.45)
            ]
        elif self.city == 'Geneva':
            basicAllowance = 12790
            taxedOnGross = {
                '%': [0.055],
                'cap': [np.inf]
            }
            brackets = [
                (0, 14500, 0),
                (14501, 31600, 0.008),
                (31601, 44200, 0.015),
                (44201, 77400, 0.04),
                (77401, 103600, 0.06),
                (103601, 134600, 0.07),
                (134601, 176000, 0.09),
                (176001, np.inf, 0.115)
            ]
        elif self.city == 'Paris':
            basicAllowance = 0
            taxedOnGross = {
                '%': [0.225],
                'cap': [44000]
            }
            brackets = [
                (0, 10777, 0),
                (10778, 27478, 0.11),
                (27479, 78570, 0.30),
                (78571, 168994, 0.41),
                (168995, np.inf, 0.45)
            ]
        elif self.city == 'Lisbon': 
            basicAllowance = 4104
            taxedOnGross = {
                '%': [0.11],
                'cap': [np.inf]
            }
            brackets = [
                (0, 7479, 0.145),
                (7480, 11284, 0.23),
                (11285, 15992, 0.265),
                (15993, 20700, 0.285),
                (20701, 26355, 0.35),
                (26356, 38632, 0.37),
                (38633, 50483, 0.435),
                (50484, np.inf, 0.48)
            ]
        elif self.city == 'Amsterdam':
            basicAllowance = 0
            taxedOnGross = {
                '%': [0.2765],
                'cap': [39000]
            }
            brackets = [
                (0, 73031, 0.3693),
                (73032, np.inf, 0.4950)
            ]
        elif self.city == 'London':
            basicAllowance = 12570
            taxedOnGross = {
                '%': [0.12, 0.02],
                'cap': [50270, np.inf]
            }
            brackets = [
                (0, 14456, 0),
                (14457, 57811, 0.20),
                (57812, 143911, 0.40),
                (143912, np.inf, 0.45)
            ]
        elif self.city == 'Rome':
            basicAllowance = 0
            taxedOnGross = {
                '%': [0.09],
                'cap': [105000]
            }
            brackets = [
                (0, 15000, 0.23),
                (15001, 28000, 0.25),
                (28001, 50000, 0.35),
                (50000, np.inf, 0.43)
            ]

        self.taxes = {
            'basic allowance': basicAllowance,
            'taxed on gross': taxedOnGross,
            'tax brackets': brackets
        }

    def getExpenses(self):
        if self.city == 'Barcelona':
            self.expenses = {
                'rent': 1800,
                'internet': 30,
                'phones': 30,
                'groceries': 600,
                'utilities': 180,
                'transportation': 100,
                'childcare': 200
            }
        elif self.city == 'Berlin':
            self.expenses = {
                'rent': 1600,
                'internet': 30,
                'phones': 30,
                'groceries': 550,
                'utilities': 200,
                'transportation': 100,
                'childcare': 300
            }
        elif self.city == 'Geneva':
            self.expenses = {
                'rent': 2500,
                'internet': 40,
                'phones': 20,
                'groceries': 700,
                'utilities': 250,
                'transportation': 150,
                'childcare': 700
            }
        elif self.city == 'Paris':
            self.expenses = {
                'rent': 2000,
                'internet': 30,
                'phones': 20,
                'groceries': 600,
                'utilities': 200,
                'transportation': 120,
                'childcare': 400
            }
        elif self.city == 'Lisbon':
            self.expenses = {
                'rent': 1400,
                'internet': 25,
                'phones': 15,
                'groceries': 500,
                'utilities': 150,
                'transportation': 80,
                'childcare': 300
            }
        elif self.city == 'Amsterdam':
            self.expenses = {
                'rent': 2000,
                'internet': 30,
                'phones': 20,
                'groceries': 600,
                'utilities': 250,
                'transportation': 120,
                'childcare': 500
            }
        elif self.city == 'London':
            self.expenses = {
                'rent': 2400,
                'internet': 35,
                'phones': 25,
                'groceries': 650,
                'utilities': 250,
                'transportation': 200,
                'childcare': 800
            }
        elif self.city == 'Rome':
            self.expenses = {
                'rent': 1500,
                'internet': 30,
                'phones': 20,
                'groceries': 550,
                'utilities': 180,
                'transportation': 100,
                'childcare': 400
            }
    
    def getPropertyInfo(self):
        if self.city == 'Barcelona':
            self.propertyInfo = {
                'interest': [0.03, 0.04],
                'price': [300000, 600000],
                'down': 0.20,
                'propertyTax': 0.008,
                'insurance': 500,
                'term': 25,
                'occupancy': [0.60, 0.85],
                'daily rate': [100, 250],
            }
        elif self.city == 'Berlin':
            self.propertyInfo = {
                'interest': [0.03, 0.04],
                'price': [350000, 700000],
                'down': 0.20,
                'propertyTax': 0.005,
                'insurance': 300,
                'term': 25,
                'occupancy': [0.50, 0.85],
                'daily rate': [80, 200],
            }
        elif self.city == 'Geneva':
            self.propertyInfo = {
                'interest': [0.02, 0.03],
                'price': [900000, 1500000],
                'down': 0.20,
                'propertyTax': 0.008,
                'insurance': 600,
                'term': 25,
                'occupancy': [0.50, 0.85],
                'daily rate': [100, 250],
            }
        elif self.city == 'Paris':
            self.propertyInfo = {
                'interest': [0.03, 0.04],
                'price': [450000, 900000],
                'down': 0.10,
                'propertyTax': 0.01,
                'insurance': 400,
                'term': 25,
                'occupancy': [0.50, 0.90],
                'daily rate': [110, 500],
            }
        elif self.city == 'Lisbon':
            self.propertyInfo = {
                'interest': [0.035, 0.04],
                'price': [250000, 600000],
                'down': 0.20,
                'propertyTax': 0.005,
                'insurance': 300,
                'term': 30,
                'occupancy': [0.60, 0.90],
                'daily rate': [80, 280],
            }
        elif self.city == 'Amsterdam':
            self.propertyInfo = {
                'interest': [0.04, 0.05],
                'price': [400000, 800000],
                'down': 0.10,
                'propertyTax': 0.002,
                'insurance': 400,
                'term': 30,
                'occupancy': [0.50, 0.85],
                'daily rate': [150, 300],
            }
        elif self.city == 'London':
            self.propertyInfo = {
                'interest': [0.04, 0.05],
                'price': [500000, 1300000],
                'down': 0.10,
                'propertyTax': 0.003,
                'insurance': 500,
                'term': 25,
                'occupancy': [0.50, 0.90],
                'daily rate': [90, 450],
            }
        elif self.city == 'Rome':
            self.propertyInfo = {
                'interest': [0.03, 0.04],
                'price': [300000, 550000],
                'down': 0.20,
                'propertyTax': 0.01,
                'insurance': 350,
                'term': 25,
                'occupancy': [0.60, 0.90],
                'daily rate': [100, 350],
            }


# if self.city == 'Barcelona':
            
# elif self.city == 'Berlin':
    
# elif self.city == 'Geneva':
    
# elif self.city == 'Paris':
    
# elif self.city == 'Lisbon':
    
# elif self.city == 'Amsterdam':
    
# elif self.city == 'London':
    
# elif self.city == 'Rome':