import sqlite3
import tkinter as tk
import RPi.GPIO as GPIO
import time
from tkinter import messagebox
from mfrc522 import SimpleMFRC522
from PIL import Image,ImageTk
GPIO.setmode(GPIO.BOARD)
GPIO.setup(26,GPIO.OUT,initial=0)
GPIO.setup(22,GPIO.OUT,initial=0)


class reader:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Card check')
        self.root.geometry('600x400')
        
        self.label = tk.Label(self.root,text='Please tap your card!', font=('Arial', 20))
        self.label.place(relx=0.5, rely=0.2, anchor='center')
        
        self.result_label = tk.Label(self.root, text='', font=('Arial',20),justify=tk.CENTER)
        self.result_label.place(relx=0.5, rely=0.5, anchor='center')
    

        self.reader = SimpleMFRC522()

        #self.root.protocol('WM_DELETE_WINDOW', self.on_closing)
            
        self.root.after(1000,self.card_read)

        self.root.mainloop()
        
    def card_read(self):
            
            card_id = None
            print(card_id)
            while card_id is None:      
                card_id, _ = self.reader.read()
                print(card_id)
            self.card_check(card_id)
            time.sleep(4)
            self.root.after(1000,self.card_read)
            
    def card_check(self,id):
        conn = sqlite3.connect('cards.db')
        c = conn.cursor()

        c.execute('''SELECT * from CARDHOLDER
                  WHERE card_id = ?''', (id,))
        result = c.fetchone()
        print(result)
        if result:  
            name = result[2]
            self.result_label.config(text=f'Welcome home:\n{name}')
            GPIO.output(26,1)
            self.root.update() 
        else:
            GPIO.output(22,1)
            self.result_label.config(text=f'Unknown card access denied')
            self.root.update()
        self.root.after(3000,self.clear_display)
        
    def clear_display(self):
        self.result_label.config(text='')
        GPIO.output(26,0)
        GPIO.output(22,0)
        

    def on_closing(self,event):
            if messagebox.askyesno('Exit','Are you sure?'):
                self.root.destroy() 

reader()
