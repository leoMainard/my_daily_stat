import streamlit as st

@st.dialog("Login", dismissible=False)
def login():
    first_name = st.text_input("Fisrtname")
    last_name = st.text_input("Lastname")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    password_confirm = st.text_input("Confirm Password", type="password")
    if st.button("Login"):
        if first_name == "admin" and password == "password":  # Example check
            st.user = first_name
            st.success("Logged in successfully!")
            st.rerun()
        else:
            st.error("Invalid credentials")

# login()