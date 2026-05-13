import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Laika ERP",
    layout="wide"
)

# SIDEBAR

st.sidebar.title("🐶 Laika ERP")

page = st.sidebar.radio(
    "Menu",
    ["Dashboard", "Purchase", "Stock"]
)

# DATA STORAGE

if "stock" not in st.session_state:
    st.session_state.stock = []

if "purchase" not in st.session_state:
    st.session_state.purchase = []

# DASHBOARD

if page == "Dashboard":

    st.title("📊 Dashboard")

    total_products = len(st.session_state.stock)

    col1, col2 = st.columns(2)

    col1.metric(
        "Total Products",
        total_products
    )

    col2.metric(
        "Total Purchase Entries",
        len(st.session_state.purchase)
    )

# PURCHASE

elif page == "Purchase":

    st.title("🛒 Purchase Entry")

    bill_no = st.text_input("Bill Number")

    date = st.date_input("Date")

    party = st.text_input("Party Name")

    product = st.text_input("Product Name")

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

    st.info(f"Total Amount: ₹ {total}")

    payment = st.selectbox(
        "Payment Type",
        ["Cash", "Online", "Udhari"]
    )

    paid = st.number_input(
        "Paid Amount",
        min_value=0.0
    )

    balance = total - paid

    st.warning(f"Balance: ₹ {balance}")

    if st.button("Save Purchase"):

        purchase_data = {

            "Bill No": bill_no,
            "Date": str(date),
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

        stock_data = {

            "Product": product,
            "Qty": qty,
            "Price": rate,
            "Unit": unit

        }

        st.session_state.purchase.append(
            purchase_data
        )

        st.session_state.stock.append(
            stock_data
        )

        st.success("Purchase Saved Successfully")

# STOCK

elif page == "Stock":

    st.title("📦 Stock")

    if len(st.session_state.stock) == 0:

        st.warning("No Stock Available")

    else:

        stock_df = pd.DataFrame(
            st.session_state.stock
        )

        st.dataframe(
            stock_df,
            use_container_width=True
        )
