import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# =========================
# GOOGLE SHEET API
# =========================

API_URL = "https://script.google.com/macros/s/AKfycbyYnn80eP0QrXZctqTH1H3U42s4QhJZuGelZWW79VW5wAYcha60djsi8T7zMsbCsrqR/exec"

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(page_title="LAIKA ERP", layout="wide")

# =========================
# CSS (same look)
# =========================

st.markdown("""
<style>
.main { background:#f8f5ff; }

[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#7c3aed,#ec4899);
}

[data-testid="stSidebar"] *{
    color:white;
}

.stButton>button{
    width:100%;
    height:45px;
    border:none;
    border-radius:12px;
    background:linear-gradient(90deg,#8b5cf6,#ec4899);
    color:white;
    font-weight:bold;
}

.card{
    background:linear-gradient(135deg,#8b5cf6,#ec4899);
    border-radius:18px;
    padding:20px;
    color:white;
    text-align:center;
    height:150px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# SAFE API FUNCTIONS
# =========================

def get_data(sheet):
    try:
        r = requests.get(f"{API_URL}?sheet={sheet}")
        return pd.DataFrame(r.json())
    except:
        return pd.DataFrame()

def save_data(sheet, data):
    try:
        payload = {"action": "save", "sheet": sheet, "data": data}
        requests.post(API_URL, json=payload, timeout=10)
    except:
        st.error("Google Sheet Connection Error")

def delete_row(sheet, row_id):
    try:
        payload = {"action": "delete", "sheet": sheet, "id": row_id}
        requests.post(API_URL, json=payload, timeout=10)
    except:
        st.error("Delete Failed")

# =========================
# LOGIN
# =========================

if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:

    st.title("🐶 LAIKA ERP LOGIN")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        if u == "admin" and p == "admin123":
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Wrong login")

    st.stop()

# =========================
# SIDEBAR
# =========================

st.sidebar.title("LAIKA ERP")

page = st.sidebar.radio("MENU", [
    "Dashboard",
    "Purchase",
    "Sales",
    "Expense",
    "Stock",
    "Customer Ledger",
    "Supplier Ledger",
    "Settings"
])

if st.sidebar.button("Logout"):
    st.session_state.login = False
    st.rerun()

# =========================
# LOAD DATA
# =========================

sales_df = get_data("Sales")
purchase_df = get_data("Purchase")
expense_df = get_data("Expense")
stock_df = get_data("Stock")
customer_df = get_data("Customer")
supplier_df = get_data("Supplier")

# fill empty cols safety
for df in [sales_df, purchase_df]:
    if not df.empty:
        for col in ["Total","Paid","Qty","Rate"]:
            if col not in df.columns:
                df[col] = 0

# =========================
# CALCULATIONS
# =========================

sales_total = sales_df["Total"].sum() if not sales_df.empty else 0
purchase_total = purchase_df["Total"].sum() if not purchase_df.empty else 0
expense_total = expense_df["Amount"].sum() if not expense_df.empty else 0

cash_total = 0
online_total = 0

if not sales_df.empty and "Payment" in sales_df.columns:
    for _, r in sales_df.iterrows():
        if r.get("Payment") == "Cash":
            cash_total += float(r.get("Paid", 0))
        elif r.get("Payment") == "Online":
            online_total += float(r.get("Paid", 0))

profit = sales_total - purchase_total - expense_total

# =========================
# DASHBOARD
# =========================

if page == "Dashboard":

    st.title("📊 Dashboard")

    c1,c2,c3,c4 = st.columns(4)

    c1.markdown(f"<div class='card'><h3>Sales</h3><h2>₹{sales_total}</h2></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='card'><h3>Purchase</h3><h2>₹{purchase_total}</h2></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='card'><h3>Cash</h3><h2>₹{cash_total}</h2></div>", unsafe_allow_html=True)
    c4.markdown(f"<div class='card'><h3>Online</h3><h2>₹{online_total}</h2></div>", unsafe_allow_html=True)

    st.divider()

    st.success(f"Total Receive = ₹{cash_total + online_total}")
    st.info(f"Profit = ₹{profit}")

# =========================
# PURCHASE
# =========================

elif page == "Purchase":

    st.title("🛒 Purchase")

    party = st.text_input("Party Name (or CASH)")

    product = st.text_input("Product")

    unit = st.selectbox("Unit", ["KG","PCS","DOZEN","BAG"])

    qty = st.number_input("Qty", 0.0)
    rate = st.number_input("Rate", 0.0)

    total = qty * rate
    st.info(f"Total = {total}")

    payment = st.selectbox("Payment", ["Cash","Online","Udhari"])
    paid = st.number_input("Paid", 0.0)
    balance = total - paid

    if st.button("Save Purchase"):

        data = {
            "Date": str(datetime.now()),
            "Party": party,
            "Product": product,
            "Unit": unit,
            "Qty": qty,
            "Rate": rate,
            "Total": total,
            "Payment": payment,
            "Paid": paid,
            "Balance": balance
        }

        save_data("Purchase", data)
        st.success("Saved")

# =========================
# SALES + REWARD SYSTEM
# =========================

elif page == "Sales":

    st.title("💰 Sales")

    customer = st.text_input("Customer")
    product = st.text_input("Product")

    unit = st.selectbox("Unit", ["KG","PCS","DOZEN","BAG"])

    qty = st.number_input("Qty", 0.0)
    rate = st.number_input("Rate", 0.0)

    total = qty * rate

    # reward system
    points = int(total // 100) * 50

    st.success(f"Reward Points = {points}")

    payment = st.selectbox("Payment", ["Cash","Online","Udhari"])
    paid = st.number_input("Paid", 0.0)
    balance = total - paid

    if st.button("Save Sale"):

        data = {
            "Date": str(datetime.now()),
            "Customer": customer,
            "Product": product,
            "Unit": unit,
            "Qty": qty,
            "Rate": rate,
            "Total": total,
            "Payment": payment,
            "Paid": paid,
            "Balance": balance,
            "Points": points
        }

        save_data("Sales", data)
        st.success("Saved")

# =========================
# EXPENSE
# =========================

elif page == "Expense":

    st.title("Expense")

    name = st.text_input("Expense Name")
    amt = st.number_input("Amount", 0.0)

    if st.button("Save"):
        save_data("Expense", {
            "Date": str(datetime.now()),
            "Expense": name,
            "Amount": amt
        })
        st.success("Saved")

# =========================
# STOCK (AUTO VIEW)
# =========================

elif page == "Stock":

    st.title("Stock")

    st.dataframe(stock_df, use_container_width=True)

# =========================
# CUSTOMER LEDGER (WITH DELETE)
# =========================

elif page == "Customer Ledger":

    st.title("Customer Ledger")

    st.dataframe(customer_df, use_container_width=True)

    if not customer_df.empty:
        idx = st.number_input("Row Index Delete", 0, len(customer_df)-1)
        if st.button("Delete Customer Row"):
            delete_row("Customer", int(idx))

# =========================
# SUPPLIER LEDGER
# =========================

elif page == "Supplier Ledger":

    st.title("Supplier Ledger")

    st.dataframe(supplier_df, use_container_width=True)

    if not supplier_df.empty:
        idx = st.number_input("Row Index Delete", 0, len(supplier_df)-1)
        if st.button("Delete Supplier Row"):
            delete_row("Supplier", int(idx))

# =========================
# SETTINGS
# =========================

elif page == "Settings":

    st.title("Settings")
    st.success("System Running Smoothly")
