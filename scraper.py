import mechanicalsoup
import pandas as pd
import sqlite3

# create browser object & open URL
browser = mechanicalsoup.StatefulBrowser()
browser.open("https://en.wikipedia.org/wiki/Comparison_of_Linux_distributions")

# extract all table headers (entire "Distribution" column)
th = browser.page.find_all("th", attrs={"class": "table-rh"})
# tidy up and slice off non-table elements 
distribution = [value.text.replace("\n", "") for value in th]
distribution = distribution[:95]

# extract table data (the rest of the table)
td = browser.page.find_all("td")
# tidy up and slice off non-table elements
columns = [value.text.replace("\n", "") for value in td]
columns = columns[6:1051]

column_names = ["Founder", 
                "Maintainer", 
                "Initial_Release_Year", 
                "Current_Stable_Version", 
                "Security_Updates", 
                "Release_Date", 
                "System_Distribution_Commitment", 
                "Forked_From", 
                "Target_Audience", 
                "Cost", 
                "Status"]

dictionary = {"Distribution": distribution}

# insert column names and their data into a dictionary
for idx, key in enumerate(column_names):
    dictionary[key] = columns[idx:][::11]

# convert dictionary to data frame
df = pd.DataFrame(data = dictionary)

# create new database and cursor
connection = sqlite3.connect("linux_distro.db")
cursor = connection.cursor()

# create database table and insert all data frame rows
cursor.execute("create table linux (Distribution, " + ",".join(column_names)+ ")")
for i in range(len(df)):
    cursor.execute("insert into linux values (?,?,?,?,?,?,?,?,?,?,?,?)", df.iloc[i])

# PERMANENTLY save inserted data in "linux_distro.db"
connection.commit()

connection.close()

