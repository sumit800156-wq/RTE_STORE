import streamlit as st
import sqlite3

st.title("🗑️ Reset RTE Store Data")

conn = sqlite3.connect("rte_store.db")
cursor = conn.cursor()

st.warning("⚠️ Ye saara master aur transaction data delete kar dega!")

if st.button("DELETE ALL DATA"):

    tables_to_delete = [
        "employee_master",
        "location_master",
        "tax_master",
        "purchase_entry",
        "reference_master",
        "stock_entry",
        "supplier_master",
        "item_master",
        "internal_transfer",
        "stock_master"
    ]

    deleted = []

    for table in tables_to_delete:
        try:
            cursor.execute(f"DELETE FROM {table}")
            deleted.append(table)
        except sqlite3.OperationalError:
            pass

    conn.commit()

    st.success("✅ All available data deleted successfully!")
    st.write("Deleted Tables:")
    st.write(deleted)

conn.close()
