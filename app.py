import streamlit as st
import pandas as pd
import requests

API_URL = "https://script.google.com/macros/s/AKfycbyYnn80eP0QrXZctqTH1H3U42s4QhJZuGelZWW79VW5wAYcha60djsi8T7zMsbCsrqR/exec"

st.set_page_config(
    page_title="Laika ERP",
    layout="wide"
)

# SIDEBAR

st.sidebar.title("🐶 Laika ERP")

page = st.sidebar.radio(
    "Menu",
    ["Dashboard", "Purchase"]
)

# DASHBOARD

if page == "Dashboard":

    st.title("📊 Dashboard")

    st.success(
        "Google Sheet Connected Successfully"
    )

# PURCHASE

elif page == "Purchase":

    st.title("🛒 Purchase Entry")

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
        ["KG", "PCS", "DOZEN", "BAG"]
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

    st.info(
        f"Total Amount: ₹ {total}"
    )

    payment = st.selectbox(
        "Payment Type",
        ["Cash", "Online", "Udhari"]
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
