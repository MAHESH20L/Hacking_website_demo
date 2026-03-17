#This program inserts the username and password and then executes the login
import sqlite3 as ql
import time
import bcrypt
import streamlit as st
from database import connect_db
max_att=3
lock_time=180
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
        cursor.execute("Select password,failed_attempts,last_attempt from users where username=?",(username,))
        user=cursor.fetchone()
        if user:
            attempts=user[1]
            last_time=user[2]
            if attempts>=max_att:
                if time.time()-last_time<lock_time:
                    conn.close()
                    return "Locked"
                else:
                    attempts=0
                    cursor.execute("UPDATE users SET failed_attempts=0 WHERE username=?",(username,))
                    conn.commit()
            if dec_hash(password,user[0]):
                cursor.execute("UPDATE users SET failed_attempts=0,last_attempt=0 WHERE username=?",(username,))
                conn.commit()
                conn.close()
                return True
            attempts+=1
            cursor.execute("UPDATE users SET failed_attempts=?,last_attempt=? WHERE username=?",(attempts,time.time(),username))
            conn.commit()
            conn.close()
            return False
        conn.close()
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

