import sqlite3
import tkinter as tk
import RPi.GPIO as GPIO
import time
from mfrc522 import SimpleMFRC522

GPIO.setmode(GPIO.BOARD)


def init_db():
    conn = sqlite3.connect('cards.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS cardholder(id INTEGER PRIMARY KEY ,
                   card_id TEXT UNIQUE NOT NULL,
                   name TEXT)
                                ''')
    conn.commit()
    conn.close()

def load_names():
    try:
        with open('names.txt', 'r') as file:
            names = [line.strip() for line in file.readlines()]
        return names
    except FileNotFoundError:
        print('Not found')

def add_card(card_id,name):
    conn = sqlite3.connect('cards.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''INSERT INTO cardholder (card_id, name)
                       VALUES (?,?)''',(card_id,name))
        conn.commit()
        
    except sqlite3.IntegrityError:
        print('Ez a kártya már létezik')
    conn.close()

def main():
    init_db()
    names = load_names()
    reader = SimpleMFRC522()
    print('Touch the card to the reader...')
    try:
        while names:
            print('Belépve')
            card_id,_ = reader.read()
           
            if card_id:
                conn = sqlite3.connect('cards.db')
                cursor = conn.cursor()
                cursor.execute('''SELECT name FROM cardholder
                               WHERE card_id = ?''',(card_id,))
                result = cursor.fetchone()
                conn.close()
                if result:
                    print('Ez a kártya már létezik')
                else:
                    if names: 
                        name = names.pop(0)
                        add_card(card_id,name)
                        print('Hozzáadva {name}')
                    else: print('No names')
                    time.sleep(2)

            print('Waiting for the next card...')
    except KeyboardInterrupt:
        GPIO.cleanup()

main()