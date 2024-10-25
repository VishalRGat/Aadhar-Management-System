import streamlit as st
import sqlite3
import pandas as pd
from io import BytesIO

# Database connection
conn = sqlite3.connect("aadhar_db.sqlite")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS aadhar_data (aadhar_number TEXT UNIQUE)")
conn.commit()

# Helper functions
def check_aadhar(aadhar_number):
    cursor.execute("SELECT * FROM aadhar_data WHERE aadhar_number=?", (aadhar_number,))
    return cursor.fetchone()

def add_aadhar(aadhar_number):
    cursor.execute("INSERT INTO aadhar_data (aadhar_number) VALUES (?)", (aadhar_number,))
    conn.commit()

def get_all_aadhar():
    cursor.execute("SELECT * FROM aadhar_data")
    rows = cursor.fetchall()
    return rows

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Aadhar Data')
    return output.getvalue()

def to_pdf(df):
    output = BytesIO()
    df.to_csv(output, index=False)
    return output.getvalue()

# Initialize session state for login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Login page
if not st.session_state.logged_in:
    st.title("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if email == "admin@example.com" and password == "password123":
            st.session_state.logged_in = True
            st.success("Login successful!")
        else:
            st.error("Invalid email or password.")
else:
    # Aadhar Number Management System
    st.title("Aadhar Number Management System")
    
    # Sidebar menu
    with st.sidebar:
        menu_option = st.r
