import streamlit as st
import pandas as pd
from db import get_connection
from datetime import date

st.set_page_config(
    page_title="Stock Management",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Stock Management")

conn = get_connection()
cursor = conn.cursor()

st.subheader("📋 Current Stock")

cursor.execute("""
SELECT
item_code,
item_name,
location,
stock,
uom
FROM stock_master
ORDER BY item_name
""")

stock = cursor.fetchall()

if stock:

    df = pd.DataFrame(
        stock,
        columns=[
            "Item Code",
            "Item Name",
            "Location",
            "Current Stock",
            "UOM"
        ]
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("No Stock Available")

st.divider()

st.subheader("📜 Stock Ledger")

cursor.execute("""
SELECT
trans_date,
trans_type,
reference_no,
item_name,
location,
qty_in,
qty_out,
balance
FROM stock_ledger
ORDER BY id DESC
LIMIT 50
""")

ledger = cursor.fetchall()

if ledger:

    ledger_df = pd.DataFrame(
        ledger,
        columns=[
            "Date",
            "Type",
            "Reference",
            "Item",
            "Location",
            "IN",
            "OUT",
            "Balance"
        ]
    )

    st.dataframe(
        ledger_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("No Stock Transactions Found")

conn.close()