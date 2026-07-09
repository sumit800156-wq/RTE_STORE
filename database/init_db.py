import sqlite3

conn = sqlite3.connect("rte_store.db")
cursor = conn.cursor()

# ================= DELETE OLD TABLES =================

tables = [
    "purchase_items",
    "purchase_entry",
    "stock_ledger",
    "stock_master",
    "internal_transfer_items",
    "internal_transfer",
    "tax_master",
    "reference_master",
    "location_master",
    "employee_master",
    "supplier_master",
    "item_master"
]

for table in tables:
    cursor.execute(f"DROP TABLE IF EXISTS {table}")

# ================= ITEM MASTER =================

cursor.execute("""
CREATE TABLE item_master(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_code TEXT UNIQUE,
    item_name TEXT NOT NULL,
    category TEXT,
    base_uom TEXT,
    sub_uom TEXT,
    material_type TEXT,
    hsn_code TEXT,
    gst TEXT,
    purchase_rate REAL,
    status TEXT
)
""")

# ================= SUPPLIER MASTER =================

cursor.execute("""
CREATE TABLE supplier_master(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier_code TEXT UNIQUE,
    supplier_name TEXT,
    address TEXT,
    gst_no TEXT,
    contact_person TEXT,
    status TEXT
)
""")

# ================= EMPLOYEE MASTER =================

cursor.execute("""
CREATE TABLE employee_master(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_code TEXT UNIQUE,
    employee_name TEXT,
    role TEXT,
    mobile TEXT,
    email TEXT,
    status TEXT
)
""")

# ================= LOCATION MASTER =================

cursor.execute("""
CREATE TABLE location_master(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_code TEXT UNIQUE,
    location_name TEXT,
    description TEXT,
    status TEXT
)
""")

# ================= REFERENCE MASTER =================

cursor.execute("""
CREATE TABLE reference_master(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    series_prefix TEXT,
    referral_no INTEGER,
    location TEXT
)
""")

# ================= TAX MASTER =================

cursor.execute("""
CREATE TABLE tax_master(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tax_code TEXT,
    cgst REAL,
    sgst REAL,
    igst REAL,
    status TEXT
)
""")

# ================= PURCHASE ENTRY =================

cursor.execute("""
CREATE TABLE purchase_entry(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reference_no TEXT,
    purchase_date TEXT,
    location TEXT,
    supplier_code TEXT,
    challan_no TEXT,
    settlement_mode TEXT,
    sub_total REAL,
    cgst REAL,
    sgst REAL,
    bill_total REAL,
    total_items INTEGER,
    total_quantity REAL
)
""")

# ================= PURCHASE ITEMS =================

cursor.execute("""
CREATE TABLE purchase_items(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    purchase_id INTEGER,
    item_code TEXT,
    item_name TEXT,
    uom TEXT,
    rate REAL,
    quantity REAL,
    amount REAL,
    gst REAL
)
""")

# ================= STOCK MASTER =================

cursor.execute("""
CREATE TABLE stock_master(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_code TEXT,
    item_name TEXT,
    location TEXT,
    stock REAL DEFAULT 0,
    purchase_rate REAL DEFAULT 0,
    uom TEXT
)
""")

# ================= STOCK LEDGER =================

cursor.execute("""
CREATE TABLE stock_ledger(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trans_date TEXT,
    trans_type TEXT,
    reference_no TEXT,
    item_code TEXT,
    item_name TEXT,
    location TEXT,
    qty_in REAL DEFAULT 0,
    qty_out REAL DEFAULT 0,
    balance REAL
)
""")

# ================= INTERNAL TRANSFER =================

cursor.execute("""
CREATE TABLE internal_transfer(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reference_no TEXT,
    transfer_date TEXT,
    from_location TEXT,
    to_location TEXT,
    template TEXT,
    purchase_ref TEXT,
    employee TEXT,
    total_items INTEGER,
    total_quantity REAL,
    sub_total REAL,
    status TEXT DEFAULT 'Completed'
)
""")

# ================= INTERNAL TRANSFER ITEMS =================

cursor.execute("""
CREATE TABLE internal_transfer_items(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transfer_id INTEGER,
    item_code TEXT,
    item_name TEXT,
    uom TEXT,
    rate REAL,
    quantity REAL,
    amount REAL
)
""")

conn.commit()
conn.close()

print("✅ RTE Store Database Initialized Successfully")