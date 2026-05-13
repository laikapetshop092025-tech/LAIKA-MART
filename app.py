import streamlit as st
import pandas as pd
from datetime import datetime
import calendar

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="LAIKA ERP",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>

.main{
    background:linear-gradient(135deg,#fdf2f8,#ede9fe);
}

/* SIDEBAR */

section[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#7c3aed,#ec4899);
}

section[data-testid="stSidebar"] *{
    color:white !important;
}

/* BUTTONS */

.stButton>button{
    width:100%;
    border:none;
    border-radius:14px;
    background:linear-gradient(90deg,#8b5cf6,#ec4899);
    color:white;
    font-weight:bold;
    padding:12px;
    transition:0.3s;
}

.stButton>button:hover{
    transform:scale(1.03);
    background:linear-gradient(90deg,#7c3aed,#db2777);
}

/* CARDS */

.card{
    padding:20px;
    border-radius:20px;
    color:white;
    text-align:center;
    margin-bottom:10px;
    box-shadow:0 4px 12px rgba(0,0,0,0.15);
}

.purple{
    background:linear-gradient(135deg,#8b5cf6,#7c3aed);
}

.pink{
    background:linear-gradient(135deg,#ec4899,#db2777);
}

.blue{
    background:linear-gradient(135deg,#3b82f6,#2563eb);
}

.green{
    background:linear-gradient(135deg,#10b981,#059669);
}

.orange{
    background:linear-gradient(135deg,#f59e0b,#d97706);
}

.red{
    background:linear-gradient(135deg,#ef4444,#dc2626);
}

/* MENU */

div[role="radiogroup"] label{
    background:white;
    padding:10px;
    margin-bottom:8px;
    border-radius:12px;
    cursor:pointer;
    transition:0.3s;
}

div[role="radiogroup"] label:hover{
    background:#f3e8ff;
    transform:scale(1.02);
}

</style>
""", unsafe_allow_html=True)

# =========================
# LOGIN
# =========================

if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:

    st.title("🐶 LAIKA ERP LOGIN")

    username = st.text_input("User ID")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username == "admin" and password == "admin123":
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Wrong ID or Password")

    st.info("Demo Login → admin / admin123")

    st.stop()

# =========================
# SESSION STORAGE
# =========================

if "purchase_data" not in st.session_state:
    st.session_state.purchase_data = []

if "sales_data" not in st.session_state:
    st.session_state.sales_data = []

if "expense_data" not in st.session_state:
    st.session_state.expense_data = []

if "customer_data" not in st.session_state:
    st.session_state.customer_data = []

if "supplier_data" not in st.session_state:
    st.session_state.supplier_data = []

if "pet_data" not in st.session_state:
    st.session_state.pet_data = []

# =========================
# AUTO BILL NUMBER
# =========================

purchase_bill = len(st.session_state.purchase_data) + 1
sales_bill = len(st.session_state.sales_data) + 1

# =========================
# DATE
# =========================

today = datetime.now()

today_date = today.strftime("%d-%m-%Y")
today_day = calendar.day_name[today.weekday()]

# =========================
# DASHBOARD CALCULATIONS
# =========================

today_sales = sum(
    x.get("Total", 0)
    for x in st.session_state.sales_data
)

today_purchase = sum(
    x.get("Total", 0)
    for x in st.session_state.purchase_data
)

today_expense = sum(
    x.get("Amount", 0)
    for x in st.session_state.expense_data
)

cash_total = 0
online_total = 0

for x in st.session_state.sales_data:

    if x.get("Payment") == "Cash":
        cash_total += x.get("Paid", 0)

    elif x.get("Payment") == "Online":
        online_total += x.get("Paid", 0)

    elif x.get("Payment") == "Both":

        cash_total += x.get("Cash", 0)
        online_total += x.get("Online", 0)

total_received = cash_total + online_total

profit = today_sales - today_purchase - today_expense

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
        "Supplier Ledger",
        "Pet Register"
    ]
)

if st.sidebar.button("Logout"):
    st.session_state.login = False
    st.rerun()

# =========================
# DASHBOARD
# =========================

if page == "Dashboard":

    st.title("📊 Dashboard")

    st.subheader(f"📅 {today_date} | {today_day}")

    c1,c2,c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <div class="card purple">
        <h3>Today's Sales</h3>
        <h1>₹ {today_sales}</h1>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="card pink">
        <h3>Today's Purchase</h3>
        <h1>₹ {today_purchase}</h1>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="card blue">
        <h3>Profit</h3>
        <h1>₹ {profit}</h1>
        </div>
        """, unsafe_allow_html=True)

    c4,c5,c6 = st.columns(3)

    with c4:
        st.markdown(f"""
        <div class="card green">
        <h3>Cash Received</h3>
        <h1>₹ {cash_total}</h1>
        </div>
        """, unsafe_allow_html=True)

    with c5:
        st.markdown(f"""
        <div class="card orange">
        <h3>Online Received</h3>
        <h1>₹ {online_total}</h1>
        </div>
        """, unsafe_allow_html=True)

    with c6:
        st.markdown(f"""
        <div class="card red">
        <h3>Total Received</h3>
        <h1>₹ {total_received}</h1>
        </div>
        """, unsafe_allow_html=True)

# =========================
# PURCHASE
# =========================

elif page == "Purchase":

    st.title("🛒 Purchase Entry")

    col1,col2 = st.columns(2)

    with col1:

        bill = st.text_input(
            "Purchase Bill No",
            value=str(purchase_bill)
        )

        supplier = st.text_input("Supplier Name")

        product = st.text_input("Product Name")

        unit = st.selectbox(
            "Unit",
            ["KG","PCS","DOZEN","BAG"]
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

        st.info(f"Total ₹ {total}")

        payment = st.selectbox(
            "Payment",
            ["Cash","Online","Udhari"]
        )

        paid = st.number_input(
            "Paid Amount",
            min_value=0.0
        )

        balance = total - paid

        st.warning(f"Balance ₹ {balance}")

    if st.button("Save Purchase"):

        st.session_state.purchase_data.append({

            "Bill": bill,
            "Supplier": supplier,
            "Product": product,
            "Unit": unit,
            "Qty": qty,
            "Rate": rate,
            "Total": total,
            "Payment": payment,
            "Paid": paid,
            "Balance": balance

        })

        st.success("Purchase Saved")

    if st.session_state.purchase_data:

        st.subheader("Purchase History")

        df = pd.DataFrame(
            st.session_state.purchase_data
        )

        st.dataframe(df, use_container_width=True)

# =========================
# SALES
# =========================

elif page == "Sales":

    st.title("💰 Sales Entry")

    col1,col2 = st.columns(2)

    with col1:

        bill = st.text_input(
            "Sales Bill No",
            value=str(sales_bill)
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

        st.info(f"Sales ₹ {total}")

        payment = st.selectbox(
            "Sales Payment",
            ["Cash","Online","Both","Udhari"]
        )

        cash_amt = 0
        online_amt = 0
        paid = 0

        if payment == "Cash":

            paid = st.number_input(
                "Cash Paid",
                min_value=0.0
            )

        elif payment == "Online":

            paid = st.number_input(
                "Online Paid",
                min_value=0.0
            )

        elif payment == "Both":

            cash_amt = st.number_input(
                "Cash",
                min_value=0.0
            )

            online_amt = st.number_input(
                "Online",
                min_value=0.0
            )

            paid = cash_amt + online_amt

        elif payment == "Udhari":

            paid = st.number_input(
                "Received",
                min_value=0.0
            )

        balance = total - paid

        st.warning(f"Balance ₹ {balance}")

    reward_points = int(total / 2)

    st.success(f"Reward Points Earned → {reward_points}")

    if st.button("Save Sale"):

        st.session_state.sales_data.append({

            "Bill": bill,
            "Customer": customer,
            "Product": product,
            "Unit": unit,
            "Qty": qty,
            "Rate": rate,
            "Total": total,
            "Payment": payment,
            "Paid": paid,
            "Cash": cash_amt,
            "Online": online_amt,
            "Balance": balance,
            "Points": reward_points

        })

        found = False

        for c in st.session_state.customer_data:

            if c["Customer"] == customer:

                c["Pending"] += balance
                c["Points"] += reward_points
                found = True

        if not found:

            st.session_state.customer_data.append({

                "Customer": customer,
                "Pending": balance,
                "Points": reward_points

            })

        st.success("Sale Saved")

    if st.session_state.sales_data:

        st.subheader("Sales History")

        df = pd.DataFrame(
            st.session_state.sales_data
        )

        st.dataframe(df, use_container_width=True)

# =========================
# EXPENSE
# =========================

elif page == "Expense":

    st.title("💸 Expense Entry")

    name = st.text_input("Expense Name")

    amount = st.number_input(
        "Amount",
        min_value=0.0
    )

    mode = st.selectbox(
        "Mode",
        ["Cash","Online"]
    )

    if st.button("Save Expense"):

        st.session_state.expense_data.append({

            "Name": name,
            "Amount": amount,
            "Mode": mode

        })

        st.success("Expense Saved")

    if st.session_state.expense_data:

        df = pd.DataFrame(
            st.session_state.expense_data
        )

        st.dataframe(df, use_container_width=True)

# =========================
# STOCK
# =========================

elif page == "Stock":

    st.title("📦 Stock")

    stock = {}

    for p in st.session_state.purchase_data:

        name = p["Product"]

        stock[name] = stock.get(name, 0) + p["Qty"]

    for s in st.session_state.sales_data:

        name = s["Product"]

        stock[name] = stock.get(name, 0) - s["Qty"]

    stock_df = pd.DataFrame(
        list(stock.items()),
        columns=["Product","Current Stock"]
    )

    st.dataframe(
        stock_df,
        use_container_width=True
    )

# =========================
# CUSTOMER LEDGER
# =========================

elif page == "Customer Ledger":

    st.title("👤 Customer Ledger")

    if st.session_state.customer_data:

        for i,c in enumerate(
            st.session_state.customer_data
        ):

            st.markdown("---")

            st.subheader(c["Customer"])

            st.write(f"Pending ₹ {c['Pending']}")
            st.write(f"Reward Points → {c['Points']}")

            col1,col2 = st.columns(2)

            with col1:

                cash = st.number_input(
                    f"Cash {i}",
                    min_value=0.0,
                    key=f"cash{i}"
                )

            with col2:

                online = st.number_input(
                    f"Online {i}",
                    min_value=0.0,
                    key=f"online{i}"
                )

            total = cash + online

            if st.button(
                f"Receive Payment {i}"
            ):

                c["Pending"] -= total

                st.success(
                    "Payment Updated"
                )

# =========================
# SUPPLIER LEDGER
# =========================

elif page == "Supplier Ledger":

    st.title("🏪 Supplier Ledger")

    supplier_summary = {}

    for p in st.session_state.purchase_data:

        s = p["Supplier"]

        if s not in supplier_summary:

            supplier_summary[s] = 0

        supplier_summary[s] += p["Balance"]

    for i,(name,balance) in enumerate(
        supplier_summary.items()
    ):

        st.markdown("---")

        st.subheader(name)

        st.write(f"Pending ₹ {balance}")

        col1,col2 = st.columns(2)

        with col1:

            cash = st.number_input(
                f"Supplier Cash {i}",
                min_value=0.0,
                key=f"sc{i}"
            )

        with col2:

            online = st.number_input(
                f"Supplier Online {i}",
                min_value=0.0,
                key=f"so{i}"
            )

        total = cash + online

        if st.button(
            f"Pay Supplier {i}"
        ):

            supplier_summary[name] -= total

            st.success(
                "Supplier Payment Updated"
            )

# =========================
# PET REGISTER
# =========================

elif page == "Pet Register":

    st.title("🐶 Pet Register")

    owner = st.text_input("Owner Name")

    pet = st.text_input("Pet Name")

    pet_type = st.selectbox(
        "Pet Type",
        ["Dog","Cat","Bird","Fish"]
    )

    breed = st.text_input("Breed")

    mobile = st.text_input("Mobile")

    if st.button("Save Pet"):

        st.session_state.pet_data.append({

            "Owner": owner,
            "Pet": pet,
            "Type": pet_type,
            "Breed": breed,
            "Mobile": mobile

        })

        st.success("Pet Saved")

    if st.session_state.pet_data:

        df = pd.DataFrame(
            st.session_state.pet_data
        )

        st.dataframe(df, use_container_width=True)
