import streamlit as st

st.set_page_config(
    page_title="RTE Store Management",
    page_icon="🏪",
    layout="wide"
)

st.title("🏪 RTE Store Management System")

st.sidebar.title("Navigation")

page = st.sidebar.selectbox(
    "Select Module",
    [
        "Dashboard",
        "Item Master",
        "Supplier Master",
        "Employee Master",
        "Location Master",
        "Tax Master",
        "Reference Master",
        "Purchase Entry"
    ]
)

# Dashboard
if page == "Dashboard":
    st.header("📊 Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Items", "0")
    col2.metric("Suppliers", "0")
    col3.metric("Employees", "0")
    col4.metric("Locations", "0")

    st.divider()

    st.subheader("System Overview")

    st.info("""
Welcome to RTE Store Management System.

Modules:
✔ Dashboard
✔ Item Master
✔ Supplier Master
✔ Employee Master
✔ Location Master
✔ Tax Master
✔ Reference Master
✔ Purchase Entry
""")

# Item Master
elif page == "Item Master":
    exec(open("pages/item_master.py").read())

# Supplier Master
elif page == "Supplier Master":
    exec(open("pages/supplier_master.py").read())

# Employee Master
elif page == "Employee Master":
    exec(open("pages/employee_master.py").read())

# Location Master
elif page == "Location Master":
    exec(open("pages/location_master.py").read())

# Tax Master
elif page == "Tax Master":
    exec(open("pages/tax_master.py").read())

# Reference Master
elif page == "Reference Master":
    exec(open("pages/reference_master.py").read())

# Purchase Entry
elif page == "Purchase Entry":
    exec(open("pages/purchase_entry.py").read())