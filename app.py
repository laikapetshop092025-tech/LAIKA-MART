import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# =========================================
# GOOGLE SHEET API
# =========================================

API_URL = "https://script.google.com/macros/s/AKfycbyYnn80eP0QrXZctqTH1H3U42s4QhJZuGelZWW79VW5wAYcha60djsi8T7zMsbCsrqR/exec"

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="LAIKA ERP",
    layout="wide"
)

# =========================================
# CSS
# =========================================

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

# =========================================
# FUNCTIONS
# =========================================

def get_data(sheet):

    try:

        response = requests.get(
            f"{API_URL}?sheet={sheet}"
        )

        data = response.json()

        return pd.DataFrame(data)

    except:

        return pd.DataFrame()

def save_data(sheet, data):

    payload = {
        "action":"save",
        "sheet":sheet,
        "data":data
    }

    requests.post(API_URL, json=payload)

# =========================================
# LOGIN
# =========================================

if "login" not in st.session_state:
    st.session_state.login = False

if st.session_state.login == False:

    st.title("🐶 LAIKA ERP LOGIN")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if username == "admin" and password == "admin123":

            st.session_state.login = True
            st.rerun()

        else:

            st.error("Wrong Username or Password")

    st.info("Username = admin")
    st.info("Password = admin123")

    st.stop()

# =========================================
# SIDEBAR
# =========================================

st.sidebar.title("🐶 LAIKA ERP")

page = st.sidebar.radio(
    "MENU",
    [
        "Dashboard",
        "Purchase",
        "Sales",
        "Expense",
        "Stock",
        "Customer Ledger",
        "Supplier Ledger",
        "Settings"
    ]
)

if st.sidebar.button("Logout"):

    st.session_state.login = False
    st.rerun()

# =========================================
# LOAD DATA
# =========================================

sales_df = get_data("Sales")
purchase_df = get_data("Purchase")
expense_df = get_data("Expense")
stock_df = get_data("Stock")
customer_df = get_data("Customer")
supplier_df = get_data("Supplier")

# =========================================
# TOTALS
# =========================================

sales_total = 0
purchase_total = 0
expense_total = 0
cash_total = 0
online_total = 0

if not sales_df.empty:

    if "Total" in sales_df.columns:

        sales_total = pd.to_numeric(
            sales_df["Total"],
            errors="coerce"
        ).sum()

    if "Payment" in sales_df.columns:

        for _,row in sales_df.iterrows():

            payment = str(row.get("Payment",""))

            paid = float(row.get("Paid",0))

            if payment == "Cash":

                cash_total += paid

            elif payment == "Online":

                online_total += paid

if not purchase_df.empty:

    if "Total" in purchase_df.columns:

        purchase_total = pd.to_numeric(
            purchase_df["Total"],
            errors="coerce"
        ).sum()

if not expense_df.empty:

    if "Amount" in expense_df.columns:

        expense_total = pd.to_numeric(
            expense_df["Amount"],
            errors="coerce"
        ).sum()

profit_total = (
    sales_total
    - purchase_total
    - expense_total
)

# =========================================
# DASHBOARD
# =========================================

if page == "Dashboard":

    st.title("📊 Dashboard")

    c1,c2,c3,c4 = st.columns(4)

    with c1:

        st.markdown(f"""
        <div class="card">
        <h3>Total Sales</h3>
        <h1>₹ {sales_total}</h1>
        </div>
        """, unsafe_allow_html=True)

    with c2:

        st.markdown(f"""
        <div class="card">
        <h3>Total Purchase</h3>
        <h1>₹ {purchase_total}</h1>
        </div>
        """, unsafe_allow_html=True)

    with c3:

        st.markdown(f"""
        <div class="card">
        <h3>Cash Receive</h3>
        <h1>₹ {cash_total}</h1>
        </div>
        """, unsafe_allow_html=True)

    with c4:

        st.markdown(f"""
        <div class="card">
        <h3>Online Receive</h3>
        <h1>₹ {online_total}</h1>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    c5,c6 = st.columns(2)

    with c5:

        st.markdown(f"""
        <div class="card">
        <h3>Total Receive</h3>
        <h1>₹ {cash_total + online_total}</h1>
        </div>
        """, unsafe_allow_html=True)

    with c6:

        st.markdown(f"""
        <div class="card">
        <h3>Total Profit</h3>
        <h1>₹ {profit_total}</h1>
        </div>
        """, unsafe_allow_html=True)

# =========================================
# PURCHASE
# =========================================

elif page == "Purchase":

    st.title("🛒 Purchase")

    product = st.text_input("Product Name")

    unit = st.selectbox(
        "Unit",
        ["KG","PCS","DOZEN","BAG"]
    )

    qty = st.number_input(
        "Quantity",
        min_value=0.0
    )

    rate = st.number_input(
        "Rate",
        min_value=0.0
    )

    total = qty * rate

    st.info(f"Total = ₹ {total}")

    payment = st.selectbox(
        "Payment",
        ["Cash","Online","Udhari"]
    )

    paid = st.number_input(
        "Paid Amount",
        min_value=0.0
    )

    balance = total - paid

    st.warning(f"Balance = ₹ {balance}")

    if st.button("Save Purchase"):

        data = {

            "Date":str(datetime.now()),
            "Product":product,
            "Unit":unit,
            "Qty":qty,
            "Rate":rate,
            "Total":total,
            "Payment":payment,
            "Paid":paid,
            "Balance":balance

        }

        save_data("Purchase", data)

        st.success("Purchase Saved")

# =========================================
# SALES
# =========================================

elif page == "Sales":

    st.title("💰 Sales")

    customer = st.text_input("Customer Name")

    product = st.text_input("Product Name")

    unit = st.selectbox(
        "Sales Unit",
        ["KG","PCS","DOZEN","BAG"]
    )

    qty = st.number_input(
        "Sales Qty",
        min_value=0.0
    )

    rate = st.number_input(
        "Sales Rate",
        min_value=0.0
    )

    total = qty * rate

    reward_points = int(total / 100) * 50

    st.success(
        f"Reward Points = {reward_points}"
    )

    payment = st.selectbox(
        "Sales Payment",
        ["Cash","Online","Udhari"]
    )

    paid = st.number_input(
        "Sales Paid Amount",
        min_value=0.0
    )

    balance = total - paid

    st.warning(f"Balance = ₹ {balance}")

    if st.button("Save Sales"):

        data = {

            "Date":str(datetime.now()),
            "Customer":customer,
            "Product":product,
            "Unit":unit,
            "Qty":qty,
            "Rate":rate,
            "Total":total,
            "Payment":payment,
            "Paid":paid,
            "Balance":balance,
            "Points":reward_points

        }

        save_data("Sales", data)

        st.success("Sales Saved")

# =========================================
# EXPENSE
# =========================================

elif page == "Expense":

    st.title("💸 Expense")

    expense = st.text_input(
        "Expense Name"
    )

    amount = st.number_input(
        "Amount",
        min_value=0.0
    )

    if st.button("Save Expense"):

        data = {

            "Date":str(datetime.now()),
            "Expense":expense,
            "Amount":amount

        }

        save_data("Expense", data)

        st.success("Expense Saved")

# =========================================
# STOCK
# =========================================

elif page == "Stock":

    st.title("📦 Stock")

    st.dataframe(
        stock_df,
        use_container_width=True
    )

# =========================================
# CUSTOMER LEDGER
# =========================================

elif page == "Customer Ledger":

    st.title("👤 Customer Ledger")

    st.dataframe(
        customer_df,
        use_container_width=True
    )

# =========================================
# SUPPLIER LEDGER
# =========================================

elif page == "Supplier Ledger":

    st.title("🏪 Supplier Ledger")

    st.dataframe(
        supplier_df,
        use_container_width=True
    )

# =========================================
# SETTINGS
# =========================================

elif page == "Settings":

    st.title("⚙️ Settings")

    st.success("ERP Running Successfully")
