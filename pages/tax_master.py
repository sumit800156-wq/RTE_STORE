import streamlit as st
from db import get_connection

st.title("💰 Tax Master")

conn = get_connection()
cursor = conn.cursor()

search = st.text_input("🔍 Search Tax Code")

st.divider()

tax_code = st.selectbox(
    "Tax Code",
    [
        "GST 0%",
        "GST 5%",
        "GST 12%",
        "GST 18%",
        "GST 28%"
    ]
)

# Auto Tax Values
if tax_code == "GST 0%":
    cgst, sgst, igst = 0.0, 0.0, 0.0

elif tax_code == "GST 5%":
    cgst, sgst, igst = 2.5, 2.5, 5.0

elif tax_code == "GST 12%":
    cgst, sgst, igst = 6.0, 6.0, 12.0

elif tax_code == "GST 18%":
    cgst, sgst, igst = 9.0, 9.0, 18.0

elif tax_code == "GST 28%":
    cgst, sgst, igst = 14.0, 14.0, 28.0

col1, col2 = st.columns(2)

with col1:
    st.number_input(
        "CGST %",
        value=float(cgst),
        disabled=True
    )

    st.number_input(
        "SGST %",
        value=float(sgst),
        disabled=True
    )

with col2:
    st.number_input(
        "IGST %",
        value=float(igst),
        disabled=True
    )

    status = st.selectbox(
        "Status",
        ["Active", "Inactive"]
    )

col1, col2 = st.columns(2)

with col1:
    if st.button("💾 Save", use_container_width=True):

        cursor.execute("""
        INSERT INTO tax_master
        (
        tax_code,
        cgst,
        sgst,
        igst,
        status
        )
        VALUES
        (?,?,?,?,?)
        """,
        (
            tax_code,
            cgst,
            sgst,
            igst,
            status
        ))

        conn.commit()

        st.success("✅ Tax Saved Successfully")

with col2:
    if st.button("➕ New", use_container_width=True):
        st.rerun()

st.divider()

st.subheader("📋 Tax List")

if search == "":
    cursor.execute("""
    SELECT tax_code,cgst,sgst,igst,status
    FROM tax_master
    ORDER BY id DESC
    """)
else:
    cursor.execute("""
    SELECT tax_code,cgst,sgst,igst,status
    FROM tax_master
    WHERE tax_code LIKE ?
    ORDER BY id DESC
    """, (f"%{search}%",))

rows = cursor.fetchall()

if rows:
    st.dataframe(rows, use_container_width=True, hide_index=True)
else:
    st.info("No Tax Record Found")

conn.close()