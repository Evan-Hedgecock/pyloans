import datetime

class Loan:
 
    def __init__(self, name, amount, percent, interest, expense, loanId=None):
        self.name = name
        self.principal = amount

        # Interest percent
        self.percent = percent 

        # Accrued interest
        if interest == None:
            self.interest = 0
        else:
            self.interest = interest 

        # Interest expense
        if expense == None:
            self.expense = 0
        else:
            self.expense = expense 
        
        # Used to track amount of days to accrue interest
        self.lastUpdate = datetime.date.today()
        self.id = loanId
        
    def __str__(self):
        total = self.getBalance()
        return f'{self.name}: {total} @ {self.percent}%'

    def makePayment(self, payment):
        # Make payment to principal first
        self.principal -= payment
        # Leftover amount goes to interest
        if self.principal < 0:
            self.interest += self.principal
            self.principal == 0

    # Interest is accrued daily (365 days)
    # Interest is accrued only based on principal
    def accrueInterest(self, days=None):
        today = datetime.date.today()
        if today == self.lastUpdate:
            return 

        # Will accrue days since last update unless days are provided
        if days == None:
            accrueDays = (today - self.lastUpdate).days
        else:
            accrueDays = days

        for i in range(accrueDays):
            dailyInterest = (self.principal * self.percent) / 365
            self.interest += dailyInterest
            self.expense += dailyInterest
   
    def getBalance(self):
        return self.principal + self.interest

    def dataArray(self):
        return [self.name, self.principal, self.percent,
                self.interest, self.expense, str(self.lastUpdate)]
