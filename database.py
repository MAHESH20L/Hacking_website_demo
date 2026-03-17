import sqlite3 as ql
def connect_db():
    conn=ql.connect("database.db")
    return conn #Establishing connection
def create_table():
    conn=connect_db()
    cursor=conn.cursor()
    cursor.execute("""
                  CREATE TABLE IF NOT EXISTS products(
                   id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT,price REAL)""" )
    cursor.execute(""" CREATE TABLE IF NOT EXISTS users(
                   id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT unique,password TEXt)""")
    conn.commit()
    conn.close()