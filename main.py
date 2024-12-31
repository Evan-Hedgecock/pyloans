from loan import Loan
import sqlite3

def main():
    print('Welcome to your loan manager!\n\nWhat would you like to do?')
    print()

    while(True):
        loans = loadLoans()
        selection = -1
        try:
            printMenu()
            print()
            selection = int(input('Enter menu number: '))
            print()
        except:
            print()
            printMenu()
            print()
            print('Only enter number.')
            try:
                selection = int(input('Enter menu number: '))
            except:
                continue

        if selection == 1:
            viewLoans(loans)

        if selection == 2:
            addLoan()
        
        if selection == 5:
            break


def printMenu():
     print('1) View Loans\n' +
           '2) Add Loans\n' +
           '3) Edit Loans\n' +
           '4) Simulate Loan Payments\n' +
           '5) Quit')

def viewLoans(loans):
    totalBalance = 0
    print('id | name | balance | percent')
    for loan in loans:
        totalBalance += loan.getBalance()
        print(f'{loan.id} | {loan.name} | ${loan.getBalance()} | {loan.percent}%')
    print(f'\nTotal balance: ${totalBalance}')
    print()
        


def addLoan():
    name = None
    amount = None
    percent = None
    interest = None
    expense = None
    
    while name == None:
        name = input('Enter loan name: ')
        if name == '':
            name = None
            print('\nCannot leave blank')

    while amount == None:
        try:
            amount = float(input('Enter loan amount: '))
        except:
            amount = None
            print('\nInvalid entry, only valid decimal point values allowed')

    while percent == None:
        try:
            percent = float(input('Enter interest rate: '))
        except:
            percent = None
            print('\nInvalid entry, only valid decimal point values allowed')

    selection = input('Does this loan have accrued interest? [y/N](Default=N) ')
    if selection.lower() == 'y':
        while interest == None:
            try:
                interest = float(input('Enter accrued interest: '))
            except:
                interest = None
                print('\nInvalid entry, only valid decimal point values allowed')
    else:
        print('Setting accrued interest to 0')
        print('You can edit this loan to change later\n')

    selection = input('Would you like to include any interest' + 
                      ' you have already paid? [y/N](Default=N) ')
    if selection.lower() == 'y':
        while expense == None:
            try:
                expense = float(input('Enter past paid interest: '))
            except:
                expense = None
                print('\nInvalid entery, only valid decimal point values allowed')
    else:
        print('Setting interest expense to 0')
        print('You can add any past paid interest to this loan later\n')

    if interest != None:
        amount -= interest

    loan = Loan(name, amount, percent, interest, expense)
    print(f'Created new loan:\n{loan}')
    print()
    saveLoan(loan)


# Load loans from ./loans.db
def loadLoans():
    con = sqlite3.connect('loans.db')
    cur = con.cursor()
    # interest = accrued interest
    # expense = interest expense
    # percent = interest APR
    cur.execute('''
        CREATE TABLE IF NOT EXISTS loans(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            principal REAL NOT NULL,
            interest REAL,
            expense REAL,
            percent REAL NOT NULL,
            lastUpdate TEXT
           )
    ''')    

    loans = []
    for row in cur.execute('SELECT * FROM loans'):
        loans.append(Loan(row[1], row[2], row[3], row[4], row[5], row[0]))

    return loans
        
def saveLoan(loan):
    con = sqlite3.connect('loans.db')
    cur = con.cursor()
    cur.execute('INSERT INTO loans(name, principal, interest, expense, percent, lastUpdate)' +
                ' VALUES(?, ?, ?, ?, ?, ?)', loan.dataArray())
    con.commit()


main()
