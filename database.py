# Database File
# Holds all functions related to sqlite3 and database

import sqlite3


# Create card table
def create_card_table():
    # define connection and cursor
    connection = sqlite3.connect('card.s3db')   # card database
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
    # close connection
    connection.close()

# Insert cards into card table
def insert_into_card_table(id, number, pin, balance):
    connection = sqlite3.connect('card.s3db')   
    cursor = connection.cursor()
    cursor.execute('INSERT INTO card VALUES (?, ?, ?, ?)', (id, number, pin, balance))   # need to use this format with ? as wildcard
    connection.commit()
    connection.close()

# Check if cards table is empty
def check_if_cards_is_empty():
    connection = sqlite3.connect('card.s3db')   
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(id) FROM card')
    num_of_cards = cursor.fetchone()
    connection.close()
    return num_of_cards

# Check if entered card is in cards table and matches entered pin
def check_card_and_pin(account):
    connection = sqlite3.connect('card.s3db') 
    cursor = connection.cursor()
    cursor.execute('SELECT number, pin FROM card WHERE id = ?', (account,))     # account is digits 6-15 of entered card (value in id column)
    records = cursor.fetchall()
    connection.close()
    return records

# Get balance of account from given user id
def get_balance(user):
    connection = sqlite3.connect('card.s3db')  
    cursor = connection.cursor()
    cursor.execute('SELECT balance FROM card WHERE id = ?', (user,))
    balance = cursor.fetchone()
    connection.close()
    return balance

# Update balance with added income
def add_income_to_db(user, income):
    connection = sqlite3.connect('card.s3db')  
    cursor = connection.cursor()
    cursor.execute('UPDATE card SET balance = balance + ? WHERE id = ?', (income, user))
    connection.commit()
    connection.close()

# Check if entered card exists and not the same as current user
def transfer_check(user, card_entered):
    connection = sqlite3.connect('card.s3db')  
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM card WHERE number = ?', (card_entered,))
    results = cursor.fetchone()
    if not results:                     # if no results found
        print('Such a card does not exist.\n')
        return 1
    elif str(results[0]) == user:       # if id matches that of current user
        print("You can't transfer money to the same acocunt!\n")
        return 1
    connection.close()
    return 0

# Transfer money from balance of one account to another
def do_transfer_db(user, card_entered, amount_to_transfer):
    connection = sqlite3.connect('card.s3db')  
    cursor = connection.cursor()
    cursor.execute('SELECT balance FROM card WHERE id = ?', (user,))
    results = cursor.fetchone()
    if results[0] < amount_to_transfer:     # check if your balance is enough for transfer
        print('Not enough money!')
    else:
        cursor.execute('UPDATE card SET balance = balance - ? WHERE id = ?', (amount_to_transfer, user))
        cursor.execute('UPDATE card SET balance = balance + ? WHERE number = ?', (amount_to_transfer, card_entered))
        print('Success!\n')
        connection.commit()
    connection.close()

# Remove account from card table
def close_account_db(user):
    connection = sqlite3.connect('card.s3db')  
    cursor = connection.cursor()
    cursor.execute('DELETE FROM card WHERE id = ?', (user,))
    connection.commit()
    connection.close()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#Functions for testing
# Display all entries in given table
def show_all_entries(table):
    connection = sqlite3.connect('card.s3db')   
    for row in connection.execute('SELECT rowID, * FROM {}'.format(table)):
        print(row)
    connection.commit()
    connection.close()

# Remove all entries from given table
def delete_all_entries(table):
    connection = sqlite3.connect('card.s3db')  
    cursor = connection.cursor()
    cursor.execute('DELETE FROM {}'.format(table))
    connection.commit()
    connection.close()
