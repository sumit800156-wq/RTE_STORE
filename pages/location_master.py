import streamlit as st
from db import get_connection

st.title("📍 Location Master")

conn = get_connection()
cursor = conn.cursor()

# ---------- Auto Location Code ----------
cursor.execute("SELECT COUNT(*) FROM location_master")
count = cursor.fetchone()[0] + 1
location_code = f"LOC{count:03d}"

# ---------- Search ----------
search = st.text_input("🔍 Search Location")

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
        "Location Code",
        value=location_code,
        disabled=True
    )

    location_name = st.selectbox(
        "Location Name",
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

with right:
    description = st.text_area("Description")

    status = st.selectbox(
        "Status",
        [
            "Active",
            "Inactive"
        ]
    )
# ---------------- SAVE ----------------

if save_btn:

    cursor.execute("""
    INSERT INTO location_master
    (
    location_code,
    location_name,
    description,
    status
    )
    VALUES
    (?,?,?,?)
    """,
    (
        location_code,
        location_name,
        description,
        status
    ))

    conn.commit()
    st.success("✅ Location Saved Successfully")

# ---------------- NEW ----------------

if new_btn:
    st.rerun()

st.divider()

st.subheader("📋 Location List")

if search.strip() == "":

    cursor.execute("""
    SELECT
    location_code,
    location_name,
    description,
    status
    FROM location_master
    ORDER BY id DESC
    """)

else:

    cursor.execute("""
    SELECT
    location_code,
    location_name,
    description,
    status
    FROM location_master
    WHERE
    location_code LIKE ?
    OR location_name LIKE ?
    ORDER BY id DESC
    """,
    (
        f"%{search}%",
        f"%{search}%"
    ))

rows = cursor.fetchall()

if rows:
    st.dataframe(rows, use_container_width=True, hide_index=True)
else:
    st.info("No Location Found")

conn.close()