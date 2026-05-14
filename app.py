import streamlit as st
import requests
from datetime import datetime

API_URL = "https://script.google.com/macros/s/AKfycbyYnn80eP0QrXZctqTH1H3U42s4QhJZuGelZWW79VW5wAYcha60djsi8T7zMsbCsrqR/exec"

st.set_page_config(page_title="Laika ERP", layout="wide")

# ======================
# SESSION INIT
# ======================

if "login" not in st.session_state:
    st.session_state.login = False

if "stock" not in st.session_state:
    st.session_state.stock = {}

if "purchase" not in st.session_state:
    st.session_state.purchase = []

if "sales" not in st.session_state:
    st.session_state.sales = []

if "customer" not in st.session_state:
    st.session_state.customer = {}

# ======================
# LOGIN
# ======================

if not st.session_state.login:

    st.title("🔐 LAIKA ERP LOGIN")

    u = st.text_input("User")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        if u == "admin" and p == "admin":
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Wrong login")

    st.stop()

# ======================
# SAFE GOOGLE SHEET PUSH
# ======================

def send(sheet, data):

    try:
        requests.post(API_URL, json={
            "sheet": sheet,
            "data": data
        }, timeout=5)
    except:
        pass

# ======================
# SIDEBAR
# ======================

st.sidebar.title("LAIKA ERP")

menu = st.sidebar.radio(
    "Menu",
    ["Dashboard", "Purchase", "Sales", "Stock", "Customer"]
)

# ======================
# STOCK ALERT STYLE
# ======================

def stock_color(qty):
    if qty <= 2:
        return "🔴 LOW"
    return "🟢 OK"

# ======================
# DASHBOARD
# ======================

if menu == "Dashboard":

    st.title("📊 Dashboard")

    total_purchase = sum(x["total"] for x in st.session_state.purchase)
    total_sales = sum(x["total"] for x in st.session_state.sales)

    cash = sum(x["paid"] for x in st.session_state.sales if x["payment"] == "Cash")
    online = sum(x["paid"] for x in st.session_state.sales if x["payment"] == "Online")

    col1, col2, col3 = st.columns(3)

    col1.metric("Purchase", total_purchase)
    col2.metric("Sales", total_sales)
    col3.metric("Profit", total_sales - total_purchase)

    st.write("Cash:", cash)
    st.write("Online:", online)

# ======================
# PURCHASE
# ======================

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

        # STOCK + ADD
        st.session_state.stock[product] = st.session_state.stock.get(product, 0) + qty

        send("Purchase", data)

        st.success("Saved")

# ======================
# SALES
# ======================

elif menu == "Sales":

    st.title("💰 Sales")

    customer = st.text_input("Customer")
    product = st.text_input("Product")
    qty = st.number_input("Qty", min_value=0.0)
    rate = st.number_input("Rate", min_value=0.0)

    total = qty * rate

    payment = st.selectbox("Payment", ["Cash", "Online"])
    paid = st.number_input("Paid", min_value=0.0)

    if st.button("Save Sale"):

        if product not in st.session_state.stock:
            st.error("No stock")
            st.stop()

        if st.session_state.stock[product] < qty:
            st.error("Low stock")
            st.stop()

        # STOCK MINUS
        st.session_state.stock[product] -= qty

        # CUSTOMER LEDGER
        st.session_state.customer.setdefault(customer, 0)
        st.session_state.customer[customer] += (total - paid)

        data = {
            "time": str(datetime.now()),
            "customer": customer,
            "product": product,
            "qty": qty,
            "rate": rate,
            "total": total,
            "payment": payment,
            "paid": paid
        }

        st.session_state.sales.append(data)

        send("Sales", data)

        st.success("Saved")

# ======================
# STOCK
# ======================

elif menu == "Stock":

    st.title("📦 Stock")

    for k, v in st.session_state.stock.items():

        st.write(f"{k} → {v} {stock_color(v)}")

# ======================
# CUSTOMER
# ======================

elif menu == "Customer":

    st.title("👤 Customer Ledger")

    for k, v in st.session_state.customer.items():

        st.write(f"{k} → Pending ₹{v}")

        pay = st.number_input(f"Receive from {k}", min_value=0.0, key=k)

        mode = st.selectbox(f"Mode {k}", ["Cash", "Online"], key=k+"m")

        if st.button(f"Add Payment {k}"):

            st.session_state.customer[k] -= pay

            send("Customer", {
                "name": k,
                "amount": pay,
                "mode": mode
            })

            st.success("Updated")
