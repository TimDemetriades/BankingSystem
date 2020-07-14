# Banking System 
# By: Tim Demetriades
# Date: 06/30/2020

from random import randint
import sys

import database


# Create the card table if not already created
database.create_card_table()

# Show all rows in card table
# database.show_all_entries('card')

# Remove all entries from card table
# database.delete_all_entries('card')


class BankingSystem:
    current_user = ""   # holds account_identifier after user logs in    
    BIN = 400000        # Bank Identification Number

    def create_account(self):
        self.account_identifier = str(randint_with_n_digits(9))      
        self.card_number = str(self.BIN) + self.account_identifier
        self.card_number = self.card_number + self.calc_checksum(self.card_number)
        self.card_PIN =  str(randint_with_n_digits(4))
        self.balance = 0

        database.insert_into_card_table(self.account_identifier, self.card_number, self.card_PIN, self.balance)     # insert new card into db

        print('\nYour card has been created')
        print(f'Your card number:\n{self.card_number}')
        print(f'Your card PIN:\n{self.card_PIN}\n')

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
        num_of_cards = database.check_if_cards_is_empty()
        if num_of_cards[0] == 0:
            print('\nYou must create an account first.\n')
        else:
            entered_card = input('\nEnter your card number:\n')
            entered_PIN = input('Enter your PIN:\n')

            account = entered_card[6:15]    # this should match the account_identifier of a card number (digits 6 to 14) and also the id column

            records = database.check_card_and_pin(account)
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
                balance = database.get_balance(BankingSystem.current_user)
                print(f"\nBalance: {balance[0]}\n")
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
