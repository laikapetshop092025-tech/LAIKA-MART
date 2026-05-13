import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import calendar

API_URL = "https://script.google.com/macros/s/AKfycbyYnn80eP0QrXZctqTH1H3U42s4QhJZuGelZWW79VW5wAYcha60djsi8T7zMsbCsrqR/exec"

st.set_page_config(
    page_title="Laika ERP",
    layout="wide"
)

# CSS

st.markdown("""

<style>

.main{
    background:#eef4ff;
}

.stButton>button{
    background:linear-gradient(90deg,#1f4ed8,#4f46e5);
    color:white;
    border:none;
    border-radius:10px;
    padding:10px 20px;
    font-weight:bold;
}

[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#1f4ed8,#4f46e5);
}

[data-testid="stSidebar"] *{
    color:white;
}

.metric-box{
    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:0 2px 10px rgba(0,0,0,0.1);
    text-align:center;
}

</style>

""", unsafe_allow_html=True)

# SIDEBAR

st.sidebar.title("🐶 LAIKA ERP")

page = st.sidebar.radio(
    "Menu",
    [
        "Dashboard",
        "Purchase",
        "Sales"
    ]
)

# DATE

today = datetime.now()

today_date = today.strftime("%d-%m-%Y")

today_day = calendar.day_name[today.weekday()]

# AUTO SERIAL

if "purchase_serial" not in st.session_state:
    st.session_state.purchase_serial = 1

if "sales_serial" not in st.session_state:
    st.session_state.sales_serial = 1

# DASHBOARD

if page == "Dashboard":

    st.title("📊 Dashboard")

    st.subheader(
        f"📅 {today_date} | {today_day}"
    )

    col1,col2,col3 = st.columns(3)

    with col1:

        st.metric(
            "Today's Sales",
            "₹ 0"
        )

        st.metric(
            "Today's Cash",
            "₹ 0"
        )

    with col2:

        st.metric(
            "Today's Purchase",
            "₹ 0"
        )

        st.metric(
            "Today's Online",
            "₹ 0"
        )

    with col3:

        st.metric(
            "Today's Profit",
            "₹ 0"
        )

        st.metric(
            "Cash + Online",
            "₹ 0"
        )

    st.divider()

    st.subheader("📈 Monthly Report")

    m1,m2,m3 = st.columns(3)

    with m1:

        st.metric(
            "Monthly Sales",
            "₹ 0"
        )

    with m2:

        st.metric(
            "Monthly Purchase",
            "₹ 0"
        )

    with m3:

        st.metric(
            "Monthly Profit",
            "₹ 0"
        )

# PURCHASE

elif page == "Purchase":

    st.title("🛒 Purchase Entry")

    col1,col2 = st.columns(2)

    with col1:

        bill_no = st.text_input(
            "Purchase Serial Number",
            value=str(
                st.session_state.purchase_serial
            )
        )

        date = st.date_input(
            "Date"
        )

        party = st.text_input(
            "Party Name"
        )

        product = st.text_input(
            "Product Name"
        )

        unit = st.selectbox(
            "Unit",
            [
                "KG",
                "PCS",
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
            "Rate",
            min_value=0.0
        )

        total = qty * rate

        st.info(
            f"Total Amount: ₹ {total}"
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

        st.success(
            response.text
        )

        st.session_state.purchase_serial += 1

# SALES

elif page == "Sales":

    st.title("💰 Sales Entry")

    col1,col2 = st.columns(2)

    with col1:

        bill_no = st.text_input(
            "Sales Serial Number",
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

        unit = st.selectbox(
            "Sales Unit",
            [
                "KG",
                "PCS",
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
            "Sales Payment Type",
            [
                "Cash",
                "Online",
                "Udhari"
            ]
        )

        paid = st.number_input(
            "Sales Paid Amount",
            min_value=0.0
        )

        balance = total - paid

        st.warning(
            f"Balance: ₹ {balance}"
        )

    if st.button("Save Sales"):

        data = {

            "type":"sales",

            "bill_no":bill_no,
            "date":str(date),
            "customer":customer,
            "product":product,
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

        st.success(
            response.text
        )

        st.session_state.sales_serial += 1
