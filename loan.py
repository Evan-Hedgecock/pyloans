import datetime
import sqlite3

class Loan:
 
    def __init__(self, name, amount, interest, expense, percent, lastUpdate=None, loanId=None):
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
        if lastUpdate == None:
            self.lastUpdate = datetime.date.today()
        else:
            date = ['', '', '']
            i = 0 
            for c in lastUpdate:
                if c == '-':
                    i += 1
                else:
                    date[i] += c
            self.lastUpdate = datetime.date(int(date[0]), int(date[1]), int(date[2]))
                

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
            dailyInterest = (self.principal * (self.percent / 100)) / 365
            dailyInterest = int(dailyInterest * 100) / 100 # Truncate to two decimal places without rounding
            self.interest += dailyInterest
            self.expense += dailyInterest
            self.interest = float(f'{self.interest:.2f}')
            self.expense = float(f'{self.expense:.2f}')
        self.lastUpdate = today
        self.updateLoan()
   
    def getBalance(self):
        return self.principal + self.interest

    def dataArray(self):
        return [self.name, self.principal, self.interest,
                self.expense, self.percent, str(self.lastUpdate)]

    def updateLoan(self):
        data = [self.name, self.principal, self.percent,
                self.interest, self.expense, self.lastUpdate, self.id]
        con = sqlite3.connect('loans.db')
        cur = con.cursor()

        cur.execute('''
        UPDATE loans
        SET name = ?,
            principal = ?,
            percent = ?,
            interest = ?,
            expense = ?,
            lastUpdate = ?
        WHERE id = ?
        ''', data)
        con.commit()
