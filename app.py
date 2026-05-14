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
# CSS (SAME UI)
# =========================

st.markdown("""

<style>

.main{
    background:#f8f5ff;
}

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
        r = requests.get(API_URL, params={"sheet": sheet}, timeout=10)
        return pd.DataFrame(r.json())
    except:
        return pd.DataFrame()

def save_data(sheet, data):
    try:
        requests.post(API_URL, json={
            "action": "save",
            "sheet": sheet,
            "data": data
        }, timeout=10)
    except:
        pass

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
            st.error("Wrong Login")

    st.stop()

# =========================
# SIDEBAR
# =========================

st.sidebar.title("🐶 LAIKA ERP")

menu = st.sidebar.radio(
    "MENU",
    ["Dashboard","Purchase","Sales","Expense","Stock","Customer Ledger","Supplier Ledger"]
)

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

# =========================
# CALCULATIONS
# =========================

sales_total = 0
purchase_total = 0
expense_total = 0
cash_total = 0
online_total = 0

if not sales_df.empty:
    if "Total" in sales_df.columns:
        sales_total = pd.to_numeric(sales_df["Total"], errors="coerce").sum()

    for _, r in sales_df.iterrows():
        paid = float(r.get("Paid",0))
        if r.get("Payment") == "Cash":
            cash_total += paid
        elif r.get("Payment") == "Online":
            online_total += paid

if not purchase_df.empty and "Total" in purchase_df.columns:
    purchase_total = pd.to_numeric(purchase_df["Total"], errors="coerce").sum()

if not expense_df.empty and "Amount" in expense_df.columns:
    expense_total = pd.to_numeric(expense_df["Amount"], errors="coerce").sum()

profit = sales_total - purchase_total - expense_total

# =========================
# DASHBOARD
# =========================

if menu == "Dashboard":

    st.title("📊 Dashboard")

    c1,c2,c3,c4 = st.columns(4)

    with c1:
        st.markdown(f'<div class="card"><h3>Sales</h3><h1>₹{sales_total}</h1></div>', unsafe_allow_html=True)

    with c2:
        st.markdown(f'<div class="card"><h3>Purchase</h3><h1>₹{purchase_total}</h1></div>', unsafe_allow_html=True)

    with c3:
        st.markdown(f'<div class="card"><h3>Cash</h3><h1>₹{cash_total}</h1></div>', unsafe_allow_html=True)

    with c4:
        st.markdown(f'<div class="card"><h3>Online</h3><h1>₹{online_total}</h1></div>', unsafe_allow_html=True)

    st.success(f"Profit: ₹ {profit}")

# =========================
# PURCHASE
# =========================

elif menu == "Purchase":

    st.title("🛒 Purchase")

    product = st.text_input("Product")
    unit = st.selectbox("Unit", ["KG","PCS","DOZEN","BAG"])
    qty = st.number_input("Qty", min_value=0.0)
    rate = st.number_input("Rate", min_value=0.0)

    total = qty * rate

    payment = st.selectbox("Payment", ["Cash","Online","Udhari"])
    paid = st.number_input("Paid", min_value=0.0)
    balance = total - paid

    if st.button("Save Purchase"):

        data = {
            "Date": str(datetime.now()),
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
# SALES
# =========================

elif menu == "Sales":

    st.title("💰 Sales")

    customer = st.text_input("Customer")
    product = st.text_input("Product")

    qty = st.number_input("Qty", min_value=0.0)
    rate = st.number_input("Rate", min_value=0.0)

    total = qty * rate

    reward = int(total/100)*50

    payment = st.selectbox("Payment", ["Cash","Online","Udhari"])
    paid = st.number_input("Paid", min_value=0.0)
    balance = total - paid

    st.success(f"Reward Points: {reward}")

    if st.button("Save Sales"):

        data = {
            "Date": str(datetime.now()),
            "Customer": customer,
            "Product": product,
            "Qty": qty,
            "Rate": rate,
            "Total": total,
            "Payment": payment,
            "Paid": paid,
            "Balance": balance,
            "Points": reward
        }

        save_data("Sales", data)
        st.success("Saved")

# =========================
# EXPENSE
# =========================

elif menu == "Expense":

    st.title("💸 Expense")

    name = st.text_input("Expense Name")
    amount = st.number_input("Amount", min_value=0.0)

    if st.button("Save Expense"):

        data = {
            "Date": str(datetime.now()),
            "Expense": name,
            "Amount": amount
        }

        save_data("Expense", data)
        st.success("Saved")

# =========================
# STOCK
# =========================

elif menu == "Stock":

    st.title("📦 Stock")
    st.dataframe(stock_df)

# =========================
# CUSTOMER LEDGER
# =========================

elif menu == "Customer Ledger":

    st.title("👤 Customer Ledger")

    name = st.text_input("Customer Name")
    amt = st.number_input("Receive Amount", min_value=0.0)

    mode = st.selectbox("Mode", ["Cash","Online"])

    if st.button("Add Payment"):

        data = {
            "Date": str(datetime.now()),
            "Customer": name,
            "Amount": amt,
            "Mode": mode
        }

        save_data("Customer", data)
        st.success("Saved")

    st.dataframe(customer_df)

# =========================
# SUPPLIER LEDGER
# =========================

elif menu == "Supplier Ledger":

    st.title("🏪 Supplier Ledger")

    name = st.text_input("Supplier Name")
    amt = st.number_input("Pay Amount", min_value=0.0)

    mode = st.selectbox("Mode", ["Cash","Online"])

    if st.button("Add Payment"):

        data = {
            "Date": str(datetime.now()),
            "Supplier": name,
            "Amount": amt,
            "Mode": mode
        }

        save_data("Supplier", data)
        st.success("Saved")

    st.dataframe(supplier_df)
