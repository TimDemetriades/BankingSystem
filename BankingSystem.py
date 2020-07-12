# Banking System 
# By: Tim Demetriades
# Date: 06/30/2020

from random import randint
import sqlite3   
import sys


# define connection and cursor
connection = sqlite3.connect('card.s3db')   # cards database
cursor = connection.cursor()

# create table query
create_card_table = '''CREATE TABLE IF NOT EXISTS 
    card (
    id INTEGER,
    number TEXT,
    pin TEXT,
    balance INTEGER DEFAULT 0
    );'''

# execute query
cursor.execute(create_card_table)

# commit changes
connection.commit()


class BankingSystem:
    current_user = ""   # holds account_identifier after user logs in    
    BIN = 400000        # Bank Identification Number

    def create_account(self):
        self.account_identifier = str(randint_with_n_digits(9))      
        self.card_number = str(self.BIN) + self.account_identifier
        self.card_number = self.card_number + self.calc_checksum(self.card_number)
        self.card_PIN =  str(randint_with_n_digits(4))
        self.balance = 0

        self.insert_into_card_table(self.account_identifier, self.card_number, self.card_PIN, self.balance)     # insert into db

        print('\nYour card has been created')
        print(f'Your card number:\n{self.card_number}')
        print(f'Your card PIN:\n{self.card_PIN}\n')

    def insert_into_card_table(self, id, number, pin, balance):
        cursor.execute('INSERT INTO card VALUES (?, ?, ?, ?)',(id, number, pin, balance))   # need to use this format with ?
        connection.commit()

    def calc_checksum(self, card_number):
        # using luhn algorithm
        sum = 0

        for counter, digit in enumerate(card_number, 1):        # start counter at 1
            n = int(digit)                                      # convert string to int
            if counter % 2  == 1 and n * 2 > 9:                 # if counter is odd and over 9 after doubling
                sum += n * 2 - 9
            elif counter % 2 == 1:                              # if counter is odd and less than 9
                sum += n * 2
            else:                                               # if counter is even
                sum += n

        if sum % 10 == 0:
            return str(0)                                       # checksum is 0
        else:
            return str(10 - sum % 10)                           # checksum is remainder to next number divisible by 10

    def log_into_account(self):
        cursor.execute('SELECT COUNT(id) FROM card')
        num_of_cards = cursor.fetchall()
        if num_of_cards == [(0,)]:
            print('\nYou must create an account first.\n')
        else:
            entered_card = input('\nEnter your card number:\n')
            entered_PIN = input('Enter your PIN:\n')

            account = entered_card[6:15]    # this should match the account_identifier of a card number (digits 6 to 14) and also the id column

            cursor.execute('SELECT number, pin FROM card WHERE id = ?', (account,))
            records = cursor.fetchall()
            if records != []:
                if records[0][0] == entered_card and records[0][1] == entered_PIN:
                    print('\nYou have successfully logged in!\n')
                    BankingSystem.current_user = account
                    self.account()
                else:
                    print('\nWrong card number or PIN!\n')
            else:
                print('\nWrong card number or PIN!\n')
            
    def account(self):
        while True:
            print('1. Balance')
            print('2. Log out')
            print('0. Exit')
            choice = input()

            if choice == '1':
                cursor.execute('SELECT balance FROM card WHERE id = ?', BankingSystem.current_user)
                balance = cursor.fetchall()
                print(f"\nBalance: {balance}\n")
            elif choice == '2':
                BankingSystem.current_user = ""
                print('\nYou have successfully logged out!\n')
                break
            elif choice == '0':
                print('\nBye!')
                sys.exit()
            else:
                print('\nPlease enter either 1, 2, or 0 to exit.\n')


def randint_with_n_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)

banking_system = BankingSystem()       # Instance of BankingSystem

# Main Loop
while True:
    print('1. Create an account')
    print('2. Log into account')
    print('0. Exit')
    choice = input()

    if choice == '1':
        banking_system.create_account()
    elif choice == '2':
        banking_system.log_into_account()
    elif choice == '0':
        print('\nBye!')
        break
    else:
        print('Please enter either 1, 2, or 0 to exit.')
