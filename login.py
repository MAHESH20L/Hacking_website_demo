#This repo is done for my learning of development as well as ethical hacking.
import streamlit as st
import random,smtplib,time #For otp time validation and generation
st.set_page_config(page_title="Auth App",layout="wide")
from auth import login_page,signup_page
from database import create_table
create_table()
from Dashboard import home
import re
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)
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
        name_user=st.text_input("email")
        repassword=st.text_input("create password",type="password")
        re_password=st.text_input("retype password",type="password")
        if st.button("Signup",use_container_width=True):
            if not is_valid_email(name_user):
                st.error("Enter valid email")
                return
            elif not name_user or not repassword:
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
def send_otp(email, otp_type="login"):
    import random, time, smtplib
    otp = str(random.randint(100000, 999999))
    # store separately
    if otp_type == "login":
        st.session_state.login_otp = otp
        st.session_state.login_otp_time = time.time()
    else:
        st.session_state.reset_otp = otp
        st.session_state.reset_otp_time = time.time()
    EMAIL = st.secrets["EMAIL"]
    PASSWORD = st.secrets["EMAIL_PASS"]
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL, PASSWORD)
    server.sendmail(EMAIL, email, f"Your OTP is {otp}")
    server.quit()
def otp_page():
    col1,col2,col3=st.columns([1,1,1])
    with col2:
        st.subheader("🔐 Enter OTP")
        if "login_otp" not in st.session_state:
            send_otp(st.session_state.temp_user, "login")
        otp_input = st.text_input("Enter OTP")
        if st.button("Verify"):
            # empty check
            if not otp_input:
                st.error("Enter OTP")
                return
            # expiry
            if time.time() - st.session_state.login_otp_time > 120:
                st.error("OTP expired")
                st.session_state.login_otp = None
                st.session_state.otp_attempts = 0
                st.session_state.page = "login"
                st.rerun()
            # attempts
            if "otp_attempts" not in st.session_state:
                st.session_state.otp_attempts = 0
            st.session_state.otp_attempts += 1
            if st.session_state.otp_attempts > 5:
                st.error("Too many attempts")
                st.stop()
            # verify
            if otp_input == st.session_state.login_otp:
                st.success("Login successful")
                st.session_state.authenticated = True
                st.session_state.username = st.session_state.temp_user
                st.session_state.page = "home"
                # cleanup
                st.session_state.otp_attempts = 0
                st.session_state.login_otp = None
                st.session_state.temp_user = None
                st.rerun()
            else:
                st.error("Wrong OTP")
        # resend
        if "last_otp_time" not in st.session_state:
            st.session_state.last_otp_time = 0
        if st.button("Resend OTP"):
            if time.time() - st.session_state.last_otp_time < 30:
                st.warning("Wait 30 seconds")
            else:
                send_otp(st.session_state.temp_user, "login")
                st.session_state.last_otp_time = time.time()
                st.success("OTP sent again")
def reset_page():
     col1,col2,col3=st.columns([1,1,1])
     with col2:
         st.subheader("🔑 Reset Password")
         email = st.text_input("Enter your email")
         if st.button("Send Reset OTP",use_container_width=True):
             if not email:
                st.error("Enter email")
                return
             elif not is_valid_email(email):
                st.error("Enter valid email")
                return
             else:
                st.session_state.reset_user = email
                send_otp(email, "reset")
                st.session_state.page = "reset_verify"
                st.rerun()
def reset_verify_page():
     col1,col2,col3=st.columns([1,1,1])
     with col2:
        st.subheader("🔑 Reset Password")
        otp = st.text_input("Enter OTP")
        new_pass = st.text_input("New Password", type="password")
        if st.button("Update Password",use_container_width=True):
            # empty check
            if not otp or not new_pass:
                st.error("Fill all fields")
                return
            # expiry
            if time.time() - st.session_state.reset_otp_time > 120:
                st.session_state.reset_otp = None
                st.error("OTP expired")
                return
            # attempts
            if "reset_attempts" not in st.session_state:
                st.session_state.reset_attempts = 0
            st.session_state.reset_attempts += 1
            if st.session_state.reset_attempts > 5:
                st.error("Too many attempts")
                st.stop()
            # verify
            if otp != st.session_state.get("reset_otp"):
                st.error("Wrong OTP")
                return
            from auth import hash_pass
            from database import connect_db
            conn = connect_db()
            cursor = conn.cursor()
            hashed = hash_pass(new_pass)
            cursor.execute(
                "UPDATE users SET password=? WHERE username=?",
                (hashed, st.session_state.reset_user)
            )
            conn.commit()
            conn.close()
            st.success("Password updated successfully")
            # cleanup
            st.session_state.reset_attempts = 0
            st.session_state.reset_otp = None
            st.session_state.page = "login"
            st.rerun()
        st.divider()
        if st.button("back_to_login",use_container_width=True):
            st.session_state.page="login"
            st.rerun()
if st.session_state.page=="login":
    col1,col2,col3=st.columns([1,1,1])
    with col2:
        st.subheader("Login_page")
        username=st.text_input("email")
        password=st.text_input("password",type="password")
        if st.button("Login",use_container_width=True):
            if not username or not password:
                st.error("Username / password cannot be empty")
            elif not is_valid_email(username):
                st.error("Enter valid email")
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
elif st.session_state.page == "reset":
    reset_page()
elif st.session_state.page == "reset_verify":
    reset_verify_page()
