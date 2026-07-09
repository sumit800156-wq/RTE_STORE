import streamlit as st
from db import get_connection
from datetime import date

st.title("🛒 Purchase Entry")

conn = get_connection()
cursor = conn.cursor()

# ---------------- Auto Reference Number ----------------

cursor.execute("SELECT COUNT(*) FROM purchase_entry")
count = cursor.fetchone()[0] + 1
reference_no = f"PUR{count:04d}"

# ---------------- Supplier List ----------------

cursor.execute("SELECT supplier_name FROM supplier_master")
supplier_list = [row[0] for row in cursor.fetchall()]

# ---------------- Location List ----------------

cursor.execute("SELECT location_name FROM location_master")
location_list = [row[0] for row in cursor.fetchall()]

st.subheader("Purchase Header")

col1, col2 = st.columns(2)

with col1:

    st.text_input(
        "Reference No",
        value=reference_no,
        disabled=True
    )

    purchase_date = st.date_input(
        "Purchase Date",
        value=date.today()
    )

    supplier = st.selectbox(
        "Supplier",
        supplier_list if supplier_list else ["No Supplier Found"]
    )

with col2:

    location = st.selectbox(
        "Location",
        location_list if location_list else ["No Location Found"]
    )

    challan_no = st.text_input(
        "Challan No"
    )

    settlement_mode = st.selectbox(
        "Settlement Mode",
        [
            "Cash",
            "Credit",
            "Bank"
        ]
    )

st.divider()

st.subheader("Item Details")
# ---------------- Item List ----------------

cursor.execute("""
SELECT
item_code,
item_name,
base_uom,
purchase_rate,
gst
FROM item_master
""")

items = cursor.fetchall()

item_names = [i[1] for i in items]

selected_item = st.selectbox(
    "Select Item",
    item_names if item_names else ["No Item Found"]
)

item_code = ""
uom = ""
rate = 0.0
gst = "0%"

for i in items:
    if i[1] == selected_item:
        item_code = i[0]
        uom = i[2]
        rate = i[3]
        gst = i[4]
        break

col1, col2, col3 = st.columns(3)

with col1:
    st.text_input(
        "Item Code",
        value=item_code,
        disabled=True
    )

    st.text_input(
        "UOM",
        value=uom,
        disabled=True
    )

with col2:

    lpr = st.number_input(
        "LPR",
        value=float(rate),
        disabled=True
    )

    quantity = st.number_input(
        "Quantity",
        min_value=0.0,
        step=1.0
    )

with col3:

    st.text_input(
        "GST",
        value=str(gst),
        disabled=True
    )

    amount = quantity * float(rate)

    st.number_input(
        "Amount",
        value=float(amount),
        disabled=True
    )

add_item = st.button(
    "➕ Add Item",
    use_container_width=True
)

if "purchase_items" not in st.session_state:
    st.session_state.purchase_items = []

if add_item:

    st.session_state.purchase_items.append({
        "Item Code": item_code,
        "Item Name": selected_item,
        "UOM": uom,
        "Rate": rate,
        "Qty": quantity,
        "GST": gst,
        "Amount": amount
    })

    st.success("✅ Item Added Successfully")
# ---------------- Purchase Item List ----------------

st.divider()
st.subheader("🛒 Purchase Item List")

if len(st.session_state.purchase_items) > 0:

    st.dataframe(
        st.session_state.purchase_items,
        use_container_width=True,
        hide_index=True
    )

    total_items = len(st.session_state.purchase_items)

    total_qty = sum(
        item["Qty"] for item in st.session_state.purchase_items
    )

    sub_total = sum(
        item["Amount"] for item in st.session_state.purchase_items
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Items", total_items)

    with col2:
        st.metric("Total Quantity", total_qty)

    with col3:
        st.metric("Sub Total", f"₹ {sub_total:.2f}")

    if st.button("🗑️ Clear All Items", use_container_width=True):
        st.session_state.purchase_items = []
        st.rerun()

else:
    st.info("No Item Added")
    # ---------- Default Values ----------

total_items = 0
total_qty = 0
sub_total = 0

if len(st.session_state.purchase_items) > 0:
    total_items = len(st.session_state.purchase_items)
    total_qty = sum(item["Qty"] for item in st.session_state.purchase_items)
    sub_total = sum(item["Amount"] for item in st.session_state.purchase_items)
# ================= BILL CALCULATION =================

st.divider()
st.subheader("💰 Bill Summary")

cgst = sub_total * 0.025
sgst = sub_total * 0.025

bill_total = sub_total + cgst + sgst

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("CGST", f"₹ {cgst:.2f}")

with c2:
    st.metric("SGST", f"₹ {sgst:.2f}")

with c3:
    st.metric("Bill Total", f"₹ {bill_total:.2f}")

st.divider()

if st.button("💾 Save Purchase", use_container_width=True):

    if len(st.session_state.purchase_items) == 0:
        st.error("Please Add Item First")

    else:

        cursor.execute("""
        INSERT INTO purchase_entry
        (
        reference_no,
        purchase_date,
        location,
        supplier_code,
        challan_no,
        settlement_mode,
        sub_total,
        cgst,
        sgst,
        bill_total,
        total_items,
        total_quantity
        )
        VALUES
        (?,?,?,?,?,?,?,?,?,?,?,?)
        """,
        (
            reference_no,
            str(purchase_date),
            location,
            supplier,
            challan_no,
            settlement_mode,
            sub_total,
            cgst,
            sgst,
            bill_total,
            total_items,
            total_qty
        ))

        purchase_id = cursor.lastrowid

        for item in st.session_state.purchase_items:

            cursor.execute("""
            INSERT INTO purchase_items
            (
            purchase_id,
            item_code,
            item_name,
            uom,
            rate,
            quantity,
            amount,
            gst
            )
            VALUES
            (?,?,?,?,?,?,?,?)
            """,
            (
                purchase_id,
                item["Item Code"],
                item["Item Name"],
                item["UOM"],
                item["Rate"],
                item["Qty"],
                item["Amount"],
                item["GST"]
            ))
            # ================= STOCK MASTER UPDATE =================

            cursor.execute("""
            SELECT stock
            FROM stock_master
            WHERE item_code=? AND location=?
            """, (
                item["Item Code"],
                location
            ))

            result = cursor.fetchone()

            if result:

                new_stock = result[0] + item["Qty"]

                cursor.execute("""
                UPDATE stock_master
                SET stock=?
                WHERE item_code=? AND location=?
                """, (
                    new_stock,
                    item["Item Code"],
                    location
                ))

            else:

                new_stock = item["Qty"]

                cursor.execute("""
                INSERT INTO stock_master
                (
                item_code,
                item_name,
                location,
                stock,
                uom
                )
                VALUES
                (?,?,?,?,?)
                """, (
                    item["Item Code"],
                    item["Item Name"],
                    location,
                    item["Qty"],
                    item["UOM"]
                ))

            # ================= STOCK LEDGER =================

            cursor.execute("""
            INSERT INTO stock_ledger
            (
            trans_date,
            trans_type,
            reference_no,
            item_code,
            item_name,
            location,
            qty_in,
            qty_out,
            balance
            )
            VALUES
            (?,?,?,?,?,?,?,?,?)
            """, (
                str(purchase_date),
                "PURCHASE",
                reference_no,
                item["Item Code"],
                item["Item Name"],
                location,
                item["Qty"],
                0,
                new_stock
            ))

        conn.commit()

        st.success("✅ Purchase Saved Successfully")

        st.session_state.purchase_items = []

        st.rerun()

conn.close()
# ================= PURCHASE HISTORY =================

st.divider()
st.subheader("📋 Purchase History")

search_ref = st.text_input("🔍 Search Reference No")

if search_ref.strip() == "":

    cursor = get_connection().cursor()

    cursor.execute("""
    SELECT
    reference_no,
    purchase_date,
    supplier_code,
    location,
    bill_total
    FROM purchase_entry
    ORDER BY id DESC
    """)

else:

    cursor = get_connection().cursor()

    cursor.execute("""
    SELECT
    reference_no,
    purchase_date,
    supplier_code,
    location,
    bill_total
    FROM purchase_entry
    WHERE reference_no LIKE ?
    ORDER BY id DESC
    """,
    (
        f"%{search_ref}%",
    ))

history = cursor.fetchall()

if history:

    st.dataframe(
        history,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("No Purchase Found")