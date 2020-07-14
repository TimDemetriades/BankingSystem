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
    connection = sqlite3.connect('card.s3db')   # card database
    cursor = connection.cursor()
    cursor.execute('INSERT INTO card VALUES (?, ?, ?, ?)', (id, number, pin, balance))   # need to use this format with ? as wildcard
    connection.commit()
    connection.close()

# Check if cards table is empty
def check_if_cards_is_empty():
    connection = sqlite3.connect('card.s3db')   # card database
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(id) FROM card')
    num_of_cards = cursor.fetchall()
    connection.close()
    return num_of_cards

# Check if entered card is in cards table and matches entered pin
def check_card_and_pin(account):
    connection = sqlite3.connect('card.s3db')   # card database
    cursor = connection.cursor()
    cursor.execute('SELECT number, pin FROM card WHERE id = ?', (account,))
    records = cursor.fetchall()
    connection.close()
    return records

# Get balance of account from given user id
def get_balance(user):
    connection = sqlite3.connect('card.s3db')   # card database
    cursor = connection.cursor()
    cursor.execute('SELECT balance FROM card WHERE id = ?', (user,))
    balance = cursor.fetchone()
    connection.close()
    return balance

# Display all entries in given table
def show_all_entries(table):
    connection = sqlite3.connect('card.s3db')   # card database
    for row in connection.execute('SELECT rowID, * FROM {}'.format(table)):
        print(row)
    connection.commit()
    connection.close()

# Remove all entries from given table
def delete_all_entries(table):
    connection = sqlite3.connect('card.s3db')   # card database
    cursor = connection.cursor()
    cursor.execute('DELETE FROM {}'.format(table))
    connection.commit()
    connection.close()
