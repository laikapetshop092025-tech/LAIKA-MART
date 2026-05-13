# Replace Entire `app.py` With This Final Fixed Code

```python
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="LAIKA ERP", layout="wide")

# =========================
# DEFAULT DATA
# =========================

if "sales" not in st.session_state:
    st.session_state.sales = []

if "purchase" not in st.session_state:
    st.session_state.purchase = []

if "expense" not in st.session_state:
    st.session_state.expense = []

if "customers" not in st.session_state:
    st.session_state.customers = []

if "suppliers" not in st.session_state:
    st.session_state.suppliers = []

if "stock" not in st.session_state:
    st.session_state.stock = {}

if "sales_no" not in st.session_state:
    st.session_state.sales_no = 1

if "purchase_no" not in st.session_state:
    st.session_state.purchase_no = 1

# =========================
# CSS
# =========================

st.markdown("""
<style>
.main {
    background: #f8f5ff;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#8b5cf6,#ec4899);
}

[data-testid="stSidebar"] * {
    color: white;
}

.stButton>button {
    width: 100%;
    border-radius: 12px;
    border: none;
    background: linear-gradient(90deg,#8b5cf6,#ec4899);
    color: white;
    font-weight: bold;
    height: 45px;
}

.card {
    background: white;
    padding: 18px;
    border-radius: 18px;
    text-align: center;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================

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
        "Supplier Ledger"
    ]
)

# =========================
# DASHBOARD CALCULATION
# =========================

sales_total = sum(x.get("Total",0) for x in st.session_state.sales)
purchase_total = sum(x.get("Total",0) for x in st.session_state.purchase)
expense_total = sum(x.get("Amount",0) for x in st.session_state.expense)

cash_total = 0
online_total = 0

for x in st.session_state.sales:
    payment = x.get("Payment","")

    if payment == "Cash":
        cash_total += x.get("Paid",0)

    elif payment == "Online":
        online_total += x.get("Paid",0)

profit_total = sales_total - purchase_total - expense_total

# =========================
# DASHBOARD
# =========================

if page == "Dashboard":

    st.title("📊 Dashboard")

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class='card'>
        <h3>Today's Sales</h3>
        <h2>₹ {sales_total}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class='card'>
        <h3>Today's Purchase</h3>
        <h2>₹ {purchase_total}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class='card'>
        <h3>Cash Receive</h3>
        <h2>₹ {cash_total}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class='card'>
        <h3>Online Receive</h3>
        <h2>₹ {online_total}</h2>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    col5,col6 = st.columns(2)

    with col5:
        st.markdown(f"""
        <div class='card'>
        <h3>Total Receive</h3>
        <h2>₹ {cash_total + online_total}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col6:
        st.markdown(f"""
        <div class='card'>
        <h3>Total Profit</h3>
        <h2>₹ {profit_total}</h2>
        </div>
        """, unsafe_allow_html=True)

# =========================
# PURCHASE
# =========================

elif page == "Purchase":

    st.title("🛒 Purchase Entry")

    col1,col2 = st.columns(2)

    with col1:

        bill_no = st.text_input(
            "Purchase Bill No",
            value=str(st.session_state.purchase_no)
        )

        supplier = st.text_input("Supplier Name")

        product = st.text_input("Product Name")

        unit = st.selectbox(
            "Unit",
            ["KG","PCS","DOZEN","BAG"]
        )

        qty = st.number_input("Quantity", min_value=0.0)

    with col2:

        rate = st.number_input("Rate", min_value=0.0)

        total = qty * rate

        st.info(f"Total = ₹ {total}")

        payment = st.selectbox(
            "Payment",
            ["Cash","Online","Udhari"]
        )

        paid = st.number_input("Paid Amount", min_value=0.0)

        balance = total - paid

        st.warning(f"Balance = ₹ {balance}")

    if st.button("Save Purchase"):

        data = {
            "Bill": bill_no,
            "Supplier": supplier,
            "Product": product,
            "Unit": unit,
            "Qty": qty,
            "Rate": rate,
            "Total": total,
            "Payment": payment,
            "Paid": paid,
            "Balance": balance
        }

        st.session_state.purchase.append(data)

        # STOCK ADD
        current_stock = st.session_state.stock.get(product,0)
        st.session_state.stock[product] = current_stock + qty

        # SUPPLIER
        found = False

        for s in st.session_state.suppliers:
            if s["Name"] == supplier:
                s["Pending"] += balance
                found = True

        if not found:
            st.session_state.suppliers.append({
                "Name": supplier,
                "Pending": balance
            })

        st.session_state.purchase_no += 1

        st.success("Purchase Saved")

    st.divider()

    st.subheader("Delete Purchase Entry")

    if len(st.session_state.purchase) > 0:

        df = pd.DataFrame(st.session_state.purchase)
        st.dataframe(df, use_container_width=True)

        delete_index = st.number_input(
            "Enter Row Number To Delete",
            min_value=0,
            max_value=len(st.session_state.purchase)-1,
            step=1
        )

        if st.button("Delete Purchase"):
            st.session_state.purchase.pop(delete_index)
            st.success("Deleted Successfully")

# =========================
# SALES
# =========================

elif page == "Sales":

    st.title("💰 Sales Entry")

    col1,col2 = st.columns(2)

    with col1:

        bill_no = st.text_input(
            "Sales Bill No",
            value=str(st.session_state.sales_no)
        )

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

    with col2:

        rate = st.number_input(
            "Sales Rate",
            min_value=0.0
        )

        total = qty * rate

        reward_points = int(total / 100) * 50

        st.info(f"Total = ₹ {total}")

        st.success(f"Reward Points = {reward_points}")

        payment = st.selectbox(
            "Sales Payment",
            ["Cash","Online","Udhari"]
        )

        paid = st.number_input(
            "Paid Amount",
            min_value=0.0
        )

        balance = total - paid

        st.warning(f"Balance = ₹ {balance}")

    if st.button("Save Sales"):

        current_stock = st.session_state.stock.get(product,0)

        if qty > current_stock:
            st.error("Not Enough Stock")

        else:

            st.session_state.stock[product] = current_stock - qty

            data = {
                "Bill": bill_no,
                "Customer": customer,
                "Product": product,
                "Unit": unit,
                "Qty": qty,
                "Rate": rate,
                "Total": total,
                "Payment": payment,
                "Paid": paid,
                "Balance": balance,
                "Points": reward_points
            }

            st.session_state.sales.append(data)

            found = False

            for c in st.session_state.customers:

                if c["Name"] == customer:
                    c["Pending"] += balance
                    c["Points"] += reward_points
                    found = True

            if not found:
                st.session_state.customers.append({
                    "Name": customer,
                    "Pending": balance,
                    "Points": reward_points
                })

            st.session_state.sales_no += 1

            st.success("Sales Saved")

    st.divider()

    st.subheader("Delete Sales Entry")

    if len(st.session_state.sales) > 0:

        df = pd.DataFrame(st.session_state.sales)
        st.dataframe(df, use_container_width=True)

        delete_index = st.number_input(
            "Delete Sales Row",
            min_value=0,
            max_value=len(st.session_state.sales)-1,
            step=1
        )

        if st.button("Delete Sales"):
            st.session_state.sales.pop(delete_index)
            st.success("Sales Deleted")

# =========================
# EXPENSE
# =========================

elif page == "Expense":

    st.title("💸 Expense Entry")

    expense_name = st.text_input("Expense Name")

    amount = st.number_input("Amount", min_value=0.0)

    payment = st.selectbox(
        "Payment Mode",
        ["Cash","Online"]
    )

    if st.button("Save Expense"):

        st.session_state.expense.append({
            "Expense": expense_name,
            "Amount": amount,
            "Payment": payment
        })

        st.success("Expense Saved")

    if len(st.session_state.expense) > 0:
        st.dataframe(pd.DataFrame(st.session_state.expense))

# =========================
# STOCK
# =========================

elif page == "Stock":

    st.title("📦 Stock")

    stock_data = []

    for product,qty in st.session_state.stock.items():
        stock_data.append({
            "Product": product,
            "Stock": qty
        })

    if len(stock_data) > 0:

        stock_df = pd.DataFrame(stock_data)

        st.dataframe(stock_df, use_container_width=True)

# =========================
# CUSTOMER LEDGER
# =========================

elif page == "Customer Ledger":

    st.title("👤 Customer Ledger")

    if len(st.session_state.customers) > 0:

        customer_df = pd.DataFrame(st.session_state.customers)

        st.dataframe(customer_df, use_container_width=True)

        customer_name = st.selectbox(
            "Select Customer",
            customer_df["Name"]
        )

        receive_cash = st.number_input(
            "Cash Receive",
            min_value=0.0
        )

        receive_online = st.number_input(
            "Online Receive",
            min_value=0.0
        )

        total_receive = receive_cash + receive_online

        if st.button("Receive Payment"):

            for c in st.session_state.customers:

                if c["Name"] == customer_name:
                    c["Pending"] -= total_receive

            st.success("Payment Updated")

# =========================
# SUPPLIER LEDGER
# =========================

elif page == "Supplier Ledger":

    st.title("🏪 Supplier Ledger")

    if len(st.session_state.suppliers) > 0:

        supplier_df = pd.DataFrame(st.session_state.suppliers)

        st.dataframe(supplier_df, use_container_width=True)

        supplier_name = st.selectbox(
            "Select Supplier",
            supplier_df["Name"]
        )

        pay_cash = st.number_input(
            "Cash Payment",
            min_value=0.0
        )

        pay_online = st.number_input(
            "Online Payment",
            min_value=0.0
        )

        total_pay = pay_cash + pay_online

        if st.button("Pay Supplier"):

            for s in st.session_state.suppliers:

                if s["Name"] == supplier_name:
                    s["Pending"] -= total_pay

            st.success("Supplier Payment Updated")

```

## Final Steps

1. Open your GitHub repository.
2. Open `app.py`
3. Delete old code.
4. Paste this full code.
5. Click `Commit Changes`
6. Open Streamlit.
7. Click `Reboot App`
8. Done ✅
