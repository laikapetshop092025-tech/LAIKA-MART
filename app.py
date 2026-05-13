import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import calendar

API_URL = "https://script.google.com/macros/s/AKfycbyYnn80eP0QrXZctqTH1H3U42s4QhJZuGelZWW79VW5wAYcha60djsi8T7zMsbCsrqR/exec"

st.set_page_config(
    page_title="LAIKA ERP",
    layout="wide"
)

# ---------- CUSTOM CSS ----------

st.markdown("""

<style>

.main{
    background:#eef4ff;
}

[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#1e3a8a,#4f46e5);
}

[data-testid="stSidebar"] *{
    color:white;
}

.stButton>button{
    width:100%;
    border:none;
    border-radius:12px;
    padding:12px;
    font-size:16px;
    font-weight:bold;
    background:linear-gradient(90deg,#2563eb,#7c3aed);
    color:white;
}

.metric-card{
    background:white;
    padding:20px;
    border-radius:20px;
    box-shadow:0 4px 10px rgba(0,0,0,0.1);
    text-align:center;
}

</style>

""", unsafe_allow_html=True)

# ---------- LOGIN ----------

if "login" not in st.session_state:
    st.session_state.login = False

if st.session_state.login == False:

    st.title("🔐 LAIKA ERP LOGIN")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username == "admin" and password == "admin123":

            st.session_state.login = True
            st.success("Login Success")
            st.rerun()

        else:

            st.error("Wrong Username or Password")

# ---------- ERP ----------

else:

    st.sidebar.title("🐶 LAIKA ERP")

    page = st.sidebar.radio(
        "Menu",
        [
            "Dashboard",
            "Purchase",
            "Sales",
            "Stock",
            "Expense",
            "Ledger"
        ]
    )

    # DATE

    today = datetime.now()

    today_date = today.strftime("%d-%m-%Y")

    today_day = calendar.day_name[today.weekday()]

    # SERIAL NUMBER

    if "purchase_serial" not in st.session_state:
        st.session_state.purchase_serial = 1

    if "sales_serial" not in st.session_state:
        st.session_state.sales_serial = 1

    # ---------- DASHBOARD ----------

    if page == "Dashboard":

        st.title("📊 LAIKA ERP DASHBOARD")

        st.subheader(
            f"📅 {today_date} | {today_day}"
        )

        c1,c2,c3,c4 = st.columns(4)

        with c1:
            st.metric("Today's Sales", "₹ 0")

        with c2:
            st.metric("Today's Purchase", "₹ 0")

        with c3:
            st.metric("Today's Profit", "₹ 0")

        with c4:
            st.metric("Today's Expenses", "₹ 0")

        st.divider()

        m1,m2,m3 = st.columns(3)

        with m1:
            st.metric("Cash Collection", "₹ 0")

        with m2:
            st.metric("Online Collection", "₹ 0")

        with m3:
            st.metric("Udhari Pending", "₹ 0")

        st.divider()

        st.success("✅ Google Sheet Connected")

    # ---------- PURCHASE ----------

    elif page == "Purchase":

        st.title("🛒 Purchase Entry")

        col1,col2 = st.columns(2)

        with col1:

            bill_no = st.text_input(
                "Purchase Bill No",
                value=str(
                    st.session_state.purchase_serial
                )
            )

            date = st.date_input("Date")

            party = st.text_input(
                "Supplier Name"
            )

            product = st.text_input(
                "Product Name"
            )

            category = st.selectbox(
                "Category",
                [
                    "Dog Food",
                    "Cat Food",
                    "Bird Food",
                    "Medicine",
                    "Accessories"
                ]
            )

            unit = st.selectbox(
                "Unit",
                [
                    "PCS",
                    "KG",
                    "DOZEN",
                    "BAG"
                ]
            )

            qty = st.number_input(
                "Quantity",
                min_value=0.0
            )

        with col2:

            rate = st.number_input(
                "Purchase Rate",
                min_value=0.0
            )

            total = qty * rate

            st.info(
                f"Total Purchase: ₹ {total}"
            )

            payment = st.selectbox(
                "Payment Type",
                [
                    "Cash",
                    "Online",
                    "Udhari"
                ]
            )

            paid = st.number_input(
                "Paid Amount",
                min_value=0.0
            )

            balance = total - paid

            st.warning(
                f"Balance: ₹ {balance}"
            )

        if st.button("Save Purchase"):

            data = {

                "type":"purchase",

                "bill_no":bill_no,
                "date":str(date),
                "party":party,
                "product":product,
                "category":category,
                "unit":unit,
                "qty":qty,
                "rate":rate,
                "total":total,
                "payment":payment,
                "paid":paid,
                "balance":balance

            }

            response = requests.post(
                API_URL,
                json=data
            )

            st.success(response.text)

            st.session_state.purchase_serial += 1

    # ---------- SALES ----------

    elif page == "Sales":

        st.title("💰 Sales Entry")

        col1,col2 = st.columns(2)

        with col1:

            bill_no = st.text_input(
                "Sales Bill No",
                value=str(
                    st.session_state.sales_serial
                )
            )

            date = st.date_input(
                "Sales Date"
            )

            customer = st.text_input(
                "Customer Name"
            )

            product = st.text_input(
                "Product Name"
            )

            category = st.selectbox(
                "Product Category",
                [
                    "Dog Food",
                    "Cat Food",
                    "Bird Food",
                    "Medicine",
                    "Accessories"
                ]
            )

            unit = st.selectbox(
                "Sales Unit",
                [
                    "PCS",
                    "KG",
                    "DOZEN",
                    "BAG"
                ]
            )

            qty = st.number_input(
                "Sales Quantity",
                min_value=0.0
            )

        with col2:

            rate = st.number_input(
                "Sales Rate",
                min_value=0.0
            )

            total = qty * rate

            st.info(
                f"Sales Amount: ₹ {total}"
            )

            payment = st.selectbox(
                "Payment Mode",
                [
                    "Cash",
                    "Online",
                    "Udhari"
                ]
            )

            paid = st.number_input(
                "Received Amount",
                min_value=0.0
            )

            balance = total - paid

            st.warning(
                f"Pending Amount: ₹ {balance}"
            )

        if st.button("Save Sales"):

            data = {

                "type":"sales",

                "bill_no":bill_no,
                "date":str(date),
                "customer":customer,
                "product":product,
                "category":category,
                "unit":unit,
                "qty":qty,
                "rate":rate,
                "total":total,
                "payment":payment,
                "paid":paid,
                "balance":balance

            }

            response = requests.post(
                API_URL,
                json=data
            )

            st.success(response.text)

            st.session_state.sales_serial += 1

    # ---------- STOCK ----------

    elif page == "Stock":

        st.title("📦 Stock Management")

        stock_data = {

            "Product":[
                "Pedigree",
                "Whiskas",
                "Bird Seeds"
            ],

            "Category":[
                "Dog Food",
                "Cat Food",
                "Bird Food"
            ],

            "Stock":[
                25,
                12,
                30
            ]

        }

        df = pd.DataFrame(stock_data)

        st.dataframe(
            df,
            use_container_width=True
        )

        st.warning(
            "⚠️ Low Stock Alert will appear here"
        )

    # ---------- EXPENSE ----------

    elif page == "Expense":

        st.title("💸 Expense Entry")

        expense_id = st.text_input(
            "Expense ID"
        )

        expense_date = st.date_input(
            "Expense Date"
        )

        expense_name = st.text_input(
            "Expense Name"
        )

        amount = st.number_input(
            "Amount",
            min_value=0.0
        )

        payment_mode = st.selectbox(
            "Payment Mode",
            [
                "Cash",
                "Online"
            ]
        )

        if st.button("Save Expense"):

            data = {

                "type":"expense",

                "id":expense_id,
                "date":str(expense_date),
                "expense_name":expense_name,
                "amount":amount,
                "payment_mode":payment_mode

            }

            response = requests.post(
                API_URL,
                json=data
            )

            st.success(response.text)

    # ---------- LEDGER ----------

    elif page == "Ledger":

        st.title("📒 Ledger")

        ledger_data = {

            "Name":[
                "Ramesh",
                "Suresh"
            ],

            "Type":[
                "Sales",
                "Purchase"
            ],

            "Balance":[
                1200,
                800
            ]

        }

        df = pd.DataFrame(ledger_data)

        st.dataframe(
            df,
            use_container_width=True
        )
