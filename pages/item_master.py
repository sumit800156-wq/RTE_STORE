import streamlit as st
from db import get_connection

st.set_page_config(
    page_title="Item Master",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Item Master")

# ================= DATABASE =================

conn = get_connection()
cursor = conn.cursor()

# ================= AUTO ITEM CODE =================

cursor.execute("SELECT COUNT(*) FROM item_master")
count = cursor.fetchone()[0] + 1

item_code = f"ITM{count:04d}"

# ================= PREDEFINED ITEMS =================

ITEMS = {

# ---------- Dairy ----------
"Milk": ("Dairy","Raw Material","LTR","0401","5%"),
"Curd": ("Dairy","Raw Material","KG","0403","5%"),
"Paneer": ("Dairy","Raw Material","KG","0406","5%"),
"Butter": ("Dairy","Raw Material","KG","0405","12%"),
"Cheese": ("Dairy","Raw Material","KG","0406","12%"),
"Ghee": ("Dairy","Raw Material","LTR","0405","12%"),

# ---------- Bakery ----------
"Bread": ("Bakery","Finished Goods","PCS","1905","5%"),
"Burger Bun": ("Bakery","Finished Goods","PCS","1905","5%"),
"Pizza Base": ("Bakery","Finished Goods","PCS","1905","12%"),
"Pav": ("Bakery","Finished Goods","PCS","1905","5%"),

# ---------- Vegetable ----------
"Potato": ("Vegetable","Raw Material","KG","0701","0%"),
"Tomato": ("Vegetable","Raw Material","KG","0702","0%"),
"Onion": ("Vegetable","Raw Material","KG","0703","0%"),
"Capsicum": ("Vegetable","Raw Material","KG","0709","0%"),
"Carrot": ("Vegetable","Raw Material","KG","0706","0%"),

# ---------- Grocery ----------
"Rice": ("Grocery","Raw Material","KG","1006","5%"),
"Wheat Flour": ("Grocery","Raw Material","KG","1101","5%"),
"Maida": ("Grocery","Raw Material","KG","1101","5%"),
"Sugar": ("Grocery","Raw Material","KG","1701","5%"),
"Salt": ("Grocery","Raw Material","KG","2501","5%"),
"Cooking Oil": ("Grocery","Raw Material","LTR","1511","5%"),

# ---------- Spices ----------
"Turmeric Powder": ("Spices","Raw Material","KG","0910","5%"),
"Red Chilli Powder": ("Spices","Raw Material","KG","0904","5%"),
"Coriander Powder": ("Spices","Raw Material","KG","0909","5%"),
"Garam Masala": ("Spices","Raw Material","KG","0910","5%"),

# ---------- Disposable ----------
"CP Thali": ("Disposable","Packaging","PCS","3923","18%"),
"50 ML Container": ("Disposable","Packaging","PCS","3923","18%"),
"300 ML Container": ("Disposable","Packaging","PCS","3923","18%"),
"Sealing Roll": ("Disposable","Packaging","ROLL","3920","18%")
}

# ================= SEARCH =================

search = st.text_input("🔍 Search Item")

st.divider()
# ================= BUTTONS =================

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

# ================= ITEM DETAILS =================

left, right = st.columns(2)

with left:

    st.text_input(
        "Item Code",
        value=item_code,
        disabled=True
    )

    item_name = st.selectbox(
        "Item Name",
        sorted(ITEMS.keys())
    )

    material_type, category, base_uom, hsn_code, gst = ITEMS[item_name]

    st.text_input(
        "Material Type",
        value=material_type,
        disabled=True
    )

    st.text_input(
        "Category",
        value=category,
        disabled=True
    )

    st.text_input(
        "Base UOM",
        value=base_uom,
        disabled=True
    )

with right:

    st.text_input(
        "HSN Code",
        value=hsn_code,
        disabled=True
    )

    st.text_input(
        "GST",
        value=gst,
        disabled=True
    )

    sub_uom = st.selectbox(
        "Sub UOM",
        ["KG","GM","LTR","ML","PCS","ROLL","BOX","PACK"],
        index=["KG","GM","LTR","ML","PCS","ROLL","BOX","PACK"].index(base_uom)
        if base_uom in ["KG","GM","LTR","ML","PCS","ROLL","BOX","PACK"]
        else 0
    )

    purchase_rate = st.number_input(
        "Purchase Rate",
        min_value=0.0,
        step=1.0
    )

    status = st.selectbox(
        "Status",
        ["Active","Inactive"]
    )
    # ================= SAVE =================

if save_btn:

    cursor.execute(
        "SELECT COUNT(*) FROM item_master WHERE item_name=?",
        (item_name,)
    )

    if cursor.fetchone()[0] > 0:

        st.error("⚠️ Item Already Exists")

    else:

        cursor.execute("""
        INSERT INTO item_master
        (
            item_code,
            item_name,
            category,
            base_uom,
            sub_uom,
            material_type,
            hsn_code,
            gst,
            purchase_rate,
            status
        )
        VALUES
        (?,?,?,?,?,?,?,?,?,?)
        """,
        (
            item_code,
            item_name,
            category,
            base_uom,
            sub_uom,
            material_type,
            hsn_code,
            gst,
            purchase_rate,
            status
        ))

        conn.commit()

        st.success("✅ Item Saved Successfully")

        st.rerun()

# ================= NEW =================

if new_btn:
    st.rerun()
    # ================= ITEM LIST =================

st.divider()

st.subheader("📋 Item Master List")

if search.strip() == "":

    cursor.execute("""
    SELECT
        item_code,
        item_name,
        material_type,
        category,
        base_uom,
        gst,
        purchase_rate,
        status
    FROM item_master
    ORDER BY id DESC
    """)

else:

    cursor.execute("""
    SELECT
        item_code,
        item_name,
        material_type,
        category,
        base_uom,
        gst,
        purchase_rate,
        status
    FROM item_master
    WHERE
        item_code LIKE ?
        OR item_name LIKE ?
        OR material_type LIKE ?
    ORDER BY id DESC
    """,
    (
        f"%{search}%",
        f"%{search}%",
        f"%{search}%"
    ))

rows = cursor.fetchall()

if rows:

    st.dataframe(
        rows,
        column_config={
            0: "Item Code",
            1: "Item Name",
            2: "Material Type",
            3: "Category",
            4: "Base UOM",
            5: "GST",
            6: "Purchase Rate",
            7: "Status"
        },
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("No Item Found")


# ================= DELETE =================

if delete_btn:

    if search.strip() == "":

        st.warning("⚠️ Search Item Code or Item Name First")

    else:

        cursor.execute(
            """
            DELETE FROM item_master
            WHERE item_code=? OR item_name=?
            """,
            (search, search)
        )

        conn.commit()

        st.success("✅ Item Deleted Successfully")

        st.rerun()

conn.close()