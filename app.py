import streamlit as st
import pandas as pd
from datetime import datetime
import calendar
import plotly.express as px

# ---------------- PAGE ----------------

st.set_page_config(
    page_title="LAIKA ERP PRO",
    layout="wide"
)

# ---------------- SESSION ----------------

if "login" not in st.session_state:
    st.session_state.login = False

if "purchase_data" not in st.session_state:
    st.session_state.purchase_data = []

if "sales_data" not in st.session_state:
    st.session_state.sales_data = []

if "expense_data" not in st.session_state:
    st.session_state.expense_data = []

# ---------------- CSS ----------------

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

.card{
    padding:22px;
    border-radius:18px;
    color:white;
    text-align:center;
    height:145px;
    display:flex;
    flex-direction:column;
    justify-content:center;
    margin-bottom:15px;
}

.blue{
    background:linear-gradient(135deg,#2563eb,#1d4ed8);
}

.green{
    background:linear-gradient(135deg,#059669,#10b981);
}

.red{
    background:linear-gradient(135deg,#dc2626,#ef4444);
}

.purple{
    background:linear-gradient(135deg,#7c3aed,#9333ea);
}

.orange{
    background:linear-gradient(135deg,#ea580c,#f97316);
}

</style>

""", unsafe_allow_html=True)

# ---------------- LOGIN ----------------

if st.session_state.login == False:

    st.title("🔐 LAIKA ERP LOGIN")

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

            st.error(
                "Wrong Username or Password"
            )

    st.divider()

    st.subheader("Forgot Password")

    forgot_user = st.text_input(
        "Enter Username"
    )

    if st.button("Recover Password"):

        if forgot_user == "admin":

            st.info(
                "Password: admin123"
            )

        else:

            st.error(
                "Username Not Found"
            )

# ---------------- ERP ----------------

else:

    # ---------- PRODUCTS ----------

    products = [

        {
            "Product":"Pedigree",
            "Category":"Dog Food",
            "Unit":"PCS",
            "Purchase":900,
            "Sale":1100,
            "Stock":20
        },

        {
            "Product":"Whiskas",
            "Category":"Cat Food",
            "Unit":"PCS",
            "Purchase":450,
            "Sale":600,
            "Stock":15
        },

        {
            "Product":"Bird Seeds",
            "Category":"Bird Food",
            "Unit":"KG",
            "Purchase":80,
            "Sale":120,
            "Stock":30
        }

    ]

    product_df = pd.DataFrame(products)

    product_names = list(
        product_df["Product"]
    )

    # ---------- SIDEBAR ----------

    st.sidebar.title("🐶 LAIKA ERP")

    if st.sidebar.button("🚪 Logout"):

        st.session_state.login = False
        st.rerun()

    page = st.sidebar.radio(

        "MENU",

        [

            "📊 Dashboard",
            "🛒 Purchase",
            "💰 Sales",
            "💸 Expense",
            "📦 Stock",
            "📒 Customer Ledger",
            "🏪 Supplier Ledger",
            "📈 Analytics",
            "🧾 Daily Closing"

        ]
    )

    today = datetime.now()

    today_date = today.strftime(
        "%d-%m-%Y"
    )

    today_day = calendar.day_name[
        today.weekday()
    ]

    # ---------- CALCULATIONS ----------

    total_sales = 0

    for item in st.session_state.sales_data:
        total_sales += item["Total"]

    total_purchase = 0

    for item in st.session_state.purchase_data:
        total_purchase += item["Total"]

    total_expense = 0

    for item in st.session_state.expense_data:
        total_expense += item["Amount"]

    total_profit = (
        total_sales
        - total_purchase
        - total_expense
    )

    # ---------------- DASHBOARD ----------------

    if page == "📊 Dashboard":

        st.title(
            "📊 LAIKA ERP DASHBOARD"
        )

        st.subheader(
            f"📅 {today_date} | {today_day}"
        )

        c1,c2,c3,c4 = st.columns(4)

        with c1:

            st.markdown(f"""

            <div class="card blue">
            <h3>Today's Sales</h3>
            <h1>₹ {total_sales}</h1>
            </div>

            """, unsafe_allow_html=True)

        with c2:

            st.markdown(f"""

            <div class="card green">
            <h3>Today's Purchase</h3>
            <h1>₹ {total_purchase}</h1>
            </div>

            """, unsafe_allow_html=True)

        with c3:

            st.markdown(f"""

            <div class="card red">
            <h3>Today's Expense</h3>
            <h1>₹ {total_expense}</h1>
            </div>

            """, unsafe_allow_html=True)

        with c4:

            st.markdown(f"""

            <div class="card purple">
            <h3>Today's Profit</h3>
            <h1>₹ {total_profit}</h1>
            </div>

            """, unsafe_allow_html=True)

        st.divider()

        st.subheader("📈 Business Analytics")

        chart_df = pd.DataFrame({

            "Type":[
                "Sales",
                "Purchase",
                "Expense",
                "Profit"
            ],

            "Amount":[
                total_sales,
                total_purchase,
                total_expense,
                total_profit
            ]

        })

        fig = px.bar(
            chart_df,
            x="Type",
            y="Amount",
            title="Business Report"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ---------------- PURCHASE ----------------

    elif page == "🛒 Purchase":

        st.title("🛒 Purchase Entry")

        col1,col2 = st.columns(2)

        with col1:

            bill_no = st.text_input(
                "Purchase Bill No"
            )

            supplier = st.text_input(
                "Supplier Name"
            )

            product = st.selectbox(
                "Product",
                product_names
            )

            product_row = product_df[
                product_df["Product"] == product
            ]

            unit = product_row.iloc[0]["Unit"]

            st.info(
                f"Unit: {unit}"
            )

            qty = st.number_input(
                "Quantity",
                min_value=0.0
            )

        with col2:

            rate = st.number_input(
                "Rate",
                value=float(
                    product_row.iloc[0]["Purchase"]
                )
            )

            total = qty * rate

            st.info(
                f"Total: ₹ {total}"
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
                f"Pending: ₹ {balance}"
            )

        if st.button("Save Purchase"):

            st.session_state.purchase_data.append({

                "Bill":bill_no,
                "Supplier":supplier,
                "Product":product,
                "Qty":qty,
                "Rate":rate,
                "Total":total,
                "Balance":balance

            })

            st.success(
                "Purchase Saved Successfully"
            )

        if len(
            st.session_state.purchase_data
        ) > 0:

            st.subheader(
                "Purchase Records"
            )

            purchase_df = pd.DataFrame(
                st.session_state.purchase_data
            )

            st.dataframe(
                purchase_df,
                use_container_width=True
            )

    # ---------------- SALES ----------------

    elif page == "💰 Sales":

        st.title("💰 Sales Entry")

        col1,col2 = st.columns(2)

        with col1:

            bill_no = st.text_input(
                "Sales Bill No"
            )

            customer = st.text_input(
                "Customer Name"
            )

            product = st.selectbox(
                "Product",
                product_names,
                key="sales"
            )

            product_row = product_df[
                product_df["Product"] == product
            ]

            unit = product_row.iloc[0]["Unit"]

            st.info(
                f"Unit: {unit}"
            )

            stock = product_row.iloc[0]["Stock"]

            st.info(
                f"Available Stock: {stock}"
            )

            qty = st.number_input(
                "Sales Qty",
                min_value=0.0
            )

        with col2:

            rate = st.number_input(
                "Sales Rate",
                value=float(
                    product_row.iloc[0]["Sale"]
                )
            )

            total = qty * rate

            st.info(
                f"Sales Total: ₹ {total}"
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
                f"Pending: ₹ {balance}"
            )

        if st.button("Save Sales"):

            st.session_state.sales_data.append({

                "Bill":bill_no,
                "Customer":customer,
                "Product":product,
                "Qty":qty,
                "Rate":rate,
                "Total":total,
                "Balance":balance

            })

            st.success(
                "Sales Saved Successfully"
            )

        if len(
            st.session_state.sales_data
        ) > 0:

            st.subheader(
                "Sales Records"
            )

            sales_df = pd.DataFrame(
                st.session_state.sales_data
            )

            st.dataframe(
                sales_df,
                use_container_width=True
            )

    # ---------------- EXPENSE ----------------

    elif page == "💸 Expense":

        st.title("💸 Expense Entry")

        expense_name = st.text_input(
            "Expense Name"
        )

        amount = st.number_input(
            "Expense Amount",
            min_value=0.0
        )

        payment = st.selectbox(

            "Payment Mode",

            [
                "Cash",
                "Online"
            ]
        )

        if st.button("Save Expense"):

            st.session_state.expense_data.append({

                "Expense":expense_name,
                "Amount":amount,
                "Payment":payment

            })

            st.success(
                "Expense Saved Successfully"
            )

        if len(
            st.session_state.expense_data
        ) > 0:

            expense_df = pd.DataFrame(
                st.session_state.expense_data
            )

            st.dataframe(
                expense_df,
                use_container_width=True
            )

    # ---------------- STOCK ----------------

    elif page == "📦 Stock":

        st.title("📦 Stock Management")

        st.dataframe(
            product_df,
            use_container_width=True
        )

        low_stock = product_df[
            product_df["Stock"] < 10
        ]

        if len(low_stock) > 0:

            st.error(
                "⚠️ Low Stock Alert"
            )

            st.dataframe(
                low_stock,
                use_container_width=True
            )

    # ---------------- CUSTOMER LEDGER ----------------

    elif page == "📒 Customer Ledger":

        st.title("📒 Customer Ledger")

        if len(
            st.session_state.sales_data
        ) > 0:

            sales_df = pd.DataFrame(
                st.session_state.sales_data
            )

            st.dataframe(
                sales_df,
                use_container_width=True
            )

        else:

            st.warning(
                "No Customer Record Found"
            )

    # ---------------- SUPPLIER LEDGER ----------------

    elif page == "🏪 Supplier Ledger":

        st.title("🏪 Supplier Ledger")

        if len(
            st.session_state.purchase_data
        ) > 0:

            purchase_df = pd.DataFrame(
                st.session_state.purchase_data
            )

            st.dataframe(
                purchase_df,
                use_container_width=True
            )

        else:

            st.warning(
                "No Supplier Record Found"
            )

    # ---------------- ANALYTICS ----------------

    elif page == "📈 Analytics":

        st.title("📈 Analytics")

        analytics_df = pd.DataFrame({

            "Category":[
                "Sales",
                "Purchase",
                "Expense",
                "Profit"
            ],

            "Amount":[
                total_sales,
                total_purchase,
                total_expense,
                total_profit
            ]

        })

        pie_chart = px.pie(
            analytics_df,
            names="Category",
            values="Amount",
            title="Business Distribution"
        )

        st.plotly_chart(
            pie_chart,
            use_container_width=True
        )

    # ---------------- DAILY CLOSING ----------------

    elif page == "🧾 Daily Closing":

        st.title("🧾 Daily Closing")

        closing_data = {

            "Today's Sales":[
                total_sales
            ],

            "Today's Purchase":[
                total_purchase
            ],

            "Today's Expense":[
                total_expense
            ],

            "Today's Profit":[
                total_profit
            ]

        }

        closing_df = pd.DataFrame(
            closing_data
        )

        st.dataframe(
            closing_df,
            use_container_width=True
        )

        st.success(
            "Daily Closing Generated Successfully"
        )
