import sqlite3
"""
Here we connect to a file called database.db that our program will create once we execute this program.
This file is the database that will hold all of our application’s data. 
We then open the schema.sql file and run it using the executescript() method that executes multiple SQL statements at once. 
This will create the urls table. Finally, we commit the changes and close the connection.
"""
connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

connection.commit()
connection.close()