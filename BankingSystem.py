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
    def __init__(self):
        self.card_number = None
        self.card_PIN = None
        self.balance = 0

    def create_account(self):
        BIN = 400000        # Bank Identification Number
        account_identifier = randint_with_n_digits(9)      
        checksum = randint_with_n_digits(1)
        self.card_number = str(BIN) + str(account_identifier) + str(checksum)

        self.card_PIN =  str(randint_with_n_digits(4))

        print('\nYour card has been created')
        print(f'Your card number:\n{self.card_number}')
        print(f'Your card PIN:\n{self.card_PIN}\n')
    
    def log_into_account(self):
        if self.card_number == None or self.card_PIN == None:
            print('\nYou must create an account first.\n')
        else:
            entered_card = input('\nEnter your card number:\n')
            entered_PIN = input('Enter your PIN:\n')

            if entered_card == self.card_number and entered_PIN == self.card_PIN:
                print('\nYou have successfully logged in!\n')
                self.account()
            else:
                print('\nWrong card number or PIN!\n')
            
    def account(self):
        while True:
            print('1. Balance')
            print('2. Log out')
            print('0. Exit')
            choice = input()

            if choice == '1':
                print(f'\nBalance: {self.balance}\n')
            elif choice == '2':
                print('\nYou have successfully logged out!\n')
                break
            elif choice == '0':
                print('\nBye!')
                sys.exit()

banking_system = Banking_System()

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