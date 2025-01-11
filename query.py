import sqlite3
from serial.tools import list_ports
import pandas as pd


# Kapcsolódás az adatbázishoz
conn = sqlite3.connect('cards.db')
# Adatok lekérdezése Pandas DataFrame-be
df = pd.read_sql_query('SELECT * FROM cardholder', conn)

# Adatok megjelenítése
print(df)

# Kapcsolat bezárása
conn.close()