import streamlit as st
import sqlite3

st.title("🗑️ Reset RTE Store Data")

conn = sqlite3.connect("rte_store.db")
cursor = conn.cursor()

st.warning("⚠️ Ye saara Master aur Transaction Data delete kar dega!")

if st.button("DELETE ALL DATA", use_container_width=True):

    tables_to_delete = [
        "employee_master",
        "location_master",
        "tax_master",
        "supplier_master",
        "item_master",
        "reference_master",

        # Purchase
        "purchase_entry",
        "purchase_items",

        # Purchase Return
        "purchase_return",
        "purchase_return_items",

        # Stock
        "stock_entry",
        "stock_master",
        "stock_ledger",

        # Internal Transfer
        "internal_transfer"
    ]

    deleted = []

    for table in tables_to_delete:
        try:
            cursor.execute(f"DELETE FROM {table}")
            deleted.append(table)
        except Exception as e:
            st.error(f"{table} : {e}")

    conn.commit()

    st.success("✅ All Data Deleted Successfully")
    st.write("Deleted Tables:")
    st.write(deleted)

conn.close()
