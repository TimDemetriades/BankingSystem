# Banking System 
# By: Tim Demetriades
# Date: 06/30/2020

from random import randint
import sys

def randint_with_n_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)

class Banking_System:
    accounts = {}       # dict of accounts created
    current_user = ""   # holds account_identifier after user logs in    
    BIN = 400000        # Bank Identification Number

    def create_account(self):
        user_data = {}  # dict to insert into accounts

        self.account_identifier = str(randint_with_n_digits(9))      
        checksum = str(randint_with_n_digits(1))
        card_number = str(self.BIN) + self.account_identifier + checksum
        card_PIN =  str(randint_with_n_digits(4))

        user_data[self.account_identifier] = {
            'Card Number': card_number,
            'PIN': card_PIN,
            'Balance': 0
        }

        Banking_System.accounts.update(user_data)       # add new account to accounts dict

        print('\nYour card has been created')
        print(f'Your card number:\n{card_number}')
        print(f'Your card PIN:\n{card_PIN}\n')
    
    def log_into_account(self):
        if Banking_System.accounts == {}:       # if no accounts have been made yet
            print('\nYou must create an account first.\n')
        else:
            entered_card = input('\nEnter your card number:\n')
            entered_PIN = input('Enter your PIN:\n')

            account = entered_card[6:15]    # this should match the account_identifier of a card number (digits 6 to 14) 

            if account in Banking_System.accounts:     # if account exists
                if Banking_System.accounts[account]['Card Number'] == entered_card and Banking_System.accounts[account]['PIN'] == entered_PIN:      # and matches correct number and pin
                    print('\nYou have successfully logged in!\n')
                    Banking_System.current_user = account
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
                print(f"\nBalance: {Banking_System.accounts[Banking_System.current_user]['Balance']}\n")
            elif choice == '2':
                Banking_System.current_user = ""
                print('\nYou have successfully logged out!\n')
                break
            elif choice == '0':
                print('\nBye!')
                sys.exit()
            else:
                print('\nPlease enter either 1, 2, or 0 to exit.\n')

banking_system = Banking_System()       # Instance of Banking_System

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