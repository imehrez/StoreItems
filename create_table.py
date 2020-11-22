import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

#Create table query, named 'users, with the collumns
# auto incrementing id
create_user_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_user_table)

create_item_table = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name text, price real)"
cursor.execute(create_item_table)

connection.commit()
connection.close()