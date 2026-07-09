import streamlit as st
from db import get_connection

st.title("📄 Reference Master")

conn = get_connection()
cursor = conn.cursor()

# ---------- Auto Reference ID ----------
cursor.execute("SELECT COUNT(*) FROM reference_master")
count = cursor.fetchone()[0] + 1

st.subheader("Reference Series Setup")

series_prefix = st.selectbox(
    "Series Prefix",
    [
        "PUR",
        "PRD",
        "STK",
        "SAL"
    ]
)

referral_no = st.number_input(
    "Starting Number",
    min_value=1,
    value=1,
    step=1
)

location = st.selectbox(
    "Location",
    [
        "Central Kitchen",
        "Main Store",
        "Cold Store",
        "Dry Store",
        "Production",
        "Restaurant",
        "Warehouse"
    ]
)

col1, col2 = st.columns(2)

with col1:

    if st.button("💾 Save", use_container_width=True):

        cursor.execute("""
        INSERT INTO reference_master
        (
        series_prefix,
        referral_no,
        location
        )
        VALUES
        (?,?,?)
        """,
        (
            series_prefix,
            referral_no,
            location
        ))

        conn.commit()

        st.success("✅ Reference Saved Successfully")

with col2:

    if st.button("➕ New", use_container_width=True):
        st.rerun()

st.divider()

search = st.text_input("🔍 Search Reference")

if search == "":

    cursor.execute("""
    SELECT
    series_prefix,
    referral_no,
    location
    FROM reference_master
    ORDER BY id DESC
    """)

else:

    cursor.execute("""
    SELECT
    series_prefix,
    referral_no,
    location
    FROM reference_master
    WHERE
    series_prefix LIKE ?
    OR location LIKE ?
    ORDER BY id DESC
    """,
    (
        f"%{search}%",
        f"%{search}%"
    ))

rows = cursor.fetchall()

st.subheader("📋 Reference List")

if rows:
    st.dataframe(rows, use_container_width=True, hide_index=True)
else:
    st.info("No Reference Found")

conn.close()