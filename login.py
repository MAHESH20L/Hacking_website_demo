#This repo is done for my learning of development as well as ethical hacking.
import streamlit as st
from auth import login_page,signup_page
from database import create_table
create_table()
from Dashboard import home
if "authenticated" not in st.session_state:
    st.session_state.authenticated=False
if "page" not in st.session_state:
    st.session_state.page="login"
if st.session_state.page=="home" and not st.session_state.get("authenticated"):
    st.session_state.page="login" #bug fixed
st.set_page_config(page_title="Auth App",layout="wide")

def signup():
    col1,col2,col3=st.columns([1,1,1])
    with col2:
        st.subheader("Signup_page")
        name_user=st.text_input("name_user")
        repassword=st.text_input("create password",type="password")
        re_password=st.text_input("retype password",type="password")
        if st.button("Signup",use_container_width=True):
            if repassword!=re_password:
                st.error("password not matched.")
            elif signup_page(name_user,repassword):
                st.success("Account created successfully")
                st.session_state.page='login'
            else:
                print("User already exists")
        st.divider()
        if st.button("Back_to_login",use_container_width=True):
            st.session_state.page="login"
            st.rerun()
if st.session_state.page=="login":
    col1,col2,col3=st.columns([1,1,1])
    with col2:
        st.subheader("Login_page")
        username=st.text_input("username")
        password=st.text_input("password",type="password")
        if st.button("Login",use_container_width=True):
            user=login_page(username,password)
            if user:
                st.success("Login successful.")
                st.session_state.authenticated=True #Fixed buy
                st.session_state.page="home"
                st.rerun()
            else:
                st.error("Invalid credentials.")
        st.divider()
        if st.button("create_account",use_container_width=True):
            st.session_state.page="signup"
            st.rerun()
if st.session_state.page=="signup":
    signup()
elif st.session_state.page=="home":
    home()
