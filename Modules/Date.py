import datetime

class Date():
    def __init__(self, monthAdd):
        self.dexToMonth = {
            1: 'Jan',
            2: 'Feb',
            3: 'Mar',
            4: 'Apr',
            5: 'May',
            6: 'Jun',
            7: 'Jul',
            8: 'Aug',
            9: 'Sep',
            10: 'Oct',
            11: 'Nov',
            12: 'Dec'
        }

        self.monthToDex = {
            'Jan': 1,
            'Feb': 2,
            'Mar': 3,
            'Apr': 4,
            'May': 5,
            'Jun': 6,
            'Jul': 7,
            'Aug': 8,
            'Sep': 9,
            'Oct': 10,
            'Nov': 11,
            'Dec': 12
        }

        self.now = datetime.datetime.now()

        self.currentMonth = self.now.month
        self.currentYear = self.now.year

        self.initStartEndDates(monthAdd)
    
    def cycleMonth(self):
        self.currentMonth, self.currentYear = self.lapYear(
            self.currentMonth + 1,
            self.currentYear
        )
    
    def initStartEndDates(self, monthAdd):
        self.startMonth, self.startYear = self.lapYear(
            self.currentMonth + monthAdd,
            self.currentYear
        )

        self.endMonth = self.startMonth
        self.endYear = self.startYear + 35

    def updateStartEndDates(self, month, year):
        if isinstance(month, str):
            month = self.monthToDex[month]
        if isinstance(year, str):
            year = int(year)

        if not self.checkDate(month, year):
            return False

        self.startMonth = month
        self.startYear = year

        self.endMonth = month
        self.endYear = year + 35

        return True

    def lapYear(self, month, year):
        if month > 12:
            return month - 12, year + 1
        return month, year
    
    def checkDate(self, month, year):
        if isinstance(month, str):
            month = self.monthToDex[month]
        if isinstance(year, str):
            year = int(year)
        if month < self.currentMonth and year == self.currentYear:
            return False
        return True