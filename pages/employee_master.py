import streamlit as st
from db import get_connection

st.title("👨‍💼 Employee Master")

conn = get_connection()
cursor = conn.cursor()

# ---------- Auto Employee Code ----------
cursor.execute("SELECT COUNT(*) FROM employee_master")
count = cursor.fetchone()[0] + 1
employee_code = f"EMP{count:03d}"

# ---------- Search ----------
search = st.text_input("🔍 Search Employee")

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
        "Employee Code",
        value=employee_code,
        disabled=True
    )

    employee_name = st.text_input("Employee Name")

    role = st.selectbox(
        "Role",
        [
            "Admin",
            "Store Manager",
            "Purchase Manager",
            "Chef",
            "Production Manager"
        ]
    )

with right:

    mobile = st.text_input("Mobile Number")

    email = st.text_input("Email")

    status = st.selectbox(
        "Status",
        [
            "Active",
            "Inactive"
        ]
    )
    # ---------------- SAVE ----------------

if save_btn:

    if employee_name.strip() == "":
        st.error("Employee Name is required")

    else:

        cursor.execute("""
        INSERT INTO employee_master
        (
        employee_code,
        employee_name,
        role,
        mobile,
        email,
        status
        )
        VALUES
        (?,?,?,?,?,?)
        """,
        (
            employee_code,
            employee_name,
            role,
            mobile,
            email,
            status
        ))

        conn.commit()

        st.success("✅ Employee Saved Successfully")

# ---------------- NEW ----------------

if new_btn:
    st.rerun()

st.divider()

st.subheader("📋 Employee List")

# ---------------- SEARCH ----------------

if search.strip() == "":

    cursor.execute("""
    SELECT
    employee_code,
    employee_name,
    role,
    mobile,
    status
    FROM employee_master
    ORDER BY id DESC
    """)

else:

    cursor.execute("""
    SELECT
    employee_code,
    employee_name,
    role,
    mobile,
    status
    FROM employee_master
    WHERE
    employee_code LIKE ?
    OR employee_name LIKE ?
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
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No Employee Found")

conn.close()