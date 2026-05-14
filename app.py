import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# =========================
# GOOGLE SHEET API
# =========================

API_URL = "https://script.google.com/macros/s/AKfycbyYnn80eP0QrXZctqTH1H3U42s4QhJZuGelZWW79VW5wAYcha60djsi8T7zMsbCsrqR/exec"

# =========================
# CONFIG
# =========================

st.set_page_config(page_title="LAIKA ERP", layout="wide")

# =========================
# SESSION INIT
# =========================

if "login" not in st.session_state:
    st.session_state.login = False

# =========================
# LOGIN SYSTEM
# =========================

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
# API FUNCTIONS (SAFE)
# =========================

def post_data(sheet, data, action="save"):

    try:
        requests.post(API_URL, json={
            "sheet": sheet,
            "action": action,
            "data": data
        }, timeout=10)

    except:
        st.error("Google Sheet connection failed")

# =========================
# SESSION DATA (LOCAL + BACKUP)
# =========================

if "sales" not in st.session_state:
    st.session_state.sales = []

if "purchase" not in st.session_state:
    st.session_state.purchase = []

if "stock" not in st.session_state:
    st.session_state.stock = {}

# =========================
# SIDEBAR
# =========================

st.sidebar.title("LAIKA ERP")

menu = st.sidebar.radio(
    "Menu",
    ["Dashboard", "Purchase", "Sales", "Expense", "Stock", "Ledger"]
)

if st.sidebar.button("Logout"):
    st.session_state.login = False
    st.rerun()

# =========================
# CALCULATION ENGINE
# =========================

sales_total = sum(x["total"] for x in st.session_state.sales)
purchase_total = sum(x["total"] for x in st.session_state.purchase)

cash = sum(x["paid"] for x in st.session_state.sales if x["payment"] == "Cash")
online = sum(x["paid"] for x in st.session_state.sales if x["payment"] == "Online")

profit = sales_total - purchase_total

# =========================
# DASHBOARD
# =========================

if menu == "Dashboard":

    st.title("📊 Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Sales", sales_total)
    col2.metric("Purchase", purchase_total)
    col3.metric("Cash", cash)
    col4.metric("Online", online)

    st.success(f"Profit: {profit}")

# =========================
# PURCHASE
# =========================

elif menu == "Purchase":

    st.title("🛒 Purchase")

    product = st.text_input("Product")
    qty = st.number_input("Qty", min_value=0.0)
    rate = st.number_input("Rate", min_value=0.0)

    total = qty * rate

    payment = st.selectbox("Payment", ["Cash", "Online"])
    paid = st.number_input("Paid", min_value=0.0)

    if st.button("Save Purchase"):

        data = {
            "time": str(datetime.now()),
            "product": product,
            "qty": qty,
            "rate": rate,
            "total": total,
            "payment": payment,
            "paid": paid
        }

        st.session_state.purchase.append(data)

        # STOCK INCREASE
        st.session_state.stock[product] = st.session_state.stock.get(product, 0) + qty

        post_data("Purchase", data)

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

    reward = int(total / 100) * 50

    payment = st.selectbox("Payment", ["Cash", "Online"])
    paid = st.number_input("Paid", min_value=0.0)

    if st.button("Save Sale"):

        # STOCK CHECK
        if product not in st.session_state.stock:
            st.error("No stock")
            st.stop()

        if st.session_state.stock[product] < qty:
            st.error("Not enough stock")
            st.stop()

        st.session_state.stock[product] -= qty

        data = {
            "time": str(datetime.now()),
            "customer": customer,
            "product": product,
            "qty": qty,
            "rate": rate,
            "total": total,
            "payment": payment,
            "paid": paid,
            "reward": reward
        }

        st.session_state.sales.append(data)

        post_data("Sales", data)

        st.success("Sale Saved")

# =========================
# EXPENSE
# =========================

elif menu == "Expense":

    st.title("💸 Expense")

    name = st.text_input("Expense Name")
    amount = st.number_input("Amount", min_value=0.0)

    if st.button("Save Expense"):

        data = {
            "time": str(datetime.now()),
            "name": name,
            "amount": amount
        }

        post_data("Expense", data)

        st.success("Saved")

# =========================
# STOCK
# =========================

elif menu == "Stock":

    st.title("📦 Stock")

    df = pd.DataFrame([
        {"Product": k, "Qty": v}
        for k, v in st.session_state.stock.items()
    ])

    st.dataframe(df)

# =========================
# LEDGER
# =========================

elif menu == "Ledger":

    st.title("📒 Ledger")

    st.write("Customers:", st.session_state.sales)
