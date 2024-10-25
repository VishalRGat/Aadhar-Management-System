import streamlit as st
import sqlite3
import pandas as pd
from io import BytesIO

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

def get_all_aadhar():
    cursor.execute("SELECT * FROM aadhar_data")
    rows = cursor.fetchall()
    return rows

# Streamlit UI
st.title("Aadhar Number Management System")

# Input Aadhar number (single bar for search and add)
aadhar_number = st.text_input("Enter Aadhar Number (12-digit)")

if st.button("Submit"):
    if not aadhar_number.isdigit() or len(aadhar_number) != 12:
        st.error("Invalid Aadhar number! Please enter a 12-digit numeric Aadhar number.")
    else:
        if check_aadhar(aadhar_number):
            st.info(f"Aadhar number {aadhar_number} already exists in the database.")
        else:
            add_aadhar(aadhar_number)
            st.success("Aadhar number added successfully.")

# Display all Aadhar numbers
st.header("All Submitted Aadhar Numbers")
data = get_all_aadhar()
df = pd.DataFrame(data, columns=["Aadhar Number"])
st.dataframe(df)

# Function to convert DataFrame to Excel in memory
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Aadhar Data')
    return output.getvalue()

# Function to convert DataFrame to PDF (using CSV as a workaround)
def to_pdf(df):
    output = BytesIO()
    df.to_csv(output, index=False)
    return output.getvalue()

# Export data options
excel_data = to_excel(df)
st.download_button(
    label="Download as Excel",
    data=excel_data,
    file_name='aadhar_data.xlsx',
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

pdf_data = to_pdf(df)
st.download_button(
    label="Download as PDF",
    data=pdf_data,
    file_name='aadhar_data.pdf',
    mime="application/pdf"
)

# Closing database connection
st.stop()
conn.close()
