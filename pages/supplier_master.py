import streamlit as st
from db import get_connection

st.title("🚚 Supplier Master")

conn = get_connection()
cursor = conn.cursor()

# ---------- Auto Supplier Code ----------
cursor.execute("SELECT COUNT(*) FROM supplier_master")
count = cursor.fetchone()[0] + 1
supplier_code = f"SUP{count:03d}"

# ---------- Search ----------
search = st.text_input("🔍 Search Supplier")

st.divider()

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    new_btn = st.button("➕ New", use_container_width=True)

with c2:
    save_btn = st.button("💾 Save", use_container_width=True)

with c3:
    edit_btn = st.button("✏️ Edit", use_container_width=True)

with c4:
    delete_btn = st.button("🗑️ Delete", use_container_width=True)

with c5:
    search_btn = st.button("🔍 Search", use_container_width=True)

st.divider()

left, right = st.columns(2)

with left:
    st.text_input(
        "Supplier Code",
        value=supplier_code,
        disabled=True
    )

    supplier_name = st.text_input("Supplier Name")

    gst_no = st.text_input("GST No")

with right:
    address = st.text_area("Address")

    contact_person = st.text_input("Contact Person")
# ---------------- SAVE ----------------

if save_btn:

    if supplier_name.strip() == "":
        st.error("Supplier Name is required")

    else:

        cursor.execute("""
        INSERT INTO supplier_master
        (
        supplier_code,
        supplier_name,
        address,
        gst_no,
        contact_person
        )
        VALUES
        (?,?,?,?,?)
        """,
        (
            supplier_code,
            supplier_name,
            address,
            gst_no,
            contact_person
        ))

        conn.commit()

        st.success("✅ Supplier Saved Successfully")

# ---------------- NEW ----------------

if new_btn:
    st.rerun()

st.divider()

st.subheader("📋 Supplier List")

# ---------------- SEARCH ----------------

if search.strip() == "":

    cursor.execute("""
    SELECT
    supplier_code,
    supplier_name,
    gst_no,
    contact_person
    FROM supplier_master
    ORDER BY id DESC
    """)

else:

    cursor.execute("""
    SELECT
    supplier_code,
    supplier_name,
    gst_no,
    contact_person
    FROM supplier_master
    WHERE
    supplier_code LIKE ?
    OR supplier_name LIKE ?
    ORDER BY id DESC
    """,
    (
        f"%{search}%",
        f"%{search}%"
    ))

rows = cursor.fetchall()

if rows:
    st.dataframe(
        rows,
        use_container_width=True
    )
else:
    st.info("No Supplier Found")

conn.close()