#This repo is done for my learning of development as well as ethical hacking.
import streamlit as st
import random,smtplib,time #For otp time validation and generation
st.set_page_config(page_title="Auth App",layout="wide")
from auth import login_page,signup_page
from database import create_table
create_table()
from Dashboard import home

if "authenticated" not in st.session_state:
    st.session_state.authenticated=False
if "page" not in st.session_state:
    st.session_state.page="login"
if not st.session_state.get("authenticated", False):
    if st.session_state.page == "home":
        st.session_state.page = "login"

def signup():
    col1,col2,col3=st.columns([1,1,1])
    with col2:
        st.subheader("Signup_page")
        name_user=st.text_input("name_user")
        repassword=st.text_input("create password",type="password")
        re_password=st.text_input("retype password",type="password")
        if st.button("Signup",use_container_width=True):
            if not name_user or not repassword:
                st.error("Fields cannot be empty")
            elif repassword!=re_password:
                st.error("password not matched.")
            elif signup_page(name_user,repassword):
                st.success("Account created successfully")
                st.session_state.page='login'
                st.rerun()
            else:
                st.error("Signup failed.")
        st.divider()
        if st.button("Back_to_login",use_container_width=True):
            st.session_state.page="login"
            st.rerun()
def send_otp(email):
    otp=str(random.randint(100000,999999)) #otp generation
    st.session_state.otp=otp #otp sending
    st.session_state.otp_time=time.time()
    server=smtplib.SMTP("smtp.gmail.com",587)#smtp protocol
    server.starttls()
    server.login("projectuse43@gmail.com","elnn ulzf drvq zmte")
    server.sendmail("projectuse43@gmail.com",email,f"Your otp is {otp}")
    server.quit()
def otp_page():
    st.subheader("Enter otp ")#OTP input
    if "otp" not in st.session_state:
        send_otp(st.session_state.temp_user)#sending otp
    otp_input=st.text_input("Enter otp") #otp input
    if st.button("verify"): #otp verification
        #Time expiry check
        if time.time()-st.session_state.otp_time>120:
            st.error("OTP expired")
            st.session_state.page="login"
            st.rerun()
        #attempt limit
        if "otp_attempts" not in st.session_state:
            st.session_state.otp_attempts=0
        st.session_state.otp_attempts+=1
        if st.session_state.otp_attempts>5:
            st.error("Too many attempts")
            st.stop()
        if otp_input=st.session_state.otp:
            st.success("Login successfull")
            st.session_state.authenticated=True
            st.session_state.username=st.session_state.temp_user
            st.session_state.page="home"
            st.session_state.otp_attempts=0
            st.session_state.otp=None
            st.rerun()
       else:
            st.error("Wrong otp")
    # 🔁 Resend OTP
    if st.button("Resend OTP"):
        send_otp(st.session_state.temp_user)
        st.success("OTP sent again")
# def reset_page():
#     st.subheader("🔑 Reset Password")
#     email = st.text_input("Enter your email")
#     if st.button("Send Reset OTP"):
#         if email:
#             st.session_state.reset_user = email
#             send_otp(email)
#             st.session_state.page = "reset_verify"
#             st.rerun()
#         else:
#             st.error("Enter email")

if st.session_state.page=="login":
    col1,col2,col3=st.columns([1,1,1])
    with col2:
        st.subheader("Login_page")
        username=st.text_input("username")
        password=st.text_input("password",type="password")
        if st.button("Login",use_container_width=True):
            if not username or not password:
                st.error("Username / password cannot be empty")
            else:
                user=login_page(username,password)
                if user==True:
                    #st.success("Login successful.")
                    st.session_state.temp_user = username#fixed otp bug
                    st.session_state.page="otp"
                    st.rerun()
                elif user=="Locked":
                    st.error("Account locked , Try again after sometime")
                else:
                    st.error("Invalid credentials.")
        st.divider()
        if st.button("Forgot Password?", use_container_width=True):
            st.session_state.page = "reset"
            st.rerun()
        st.divider()
        if st.button("create_account",use_container_width=True):
            st.session_state.page="signup"
            st.rerun()
if st.session_state.page=="signup":
    signup()
elif st.session_state.page=="home":
    home()
elif st.session_state.page=="otp":
    otp_page()
