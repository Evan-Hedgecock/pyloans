import loan
import sys

def main():

    loan.loadLoans()

    print('Welcome to your loan manager!\n\nWhat would you like to do?')
    print()
    selection = -1

    while(selection < 1 or selection > 5):
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


def printMenu():
     print('1) View Loans\n' +
           '2) Add Loans\n' +
           '3) Edit Loans\n' +
           '4) Simulate Loan Payments\n' +
           '5) Quit')

main()



