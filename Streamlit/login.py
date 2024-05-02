import streamlit as st
import time # for simulating a real-time data, time loop
import sqlite3
from passlib.hash import pbkdf2_sha256
import mysql.connector

import menu

# connect to database
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "stud_feedback"
}

# Database initialization
db_connection = mysql.connector.connect(
    host=db_config["host"],
    user=db_config["user"],
    password=db_config["password"],
    database=db_config["database"]
)
cursor = db_connection.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255),
    password VARCHAR(255)
)
''')
db_connection.commit()

# Function to create a hashed password
def hash_password(password):
    return pbkdf2_sha256.hash(password)

# Function to verify a password against the hashed password
def verify_password(password, hashed_password):
    return pbkdf2_sha256.verify(password, hashed_password)

# Streamlit app
def main():

    # Set page configuration
    st.set_page_config(
        page_title="Real-Time Sentiment Analysis Dashboard",
        page_icon="📈",
        layout="wide"
    )

    #st.title("Login")
    # Page state management
    page = st.sidebar.selectbox("Select Page", ["Home", "Login", "Register"])
    st.sidebar.write("")

    if page == "Home":
        st.header("Welcome to the Sentiment Analysis System")

    elif page == "Login":
        st.header("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")        
        login_button = st.button("Login")
        error_message = st.empty()

        if login_button:
            if authenticate_user(username, password):
                success_message = st.success("Login successful!")

                # Simulate a delay before redirecting
                for i in range(3, 0, -1):
                    success_message.info(f"Redirecting in {i} seconds...")
                    time.sleep(1)

                # Clear the login section
                success_message.empty()
                error_message.empty()
                st.empty()

                # Set the logged_in session state
                st.session_state.user_info = {"username": username}
                st.session_state.logged_in = True

                # redirect to main dashboard
                
                #st.experimental_rerun()
                

            else:
                error_message.error("Invalid username or password")

    elif page == "Register":
        st.header("Register")
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        if st.button("Register"):
            if register_user(new_username, new_password):
                st.success("Registration successful!")
            else:
                st.error("Username already exists")

def authenticate_user(username, password):
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()

    if user and verify_password(password, user[2]):
        return True
    else:
        return False

def register_user(username, password):
    hashed_password = hash_password(password)

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        db_connection.commit()
        return True
    except sqlite3.IntegrityError:
        return False

if __name__ == "__main__":
    main()