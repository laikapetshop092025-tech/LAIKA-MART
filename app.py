import streamlit as st
import pandas as pd
from datetime import datetime
import calendar

# ================= PAGE =================

st.set_page_config(
    page_title="LAIKA ERP",
    layout="wide"
)

# ================= CSS =================

st.markdown("""

<style>

.main{
    background:linear-gradient(135deg,#fdf2f8,#ede9fe);
}

[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#7c3aed,#ec4899);
}

[data-testid="stSidebar"] *{
    color:white;
}

.stButton>button{
    width:100%;
    border:none;
    border-radius:12px;
    background:linear-gradient(90deg,#8b5cf6,#ec4899);
    color:white;
    font-weight:bold;
    padding:12px;
    transition:0.3s;
}

.stButton>button:hover{
    transform:scale(1.03);
    background:linear-gradient(90deg,#ec4899,#8b5cf6);
}

.metric-card{
    background:white;
    padding:20px;
    border-radius:18px;
    box-shadow:0 4px 15px rgba(0,0,0,0.1);
    text-align:center;
    margin-bottom:15px;
}

</style>

""", unsafe_allow_html=True)

# ================= LOGIN =================

if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:

    st.title("🔐 LAIKA ERP LOGIN")

    username = st.text_input("User ID")
    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if (
            username == "admin"
            and
            password == "1234"
        ):

            st.session_state.login = True
            st.rerun()

        else:

            st.error("Wrong ID Password")

    st.stop()

# ================= SESSION =================

if "purchase_data" not in st.session_state:
    st.session_state.purchase_data = []

if "sales_data" not in st.session_state:
    st.session_state.sales_data = []

if "expense_data" not in st.session_state:
    st.session_state.expense_data = []

if "stock_data" not in st.session_state:
    st.session_state.stock_data = []

if "pet_data" not in st.session_state:
    st.session_state.pet_data = []

if "purchase_no" not in st.session_state:
    st.session_state.purchase_no = 1

if "sales_no" not in st.session_state:
    st.session_state.sales_no = 1

# ================= SIDEBAR =================

st.sidebar.title("🐶 LAIKA ERP")

page = st.sidebar.radio(

    "MENU",

    [

        "📊 Dashboard",
        "🛒 Purchase",
        "💰 Sales",
        "📦 Stock",
        "📒 Customer Ledger",
        "🚚 Supplier Ledger",
        "💸 Expense",
        "🐶 Pet Register"

    ]

)

# ================= DATE =================

today = datetime.now()

today_date = today.strftime("%d-%m-%Y")

today_day = calendar.day_name[
    today.weekday()
]

# ================= CALCULATION =================

today_sales = 0
today_purchase = 0
today_profit = 0

cash_total = 0
online_total = 0

# PURCHASE

for p in st.session_state.purchase_data:

    today_purchase += p["Total"]

# SALES

for s in st.session_state.sales_data:

    today_sales += s["Total"]

    profit = (
        s["Total"]
        - (s["Qty"] * s["Purchase Price"])
    )

    today_profit += profit

    payment_type = s.get(
        "Payment",
        ""
    )

    if payment_type == "Cash":

        cash_total += s["Paid"]

    elif payment_type == "Online":

        online_total += s["Paid"]

    elif payment_type == "Mixed":

        cash_total += s.get(
            "Cash Amount",
            0
        )

        online_total += s.get(
            "Online Amount",
            0
        )

# ================= DASHBOARD =================

if page == "📊 Dashboard":

    st.title("📊 DASHBOARD")

    st.subheader(
        f"📅 {today_date} | {today_day}"
    )

    c1,c2,c3 = st.columns(3)

    with c1:

        st.markdown(f"""

        <div class="metric-card">

        <h3>💰 Today Sales</h3>
        <h2>₹ {today_sales}</h2>

        </div>

        """, unsafe_allow_html=True)

        st.markdown(f"""

        <div class="metric-card">

        <h3>💵 Cash</h3>
        <h2>₹ {cash_total}</h2>

        </div>

        """, unsafe_allow_html=True)

    with c2:

        st.markdown(f"""

        <div class="metric-card">

        <h3>🛒 Purchase</h3>
        <h2>₹ {today_purchase}</h2>

        </div>

        """, unsafe_allow_html=True)

        st.markdown(f"""

        <div class="metric-card">

        <h3>📲 Online</h3>
        <h2>₹ {online_total}</h2>

        </div>

        """, unsafe_allow_html=True)

    with c3:

        st.markdown(f"""

        <div class="metric-card">

        <h3>📈 Profit</h3>
        <h2>₹ {today_profit}</h2>

        </div>

        """, unsafe_allow_html=True)

        st.markdown(f"""

        <div class="metric-card">

        <h3>💳 Total Receive</h3>
        <h2>₹ {cash_total + online_total}</h2>

        </div>

        """, unsafe_allow_html=True)

# ================= PURCHASE =================

elif page == "🛒 Purchase":

    st.title("🛒 PURCHASE")

    c1,c2 = st.columns(2)

    with c1:

        bill = st.text_input(
            "Purchase Bill",
            value=str(
                st.session_state.purchase_no
            )
        )

        party = st.text_input(
            "Supplier Name"
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

    with c2:

        rate = st.number_input(
            "Purchase Rate",
            min_value=0.0
        )

        total = qty * rate

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

        st.info(
            f"Total ₹ {total}"
        )

        st.warning(
            f"Balance ₹ {balance}"
        )

    if st.button("SAVE PURCHASE"):

        data = {

            "Bill":bill,
            "Party":party,
            "Product":product,
            "Unit":unit,
            "Qty":qty,
            "Rate":rate,
            "Total":total,
            "Payment":payment,
            "Paid":paid,
            "Balance":balance

        }

        st.session_state.purchase_data.append(
            data
        )

        # STOCK UPDATE

        found = False

        for item in st.session_state.stock_data:

            if item["Product"] == product:

                item["Qty"] += qty
                found = True

        if not found:

            st.session_state.stock_data.append({

                "Product":product,
                "Qty":qty,
                "Unit":unit,
                "Rate":rate

            })

        st.session_state.purchase_no += 1

        st.success("Purchase Saved")

    st.divider()

    if len(st.session_state.purchase_data)>0:

        st.dataframe(
            pd.DataFrame(
                st.session_state.purchase_data
            ),
            use_container_width=True
        )

        delete_index = st.selectbox(

            "Delete Purchase Entry",

            range(
                len(
                    st.session_state.purchase_data
                )
            )

        )

        if st.button("DELETE PURCHASE"):

            st.session_state.purchase_data.pop(
                delete_index
            )

            st.success("Deleted")

            st.rerun()

# ================= SALES =================

elif page == "💰 Sales":

    st.title("💰 SALES")

    c1,c2 = st.columns(2)

    with c1:

        bill = st.text_input(

            "Sales Bill",

            value=str(
                st.session_state.sales_no
            )

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
            "Sales Qty",
            min_value=0.0
        )

    with c2:

        sale_rate = st.number_input(
            "Sales Rate",
            min_value=0.0
        )

        total = qty * sale_rate

        payment = st.selectbox(

            "Payment",

            [
                "Cash",
                "Online",
                "Udhari",
                "Mixed"
            ]

        )

        cash_amount = st.number_input(
            "Cash Amount",
            min_value=0.0
        )

        online_amount = st.number_input(
            "Online Amount",
            min_value=0.0
        )

        paid = (
            cash_amount
            + online_amount
        )

        balance = total - paid

        st.info(
            f"Total ₹ {total}"
        )

        st.warning(
            f"Balance ₹ {balance}"
        )

    purchase_price = 0

    for item in st.session_state.stock_data:

        if item["Product"] == product:

            purchase_price = item["Rate"]

            item["Qty"] -= qty

    points = int(total / 100) * 50

    discount = points * 2

    if st.button("SAVE SALES"):

        data = {

            "Bill":bill,
            "Customer":customer,
            "Product":product,
            "Unit":unit,
            "Qty":qty,
            "Rate":sale_rate,
            "Total":total,
            "Payment":payment,
            "Paid":paid,
            "Balance":balance,
            "Points":points,
            "Discount":discount,
            "Purchase Price":purchase_price,
            "Cash Amount":cash_amount,
            "Online Amount":online_amount

        }

        st.session_state.sales_data.append(
            data
        )

        st.session_state.sales_no += 1

        st.success(
            f"Sales Saved | {points} Points Added"
        )

    st.divider()

    if len(st.session_state.sales_data)>0:

        st.dataframe(

            pd.DataFrame(
                st.session_state.sales_data
            ),

            use_container_width=True

        )

        delete_sale = st.selectbox(

            "Delete Sales Entry",

            range(
                len(
                    st.session_state.sales_data
                )
            )

        )

        if st.button("DELETE SALES"):

            st.session_state.sales_data.pop(
                delete_sale
            )

            st.success("Deleted")

            st.rerun()

# ================= STOCK =================

elif page == "📦 Stock":

    st.title("📦 STOCK")

    if len(
        st.session_state.stock_data
    ) == 0:

        st.warning("No Stock")

    else:

        stock_df = pd.DataFrame(
            st.session_state.stock_data
        )

        st.dataframe(
            stock_df,
            use_container_width=True
        )

# ================= CUSTOMER LEDGER =================

elif page == "📒 Customer Ledger":

    st.title("📒 CUSTOMER LEDGER")

    if len(
        st.session_state.sales_data
    ) == 0:

        st.warning("No Customer Data")

    else:

        sales_df = pd.DataFrame(
            st.session_state.sales_data
        )

        st.dataframe(
            sales_df,
            use_container_width=True
        )

        st.divider()

        st.subheader(
            "💵 Receive Payment"
        )

        selected = st.selectbox(

            "Select Customer",

            range(
                len(
                    st.session_state.sales_data
                )
            ),

            format_func=lambda x:

            f"""

            {st.session_state.sales_data[x]['Customer']}
            | Pending:
            ₹ {st.session_state.sales_data[x]['Balance']}

            """

        )

        customer_data = (
            st.session_state.sales_data[
                selected
            ]
        )

        c1,c2 = st.columns(2)

        with c1:

            receive_cash = st.number_input(
                "Receive Cash",
                min_value=0.0
            )

        with c2:

            receive_online = st.number_input(
                "Receive Online",
                min_value=0.0
            )

        receive_total = (
            receive_cash
            + receive_online
        )

        if st.button("RECEIVE PAYMENT"):

            customer_data["Paid"] += receive_total

            customer_data["Balance"] -= receive_total

            if customer_data["Balance"] < 0:

                customer_data["Balance"] = 0

            customer_data[
                "Cash Amount"
            ] += receive_cash

            customer_data[
                "Online Amount"
            ] += receive_online

            st.success("Payment Received")

            st.rerun()

# ================= SUPPLIER LEDGER =================

elif page == "🚚 Supplier Ledger":

    st.title("🚚 SUPPLIER LEDGER")

    if len(
        st.session_state.purchase_data
    ) == 0:

        st.warning("No Supplier Data")

    else:

        purchase_df = pd.DataFrame(
            st.session_state.purchase_data
        )

        st.dataframe(
            purchase_df,
            use_container_width=True
        )

# ================= EXPENSE =================

elif page == "💸 Expense":

    st.title("💸 EXPENSE")

    name = st.text_input(
        "Expense Name"
    )

    amount = st.number_input(
        "Expense Amount",
        min_value=0.0
    )

    payment = st.selectbox(

        "Expense Payment",

        [
            "Cash",
            "Online"
        ]

    )

    if st.button("SAVE EXPENSE"):

        st.session_state.expense_data.append({

            "Name":name,
            "Amount":amount,
            "Payment":payment

        })

        st.success("Expense Saved")

    if len(
        st.session_state.expense_data
    ) > 0:

        st.dataframe(

            pd.DataFrame(
                st.session_state.expense_data
            ),

            use_container_width=True

        )

# ================= PET REGISTER =================

elif page == "🐶 Pet Register":

    st.title("🐶 PET REGISTER")

    pet_name = st.text_input(
        "Pet Name"
    )

    owner = st.text_input(
        "Owner Name"
    )

    pet_type = st.selectbox(

        "Pet Type",

        [
            "Dog",
            "Cat",
            "Bird",
            "Fish"
        ]

    )

    mobile = st.text_input(
        "Mobile Number"
    )

    if st.button("SAVE PET"):

        st.session_state.pet_data.append({

            "Pet":pet_name,
            "Owner":owner,
            "Type":pet_type,
            "Mobile":mobile

        })

        st.success("Pet Saved")

    if len(
        st.session_state.pet_data
    ) > 0:

        st.dataframe(

            pd.DataFrame(
                st.session_state.pet_data
            ),

            use_container_width=True

        )

# ================= LOGOUT =================

st.sidebar.divider()

if st.sidebar.button("🚪 Logout"):

    st.session_state.login = False

    st.rerun()
