import streamlit as st
import pandas as pd
import requests

API_URL = "https://script.google.com/macros/s/AKfycbyYnn80eP0QrXZctqTH1H3U42s4QhJZuGelZWW79VW5wAYcha60djsi8T7zMsbCsrqR/exec"

st.set_page_config(
    page_title="Laika ERP",
    layout="wide"
)

# CUSTOM CSS

st.markdown("""

<style>

.main {
    background-color:#eef4ff;
}

.stButton>button {
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

# DASHBOARD

if page == "Dashboard":

    st.title("📊 Dashboard")

    col1,col2,col3 = st.columns(3)

    col1.metric(
        "ERP Status",
        "Running"
    )

    col2.metric(
        "Database",
        "Connected"
    )

    col3.metric(
        "Version",
        "1.0"
    )

    st.success(
        "Google Sheet Connected Successfully"
    )

# PURCHASE

elif page == "Purchase":

    st.title("🛒 Purchase Entry")

    col1,col2 = st.columns(2)

    with col1:

        bill_no = st.text_input(
            "Bill Number"
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

# SALES

elif page == "Sales":

    st.title("💰 Sales Entry")

    col1,col2 = st.columns(2)

    with col1:

        bill_no = st.text_input(
            "Sales Bill Number"
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
