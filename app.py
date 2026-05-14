import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# =========================================
# GOOGLE SHEET API
# =========================================

API_URL = "PASTE_YOUR_GOOGLE_SCRIPT_WEBAPP_URL_HERE"

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
    background:#f7f3ff;
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
    transition:0.3s;
}

.stButton>button:hover{
    transform:scale(1.02);
}

.card{
    background:linear-gradient(135deg,#a78bfa,#f472b6);
    padding:20px;
    border-radius:18px;
    color:white;
    text-align:center;
    height:150px;
    box-shadow:0 4px 15px rgba(0,0,0,0.15);
}

.menu-title{
    font-size:18px;
    font-weight:bold;
}

</style>

""", unsafe_allow_html=True)

# =========================================
# FUNCTIONS
# =========================================

def get_data(sheet_name):

    try:

        response = requests.get(
            f"{API_URL}?sheet={sheet_name}"
        )

        data = response.json()

        return pd.DataFrame(data)

    except:

        return pd.DataFrame()

def save_data(sheet_name, data):

    payload = {
        "action":"save",
        "sheet":sheet_name,
        "data":data
    }

    requests.post(API_URL, json=payload)

def delete_data(sheet_name, row_id):

    payload = {
        "action":"delete",
        "sheet":sheet_name,
        "row_id":row_id
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

    col1,col2 = st.columns(2)

    with col1:

        if st.button("Login"):

            if username == "admin" and password == "admin123":

                st.session_state.login = True
                st.rerun()

            else:

                st.error("Wrong Username or Password")

    with col2:

        if st.button("Forgot Password"):

            st.info("Default Login")
            st.info("Username = admin")
            st.info("Password = admin123")

    st.stop()

# =========================================
# SIDEBAR
# =========================================

st.sidebar.markdown(
    "<h1>🐶 LAIKA ERP</h1>",
    unsafe_allow_html=True
)

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

st.sidebar.divider()

st.sidebar.success("Admin Login Active")

if st.sidebar.button("Logout"):

    st.session_state.login = False
    st.rerun()

# =========================================
# LOAD DATA
# =========================================

sales_df = get_data("Sales")
purchase_df = get_data("Purchase")
expense_df = get_data("Expense")
customer_df = get_data("Customer")
supplier_df = get_data("Supplier")
stock_df = get_data("Stock")

# =========================================
# SAFE VALUES
# =========================================

sales_total = 0
purchase_total = 0
expense_total = 0
cash_total = 0
online_total = 0

if not sales_df.empty:

    if "Total" in sales_df.columns:
        sales_total = sales_df["Total"].astype(float).sum()

    if "Payment" in sales_df.columns:

        for _,row in sales_df.iterrows():

            if row["Payment"] == "Cash":
                cash_total += float(row["Paid"])

            elif row["Payment"] == "Online":
                online_total += float(row["Paid"])

if not purchase_df.empty:

    if "Total" in purchase_df.columns:
        purchase_total = purchase_df["Total"].astype(float).sum()

if not expense_df.empty:

    if "Amount" in expense_df.columns:
        expense_total = expense_df["Amount"].astype(float).sum()

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

    d1,d2 = st.columns(2)

    with d1:

        st.markdown(f"""
        <div class="card">
        <h3>Total Receive</h3>
        <h1>₹ {cash_total + online_total}</h1>
        </div>
        """, unsafe_allow_html=True)

    with d2:

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

    st.title("🛒 Purchase Entry")

    col1,col2 = st.columns(2)

    with col1:

        bill = st.text_input(
            "Purchase Bill Number",
            value=str(len(purchase_df)+1)
        )

        supplier = st.text_input(
            "Supplier Name"
        )

        product = st.text_input(
            "Product Name"
        )

        unit = st.selectbox(
            "Unit",
            ["KG","PCS","DOZEN","BAG"]
        )

    with col2:

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

            "ID":str(datetime.now().timestamp()),
            "Bill":bill,
            "Supplier":supplier,
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
        st.rerun()

    st.divider()

    if not purchase_df.empty:

        st.dataframe(
            purchase_df,
            use_container_width=True
        )

        delete_id = st.text_input(
            "Delete Purchase ID"
        )

        if st.button("Delete Purchase"):

            delete_data(
                "Purchase",
                delete_id
            )

            st.success("Purchase Deleted")
            st.rerun()

# =========================================
# SALES
# =========================================

elif page == "Sales":

    st.title("💰 Sales Entry")

    col1,col2 = st.columns(2)

    with col1:

        bill = st.text_input(
            "Sales Bill Number",
            value=str(len(sales_df)+1)
        )

        customer = st.text_input(
            "Customer Name"
        )

        product = st.text_input(
            "Product Name"
        )

        unit = st.selectbox(
            "Sales Unit",
            ["KG","PCS","DOZEN","BAG"]
        )

    with col2:

        qty = st.number_input(
            "Sales Quantity",
            min_value=0.0
        )

        rate = st.number_input(
            "Sales Rate",
            min_value=0.0
        )

        total = qty * rate

        reward_points = int(total/100)*50

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

            "ID":str(datetime.now().timestamp()),
            "Bill":bill,
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
        st.rerun()

    st.divider()

    if not sales_df.empty:

        st.dataframe(
            sales_df,
            use_container_width=True
        )

        delete_id = st.text_input(
            "Delete Sales ID"
        )

        if st.button("Delete Sales"):

            delete_data(
                "Sales",
                delete_id
            )

            st.success("Sales Deleted")
            st.rerun()

# =========================================
# EXPENSE
# =========================================

elif page == "Expense":

    st.title("💸 Expense")

    expense_name = st.text_input(
        "Expense Name"
    )

    amount = st.number_input(
        "Amount",
        min_value=0.0
    )

    payment = st.selectbox(
        "Payment Mode",
        ["Cash","Online"]
    )

    if st.button("Save Expense"):

        data = {

            "ID":str(datetime.now().timestamp()),
            "Expense":expense_name,
            "Amount":amount,
            "Payment":payment

        }

        save_data("Expense", data)

        st.success("Expense Saved")
        st.rerun()

    if not expense_df.empty:

        st.dataframe(
            expense_df,
            use_container_width=True
        )

# =========================================
# STOCK
# =========================================

elif page == "Stock":

    st.title("📦 Stock")

    if not stock_df.empty:

        st.dataframe(
            stock_df,
            use_container_width=True
        )

# =========================================
# CUSTOMER LEDGER
# =========================================

elif page == "Customer Ledger":

    st.title("👤 Customer Ledger")

    if not customer_df.empty:

        st.dataframe(
            customer_df,
            use_container_width=True
        )

# =========================================
# SUPPLIER LEDGER
# =========================================

elif page == "Supplier Ledger":

    st.title("🏪 Supplier Ledger")

    if not supplier_df.empty:

        st.dataframe(
            supplier_df,
            use_container_width=True
        )

# =========================================
# SETTINGS
# =========================================

elif page == "Settings":

    st.title("⚙️ Settings")

    st.success("LAIKA ERP Running Successfully")

    st.info("Admin Mode Active")
