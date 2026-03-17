#This program inserts the username and password and then executes the login
import sqlite3 as ql
import bcrypt
import streamlit as st
from database import connect_db
def hash_pass(password):
    return bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()
def dec_hash(password,hashed):
    return bcrypt.checkpw(password.encode(),hashed.encode())
def login_page(username,password):
    if not username or not password:
        return False
    else:
        conn=connect_db()
        cursor=conn.cursor()#connecting database
        cursor.execute("Select password from users where username=?",(username,))
        user=cursor.fetchone()
        conn.close()
        if user:
           return dec_hash(password,user[0])
        return False
def signup_page(username,password):
    conn=connect_db()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user=cursor.fetchone()
    if user:
        conn.close()
        st.error("Signup failed.")
        return False
    hashed=hash_pass(password)
    cursor.execute("INSERT into users(username,password) VALUES(?,?)",(username,hashed))
    conn.commit()
    conn.close()
    return True

