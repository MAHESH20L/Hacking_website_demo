import streamlit as st
def home():
    st.sidebar.title("Navigation")
    page=st.sidebar.radio("Goto",['home','profile','settings'])
    if page=='home':
        st.title('welcome to homepage')
        st.write("Your personal dashboard")
    st.sidebar.divider()
    if st.sidebar.button("Logout"):
        st.session_state.page="login"
        st.rerun()