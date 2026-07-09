import streamlit as st
from db import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS purchase_return (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    return_reference TEXT,
    purchase_reference TEXT,
    return_date TEXT,
    supplier TEXT,
    location TEXT,
    total_items INTEGER,
    total_qty REAL,
    total_amount REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS purchase_return_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    return_id INTEGER,
    item_code TEXT,
    item_name TEXT,
    uom TEXT,
    rate REAL,
    purchase_qty REAL,
    return_qty REAL,
    amount REAL
)
""")

conn.commit()
conn.close()

st.success("✅ Purchase Return Tables Created Successfully")
