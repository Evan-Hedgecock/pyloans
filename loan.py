import sqlite3

# Load loans from ./loans.db
def loadLoans():
    con = sqlite3.connect('loans.db')
    cur = con.cursor()
    f = open('loans.db')
    try:
        if f.read() == '':
            print('Creating loans.db')
            cur.execute('CREATE TABLE loans(id, name, balance, interest)')
    except UnicodeDecodeError:
       print('loans.db already created') 
