import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from db import get_connection
from datetime import datetime

st.set_page_config(
    page_title="RTE Store ERP",
    page_icon="📊",
    layout="wide"
)

st.title("📊 RTE STORE ERP DASHBOARD")

conn = get_connection()
cursor = conn.cursor()

# ================= COUNTS =================

def get_count(table):

    cursor.execute(f"SELECT COUNT(*) FROM {table}")

    return cursor.fetchone()[0]


total_items = get_count("item_master")
total_suppliers = get_count("supplier_master")
total_employees = get_count("employee_master")
total_locations = get_count("location_master")
total_purchase = get_count("purchase_entry")
total_transfer = get_count("internal_transfer")


# ================= STOCK =================

cursor.execute("""
SELECT IFNULL(SUM(stock),0)
FROM stock_master
""")

current_stock = cursor.fetchone()[0]


# ================= PURCHASE AMOUNT =================

cursor.execute("""
SELECT IFNULL(SUM(bill_total),0)
FROM purchase_entry
""")

purchase_amount = cursor.fetchone()[0]


# ================= TODAY PURCHASE =================

today = datetime.today().strftime("%Y-%m-%d")

cursor.execute("""
SELECT IFNULL(SUM(bill_total),0)
FROM purchase_entry
WHERE purchase_date=?
""",(today,))

today_purchase = cursor.fetchone()[0]


# ================= MONTH PURCHASE =================

month = datetime.today().strftime("%Y-%m")

cursor.execute("""
SELECT IFNULL(SUM(bill_total),0)
FROM purchase_entry
WHERE substr(purchase_date,1,7)=?
""",(month,))

month_purchase = cursor.fetchone()[0]


# ================= KPI =================

st.subheader("📈 Business Overview")

c1,c2,c3,c4 = st.columns(4)

with c1:
    st.metric(
        "📦 Total Items",
        total_items
    )

with c2:
    st.metric(
        "🚚 Suppliers",
        total_suppliers
    )

with c3:
    st.metric(
        "👨 Employees",
        total_employees
    )

with c4:
    st.metric(
        "📍 Locations",
        total_locations
    )


c5,c6,c7,c8 = st.columns(4)

with c5:
    st.metric(
        "🛒 Purchases",
        total_purchase
    )

with c6:
    st.metric(
        "🔄 Transfers",
        total_transfer
    )

with c7:
    st.metric(
        "📦 Current Stock",
        current_stock
    )

with c8:
    st.metric(
        "💰 Purchase Amount",
        f"₹ {purchase_amount:,.2f}"
    )


c9,c10 = st.columns(2)

with c9:
    st.metric(
        "📅 Today's Purchase",
        f"₹ {today_purchase:,.2f}"
    )

with c10:
    st.metric(
        "📆 This Month Purchase",
        f"₹ {month_purchase:,.2f}"
    )

st.divider()
# ================= PURCHASE ANALYTICS =================

st.subheader("💰 Purchase Analytics")

# Average Purchase
cursor.execute("""
SELECT IFNULL(AVG(bill_total),0)
FROM purchase_entry
""")
average_purchase = cursor.fetchone()[0]

# Highest Purchase
cursor.execute("""
SELECT IFNULL(MAX(bill_total),0)
FROM purchase_entry
""")
highest_purchase = cursor.fetchone()[0]

# Lowest Purchase
cursor.execute("""
SELECT IFNULL(MIN(bill_total),0)
FROM purchase_entry
WHERE bill_total > 0
""")
lowest_purchase = cursor.fetchone()[0]

# Total Quantity Purchased
cursor.execute("""
SELECT IFNULL(SUM(total_quantity),0)
FROM purchase_entry
""")
total_qty = cursor.fetchone()[0]

# Average Quantity per Purchase
cursor.execute("""
SELECT IFNULL(AVG(total_quantity),0)
FROM purchase_entry
""")
avg_qty = cursor.fetchone()[0]

a1, a2, a3, a4, a5 = st.columns(5)

with a1:
    st.metric(
        "📊 Average Purchase",
        f"₹ {average_purchase:,.2f}"
    )

with a2:
    st.metric(
        "🏆 Highest Purchase",
        f"₹ {highest_purchase:,.2f}"
    )

with a3:
    st.metric(
        "📉 Lowest Purchase",
        f"₹ {lowest_purchase:,.2f}"
    )

with a4:
    st.metric(
        "📦 Total Qty Purchased",
        f"{total_qty:,.2f}"
    )

with a5:
    st.metric(
        "📋 Avg Qty / Purchase",
        f"{avg_qty:,.2f}"
    )

st.divider()
# ================= ALERTS =================

st.subheader("⚠️ Alerts & Notifications")

# ---------- Low Stock ----------
cursor.execute("""
SELECT COUNT(*)
FROM stock_master
WHERE stock <= 10
""")
low_stock = cursor.fetchone()[0]

# ---------- Out of Stock ----------
cursor.execute("""
SELECT COUNT(*)
FROM stock_master
WHERE stock = 0
""")
out_stock = cursor.fetchone()[0]

# ---------- Inactive Items ----------
cursor.execute("""
SELECT COUNT(*)
FROM item_master
WHERE status='Inactive'
""")
inactive_items = cursor.fetchone()[0]

# ---------- Inactive Suppliers ----------
cursor.execute("""
SELECT COUNT(*)
FROM supplier_master
WHERE status='Inactive'
""")
inactive_suppliers = cursor.fetchone()[0]

# ---------- Inactive Employees ----------
cursor.execute("""
SELECT COUNT(*)
FROM employee_master
WHERE status='Inactive'
""")
inactive_employees = cursor.fetchone()[0]

# ---------- Today's Transfers ----------
today = datetime.today().strftime("%Y-%m-%d")

cursor.execute("""
SELECT COUNT(*)
FROM internal_transfer
WHERE transfer_date=?
""",(today,))
today_transfer = cursor.fetchone()[0]

a1, a2, a3 = st.columns(3)

with a1:
    st.error(f"🔴 Low Stock Items : {low_stock}")

with a2:
    st.warning(f"📦 Out of Stock : {out_stock}")

with a3:
    st.info(f"🔄 Today's Transfers : {today_transfer}")

a4, a5 = st.columns(2)

with a4:
    st.warning(f"🚫 Inactive Items : {inactive_items}")

with a5:
    st.warning(
        f"🚚 Suppliers : {inactive_suppliers} | 👨 Employees : {inactive_employees}"
    )

st.divider()
# ================= CHARTS =================

st.subheader("📊 Business Analytics")

col1, col2 = st.columns(2)

# ---------- Purchase Trend ----------

with col1:

    cursor.execute("""
    SELECT purchase_date,
           SUM(bill_total)
    FROM purchase_entry
    GROUP BY purchase_date
    ORDER BY purchase_date
    """)

    rows = cursor.fetchall()

    if rows:

        df = pd.DataFrame(
            rows,
            columns=["Date", "Amount"]
        )

        fig, ax = plt.subplots(figsize=(6,3))

        ax.plot(
            df["Date"],
            df["Amount"],
            marker="o"
        )

        ax.set_title("Purchase Trend")
        plt.xticks(rotation=45)

        st.pyplot(fig)

    else:

        st.info("No Purchase Data")


# ---------- Material Type Wise Items ----------

with col2:

    cursor.execute("""
    SELECT material_type,
           COUNT(*)
    FROM item_master
    GROUP BY material_type
    """)

    rows = cursor.fetchall()

    if rows:

        df = pd.DataFrame(
            rows,
            columns=["Material Type", "Items"]
        )

        fig, ax = plt.subplots(figsize=(6,3))

        ax.pie(
            df["Items"],
            labels=df["Material Type"],
            autopct="%1.1f%%"
        )

        ax.set_title("Material Type Wise Items")

        st.pyplot(fig)

    else:

        st.info("No Item Data")

st.divider()

# ================= SECOND ROW =================

col3, col4 = st.columns(2)

# ---------- Purchase By Supplier ----------

with col3:

    cursor.execute("""
    SELECT supplier_code,
           SUM(bill_total)
    FROM purchase_entry
    GROUP BY supplier_code
    """)

    rows = cursor.fetchall()

    if rows:

        df = pd.DataFrame(
            rows,
            columns=["Supplier", "Amount"]
        )

        fig, ax = plt.subplots(figsize=(6,3))

        ax.bar(
            df["Supplier"],
            df["Amount"]
        )

        ax.set_title("Purchase By Supplier")

        plt.xticks(rotation=30)

        st.pyplot(fig)

    else:

        st.info("No Supplier Purchase")


# ---------- Purchase By Location ----------

with col4:

    cursor.execute("""
    SELECT location,
           SUM(bill_total)
    FROM purchase_entry
    GROUP BY location
    """)

    rows = cursor.fetchall()

    if rows:

        df = pd.DataFrame(
            rows,
            columns=["Location", "Amount"]
        )

        fig, ax = plt.subplots(figsize=(6,3))

        ax.bar(
            df["Location"],
            df["Amount"]
        )

        ax.set_title("Purchase By Location")

        plt.xticks(rotation=30)

        st.pyplot(fig)

    else:

        st.info("No Location Purchase")

st.divider()
# ================= MASTERS =================

st.subheader("📋 Masters Overview")

col1, col2 = st.columns(2)

# ---------- Last Added Items ----------

with col1:

    st.markdown("### 📦 Last Added Items")

    cursor.execute("""
    SELECT
        item_code,
        item_name,
        material_type,
        purchase_rate
    FROM item_master
    ORDER BY id DESC
    LIMIT 10
    """)

    rows = cursor.fetchall()

    if rows:

        df = pd.DataFrame(
            rows,
            columns=[
                "Code",
                "Item",
                "Material Type",
                "Rate"
            ]
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No Items Found")


# ---------- Last Added Suppliers ----------

with col2:

    st.markdown("### 🚚 Last Added Suppliers")

    cursor.execute("""
    SELECT
        supplier_code,
        supplier_name,
        contact_person,
        status
    FROM supplier_master
    ORDER BY id DESC
    LIMIT 10
    """)

    rows = cursor.fetchall()

    if rows:

        df = pd.DataFrame(
            rows,
            columns=[
                "Code",
                "Supplier",
                "Contact",
                "Status"
            ]
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No Suppliers Found")


st.divider()

# ================= EMPLOYEES & LOCATIONS =================

col3, col4 = st.columns(2)

# ---------- Employees ----------

with col3:

    st.markdown("### 👨 Last Added Employees")

    cursor.execute("""
    SELECT
        employee_code,
        employee_name,
        role,
        status
    FROM employee_master
    ORDER BY id DESC
    LIMIT 10
    """)

    rows = cursor.fetchall()

    if rows:

        df = pd.DataFrame(
            rows,
            columns=[
                "Code",
                "Employee",
                "Role",
                "Status"
            ]
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No Employees Found")


# ---------- Locations ----------

with col4:

    st.markdown("### 📍 Locations")

    cursor.execute("""
    SELECT
        location_code,
        location_name,
        status
    FROM location_master
    ORDER BY id DESC
    LIMIT 10
    """)

    rows = cursor.fetchall()

    if rows:

        df = pd.DataFrame(
            rows,
            columns=[
                "Code",
                "Location",
                "Status"
            ]
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No Locations Found")

st.divider()
# ================= RECENT TRANSACTIONS =================

st.subheader("📜 Recent Transactions")

col1, col2 = st.columns(2)

# ================= LAST 10 PURCHASES =================

with col1:

    st.markdown("### 🛒 Last 10 Purchases")

    cursor.execute("""
    SELECT
        reference_no,
        purchase_date,
        supplier_code,
        bill_total
    FROM purchase_entry
    ORDER BY id DESC
    LIMIT 10
    """)

    rows = cursor.fetchall()

    if rows:

        purchase_df = pd.DataFrame(
            rows,
            columns=[
                "Reference",
                "Date",
                "Supplier",
                "Amount"
            ]
        )

        st.dataframe(
            purchase_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No Purchase Found")


# ================= LAST 10 TRANSFERS =================

with col2:

    st.markdown("### 🔄 Last 10 Internal Transfers")

    cursor.execute("""
    SELECT
        reference_no,
        transfer_date,
        from_location,
        to_location,
        total_quantity
    FROM internal_transfer
    ORDER BY id DESC
    LIMIT 10
    """)

    rows = cursor.fetchall()

    if rows:

        transfer_df = pd.DataFrame(
            rows,
            columns=[
                "Reference",
                "Date",
                "From",
                "To",
                "Quantity"
            ]
        )

        st.dataframe(
            transfer_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No Transfer Found")

st.divider()

# ================= STOCK LEDGER =================

st.subheader("📦 Latest Stock Movement")

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
LIMIT 15
""")

rows = cursor.fetchall()

if rows:

    ledger_df = pd.DataFrame(
        rows,
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

    st.info("No Stock Movement Found")

st.divider()
# ================= STOCK SUMMARY =================

st.subheader("📦 Stock Summary")

# ---------- Store Stock ----------

cursor.execute("""
SELECT IFNULL(SUM(stock),0)
FROM stock_master
WHERE location='Store'
""")

store_stock = cursor.fetchone()[0]

# ---------- Kitchen Stock ----------

cursor.execute("""
SELECT IFNULL(SUM(stock),0)
FROM stock_master
WHERE location='Kitchen'
""")

kitchen_stock = cursor.fetchone()[0]

# ---------- Total Stock ----------

cursor.execute("""
SELECT IFNULL(SUM(stock),0)
FROM stock_master
""")

total_stock = cursor.fetchone()[0]

# ---------- Stock Value ----------

cursor.execute("""
SELECT IFNULL(SUM(stock * purchase_rate),0)
FROM stock_master
""")

stock_value = cursor.fetchone()[0]

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "🏪 Store Stock",
        f"{store_stock:,.2f}"
    )

with c2:
    st.metric(
        "🍳 Kitchen Stock",
        f"{kitchen_stock:,.2f}"
    )

with c3:
    st.metric(
        "📦 Total Stock",
        f"{total_stock:,.2f}"
    )

with c4:
    st.metric(
        "💰 Stock Value",
        f"₹ {stock_value:,.2f}"
    )

st.divider()

# ================= TOP PURCHASED ITEMS =================

col1, col2 = st.columns(2)

with col1:

    st.subheader("🏆 Top Purchased Items")

    cursor.execute("""
    SELECT
        item_name,
        SUM(quantity)
    FROM purchase_items
    GROUP BY item_name
    ORDER BY SUM(quantity) DESC
    LIMIT 10
    """)

    rows = cursor.fetchall()

    if rows:

        df = pd.DataFrame(
            rows,
            columns=[
                "Item",
                "Quantity"
            ]
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No Purchase Data")


# ================= CURRENT STOCK =================

with col2:

    st.subheader("📦 Current Stock")

    cursor.execute("""
    SELECT
        item_name,
        location,
        stock,
        uom
    FROM stock_master
    ORDER BY stock DESC
    LIMIT 10
    """)

    rows = cursor.fetchall()

    if rows:

        df = pd.DataFrame(
            rows,
            columns=[
                "Item",
                "Location",
                "Stock",
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
# ================= QUICK ACTIONS =================

st.subheader("⚡ Quick Actions")

q1, q2, q3, q4 = st.columns(4)

with q1:
    if st.button("📦 Add Item", use_container_width=True):
        st.info("Go to ➜ Item Master")

with q2:
    if st.button("🛒 Purchase Entry", use_container_width=True):
        st.info("Go to ➜ Purchase Entry")

with q3:
    if st.button("🔄 Internal Transfer", use_container_width=True):
        st.info("Go to ➜ Internal Transfer")

with q4:
    if st.button("📦 Stock Management", use_container_width=True):
        st.info("Go to ➜ Stock Management")

st.divider()

# ================= SYSTEM INFORMATION =================

st.subheader("🖥️ System Information")

s1, s2, s3, s4 = st.columns(4)

with s1:
    st.metric(
        "📅 Date",
        datetime.now().strftime("%d-%m-%Y")
    )

with s2:
    st.metric(
        "🕒 Time",
        datetime.now().strftime("%H:%M:%S")
    )

with s3:
    st.metric(
        "🟢 Database",
        "Connected"
    )

with s4:
    st.metric(
        "💻 ERP Version",
        "V3.0"
    )

st.divider()

# ================= FOOTER =================

st.markdown(
    """
    <div style="text-align:center;padding:10px;">
        <h4>🏨 RTE STORE ERP MANAGEMENT SYSTEM</h4>
        <p>Developed using Python • Streamlit • SQLite</p>
        <p>© 2026 All Rights Reserved</p>
    </div>
    """,
    unsafe_allow_html=True
)

conn.close()