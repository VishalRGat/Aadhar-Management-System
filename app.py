import streamlit as st
import sqlite3

# Database connection
conn = sqlite3.connect("aadhar_db.sqlite")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS aadhar_data (aadhar_number TEXT UNIQUE)")
conn.commit()

def check_aadhar(aadhar_number):
    cursor.execute("SELECT * FROM aadhar_data WHERE aadhar_number=?", (aadhar_number,))
    return cursor.fetchone()

def add_aadhar(aadhar_number):
    cursor.execute("INSERT INTO aadhar_data (aadhar_number) VALUES (?)", (aadhar_number,))
    conn.commit()

# Streamlit UI
st.title("Aadhar Number Management System")

# Search Aadhar number
search_number = st.text_input("Search Aadhar Number:")
if st.button("Search"):
    result = check_aadhar(search_number)
    if result:
        st.success(f"Aadhar number {search_number} found in the database.")
    else:
        st.warning("Aadhar number not found.")

# Input and submit Aadhar number
aadhar_number = st.text_input("Enter new Aadhar Number:")
if st.button("Submit"):
    if check_aadhar(aadhar_number):
        st.info("Aadhar number already exists. Please enter a new number.")
    else:
        add_aadhar(aadhar_number)
        st.success("Aadhar number added successfully.")

# Closing database connection
st.stop()
conn.close()
