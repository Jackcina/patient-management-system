import sqlite3
import pandas as pd

# Read the Excel file
df = pd.read_excel("Untitled spreadsheet.xlsx")   # Change the name if your file is different

# Remove extra spaces from column names
df.columns = df.columns.str.strip()

# Connect to the database
conn = sqlite3.connect("patients.db")
cursor = conn.cursor()

# Insert each row
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO patients
        (patient_name, age, sex, duration, disease, before_value, after_value)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        row["PATIENT NAME"],
        row["AGE"],
        row["SEX"],
        row["DURATION"],
        row["DISEASE"],
        row["BEFORE"],
        row["AFTER"]
    ))

conn.commit()
conn.close()

print("✅ Excel data imported successfully!")