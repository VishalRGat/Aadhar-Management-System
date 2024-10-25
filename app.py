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

# Aadhar Number Management System
st.title("Aadhar Number Management System")

# Initialize session state for aadhar input if not already done
if 'aadhar_input' not in st.session_state:
    st.session_state.aadhar_input = ""

# Sidebar menu
with st.sidebar:
    menu_option = st.radio("Menu", ["Add Aadhar Number", "View All Aadhar Numbers"])

# Aadhar number input
if menu_option == "Add Aadhar Number":
    aadhar_number = st.text_input("Enter number here", value=st.session_state.aadhar_input, max_chars=12)  # Title updated
    if st.button("Submit"):
        if not aadhar_number.isdigit() or len(aadhar_number) != 12:
            st.error("Invalid Aadhar number! Please enter exactly 12 numeric digits.")
        else:
            if check_aadhar(aadhar_number):
                
