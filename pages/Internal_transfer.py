import streamlit as st
from db import get_connection

st.set_page_config(
    page_title="Internal Transfer",
    page_icon="🔄",
    layout="wide"
)

st.title("🔄 Internal Transfer")

conn = get_connection()
cursor = conn.cursor()

st.info("Internal Transfer Module ")
from datetime import date

# ================= AUTO REFERENCE =================

cursor.execute("SELECT COUNT(*) FROM internal_transfer")
count = cursor.fetchone()[0] + 1
reference_no = f"TRF{count:04d}"

# ================= LOCATION LIST =================

cursor.execute("""
SELECT location_name
FROM location_master
ORDER BY location_name
""")

location_list = [row[0] for row in cursor.fetchall()]

# ================= EMPLOYEE LIST =================

cursor.execute("""
SELECT employee_name
FROM employee_master
ORDER BY employee_name
""")

employee_list = [row[0] for row in cursor.fetchall()]

st.subheader("Transfer Header")

col1, col2 = st.columns(2)

with col1:

    st.text_input(
        "Reference No",
        value=reference_no,
        disabled=True
    )

    transfer_date = st.date_input(
        "Transfer Date",
        value=date.today()
    )

    from_location = st.selectbox(
        "From Location",
        location_list if location_list else ["No Location"]
    )

    template = st.text_input(
        "Template"
    )

with col2:

    to_location = st.selectbox(
        "To Location",
        location_list if location_list else ["No Location"]
    )

    purchase_ref = st.text_input(
        "Purchase Entry No."
    )

    employee = st.selectbox(
        "Employee",
        employee_list if employee_list else ["No Employee"]
    )

# ================= VALIDATION =================

if from_location == to_location:
    st.warning("⚠️ From Location and To Location cannot be the same.")
st.divider()
st.subheader("📦 Item Details")

# ================= ITEM LIST =================

cursor.execute("""
SELECT
item_code,
item_name,
base_uom,
purchase_rate
FROM item_master
ORDER BY item_name
""")

items = cursor.fetchall()

item_names = [i[1] for i in items]

selected_item = st.selectbox(
    "Select Item",
    item_names if item_names else ["No Item Found"]
)

item_code = ""
item_name = ""
uom = ""
rate = 0.0
balance_qty = 0.0

for i in items:
    if i[1] == selected_item:
        item_code = i[0]
        item_name = i[1]
        uom = i[2]
        rate = i[3]
        break

# ================= CURRENT STOCK =================

cursor.execute("""
SELECT stock
FROM stock_master
WHERE item_code=? AND location=?
""", (
    item_code,
    from_location
))

stock = cursor.fetchone()

if stock:
    balance_qty = stock[0]

col1, col2, col3 = st.columns(3)

with col1:

    st.text_input(
        "Item Code",
        value=item_code,
        disabled=True
    )

    st.text_input(
        "Description",
        value=item_name,
        disabled=True
    )

with col2:

    st.text_input(
        "UOM",
        value=uom,
        disabled=True
    )

    st.number_input(
        "Balance Quantity",
        value=float(balance_qty),
        disabled=True
    )

with col3:

    st.number_input(
        "Rate",
        value=float(rate),
        disabled=True
    )

    quantity = st.number_input(
        "Transfer Quantity",
        min_value=0.0,
        step=1.0
    )

amount = quantity * float(rate)

st.number_input(
    "Amount",
    value=float(amount),
    disabled=True
)

col1, col2 = st.columns(2)

add_item = col1.button(
    "➕ Add Item",
    use_container_width=True
)

cancel_item = col2.button(
    "❌ Cancel",
    use_container_width=True
)

# ================= SESSION =================

if "transfer_items" not in st.session_state:
    st.session_state.transfer_items = []

if add_item:

    if quantity <= 0:
        st.error("Enter Quantity")

    elif quantity > balance_qty:
        st.error("Insufficient Stock")

    else:

        st.session_state.transfer_items.append({
            "Item Code": item_code,
            "Description": item_name,
            "UOM": uom,
            "Rate": rate,
            "Quantity": quantity,
            "Amount": amount
        })

        st.success("Item Added Successfully")

if cancel_item:
    st.session_state.transfer_items = []
    st.rerun()
    # ================= TRANSFER ITEM LIST =================

st.divider()
st.subheader("📋 Transfer Item List")

if len(st.session_state.transfer_items) > 0:

    st.dataframe(
        st.session_state.transfer_items,
        use_container_width=True,
        hide_index=True
    )

    total_items = len(st.session_state.transfer_items)

    total_qty = sum(
        item["Quantity"] for item in st.session_state.transfer_items
    )

    sub_total = sum(
        item["Amount"] for item in st.session_state.transfer_items
    )

else:

    total_items = 0
    total_qty = 0
    sub_total = 0

    st.info("No Item Added")

# ================= SUMMARY =================

st.divider()
st.subheader("📊 Transfer Summary")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Total Items", total_items)

with c2:
    st.metric("Total Quantity", total_qty)

with c3:
    st.metric("Sub Total", f"₹ {sub_total:.2f}")

# ================= BUTTONS =================

col1, col2, col3 = st.columns(3)

recalculate = col1.button(
    "🔄 Recalculate",
    use_container_width=True
)

clear_items = col2.button(
    "🗑️ Clear",
    use_container_width=True
)

save_transfer = col3.button(
    "✅ OK",
    use_container_width=True
)

if recalculate:
    st.rerun()

if clear_items:
    st.session_state.transfer_items = []
    st.success("Items Cleared")
    st.rerun()
if save_transfer:

    if len(st.session_state.transfer_items) == 0:

        st.error("Please Add Item First")

    elif from_location == to_location:

        st.error("From Location and To Location cannot be same")

    else:

        # ================= SAVE HEADER =================

        cursor.execute("""
        INSERT INTO internal_transfer
        (
            reference_no,
            transfer_date,
            from_location,
            to_location,
            template,
            purchase_ref,
            employee,
            total_items,
            total_quantity,
            sub_total
        )
        VALUES (?,?,?,?,?,?,?,?,?,?)
        """, (
            reference_no,
            str(transfer_date),
            from_location,
            to_location,
            template,
            purchase_ref,
            employee,
            total_items,
            total_qty,
            sub_total
        ))

        transfer_id = cursor.lastrowid

        # ================= SAVE ITEMS =================

        for item in st.session_state.transfer_items:

            cursor.execute("""
            INSERT INTO internal_transfer_items
            (
                transfer_id,
                item_code,
                item_name,
                uom,
                rate,
                quantity,
                amount
            )
            VALUES (?,?,?,?,?,?,?)
            """, (
                transfer_id,
                item["Item Code"],
                item["Description"],
                item["UOM"],
                item["Rate"],
                item["Quantity"],
                item["Amount"]
            ))

            # ================= FROM LOCATION STOCK =================

            cursor.execute("""
            UPDATE stock_master
            SET stock = stock - ?
            WHERE item_code=? AND location=?
            """, (
                item["Quantity"],
                item["Item Code"],
                from_location
            ))

            # ================= TO LOCATION STOCK =================

            cursor.execute("""
            SELECT stock
            FROM stock_master
            WHERE item_code=? AND location=?
            """, (
                item["Item Code"],
                to_location
            ))

            result = cursor.fetchone()

            if result:

                cursor.execute("""
                UPDATE stock_master
                SET stock = stock + ?
                WHERE item_code=? AND location=?
                """, (
                    item["Quantity"],
                    item["Item Code"],
                    to_location
                ))

            else:

                cursor.execute("""
                INSERT INTO stock_master
                (
                    item_code,
                    item_name,
                    location,
                    stock,
                    uom
                )
                VALUES (?,?,?,?,?)
                """, (
                    item["Item Code"],
                    item["Description"],
                    to_location,
                    item["Quantity"],
                    item["UOM"]
                ))

            # ================= STOCK LEDGER OUT =================

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
            VALUES (?,?,?,?,?,?,?,?,?)
            """, (
                str(transfer_date),
                "TRANSFER OUT",
                reference_no,
                item["Item Code"],
                item["Description"],
                from_location,
                0,
                item["Quantity"],
                0
            ))

            # ================= STOCK LEDGER IN =================

            cursor.execute("""
            SELECT stock
            FROM stock_master
            WHERE item_code=? AND location=?
            """, (
                item["Item Code"],
                to_location
            ))

            new_balance = cursor.fetchone()[0]

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
            VALUES (?,?,?,?,?,?,?,?,?)
            """, (
                str(transfer_date),
                "TRANSFER IN",
                reference_no,
                item["Item Code"],
                item["Description"],
                to_location,
                item["Quantity"],
                0,
                new_balance
            ))

        conn.commit()

        st.success("✅ Internal Transfer Saved Successfully")

        st.session_state.transfer_items = []

        st.rerun()