import sqlite3
import pandas as pd

# load database file (make sure you run scraper.py first to create it)
connection = sqlite3.connect("linux_distro.db")

cursor = connection.cursor() # allows to execute SQL

# SELECT all the releases from 2008 
cursor.execute("select * from linux where Initial_Release_Year=:c", {"c": "2008"})
for row in cursor:
    print(row)

connection.close()