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

.card1{
    background:linear-gradient(135deg,#2563eb,#1d4ed8);
    padding:20px;
    border-radius:20px;
    color:white;
    text-align:center;
}

.card2{
    background:linear-gradient(135deg,#059669,#10b981);
    padding:20px;
    border-radius:20px;
    color:white;
    text-align:center;
}

.card3{
    background:linear-gradient(135deg,#dc2626,#ef4444);
    padding:20px;
    border-radius:20px;
    color:white;
    text-align:center;
}

.card4{
    background:linear-gradient(135deg,#7c3aed,#9333ea);
    padding:20px;
    border-radius:20px;
    color:white;
    text-align:center;
}

</style>

""", unsafe_allow_html=True)

# ---------------- LOGIN STATE ----------------

if "login" not in st.session_state:
    st.session_state.login = False

# ---------------- LOGIN PAGE ----------------

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
            st.success("Login Success")
            st.rerun()

        else:

            st.error("Wrong Username or Password")

    st.divider()

    st.subheader("Forgot Password")

    forgot_user = st.text_input(
        "Enter Username"
    )

    if st.button("Recover Password"):

        if forgot_user == "admin":

            st.info(
                "Your Password is: admin123"
            )

        else:

            st.error("Username Not Found")

# ---------------- ERP ----------------

else:

    # ---------- SIDEBAR ----------

    st.sidebar.title("🐶 LAIKA ERP")

    if st.sidebar.button("Logout"):

        st.session_state.login = False
        st.rerun()

    page = st.sidebar.radio(

        "Menu",

        [
            "Dashboard",
            "Purchase",
            "Sales",
            "Expense",
            "Stock"
        ]
    )

    # ---------- DATE ----------

    today = datetime.now()

    today_date = today.strftime("%d-%m-%Y")

    today_day = calendar.day_name[
        today.weekday()
    ]

    # ---------- DASHBOARD ----------

    if page == "Dashboard":

        st.title("📊 Dashboard")

        st.subheader(
            f"📅 {today_date} | {today_day}"
        )

        c1,c2,c3,c4 = st.columns(4)

        with c1:

            st.markdown(f"""

            <div class="card1">
            <h3>Today's Sales</h3>
            <h1>₹ 0</h1>
            </div>

            """, unsafe_allow_html=True)

        with c2:

            st.markdown(f"""

            <div class="card2">
            <h3>Today's Purchase</h3>
            <h1>₹ 0</h1>
            </div>

            """, unsafe_allow_html=True)

        with c3:

            st.markdown(f"""

            <div class="card3">
            <h3>Today's Expense</h3>
            <h1>₹ 0</h1>
            </div>

            """, unsafe_allow_html=True)

        with c4:

            st.markdown(f"""

            <div class="card4">
            <h3>Today's Profit</h3>
            <h1>₹ 0</h1>
            </div>

            """, unsafe_allow_html=True)

        st.divider()

        st.success(
            "✅ ERP Running Successfully"
        )

    # ---------- PURCHASE ----------

    elif page == "Purchase":

        st.title("🛒 Purchase Entry")

        bill_no = st.text_input(
            "Bill Number"
        )

        product = st.text_input(
            "Product Name"
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

        st.info(f"Total: ₹ {total}")

        if st.button("Save Purchase"):

            st.success(
                "Purchase Saved"
            )

        st.divider()

        st.subheader("Delete Purchase Entry")

        delete_purchase = st.text_input(
            "Enter Bill Number to Delete"
        )

        if st.button("Delete Purchase"):

            st.warning(
                f"Purchase Bill {delete_purchase} Deleted"
            )

    # ---------- SALES ----------

    elif page == "Sales":

        st.title("💰 Sales Entry")

        bill_no = st.text_input(
            "Sales Bill No"
        )

        customer = st.text_input(
            "Customer Name"
        )

        qty = st.number_input(
            "Sales Quantity",
            min_value=0.0
        )

        rate = st.number_input(
            "Sales Rate",
            min_value=0.0
        )

        total = qty * rate

        st.info(f"Sales Total: ₹ {total}")

        if st.button("Save Sales"):

            st.success(
                "Sales Saved"
            )

        st.divider()

        st.subheader("Delete Sales Entry")

        delete_sales = st.text_input(
            "Enter Sales Bill No"
        )

        if st.button("Delete Sales"):

            st.warning(
                f"Sales Bill {delete_sales} Deleted"
            )

    # ---------- EXPENSE ----------

    elif page == "Expense":

        st.title("💸 Expense Entry")

        expense_name = st.text_input(
            "Expense Name"
        )

        amount = st.number_input(
            "Amount",
            min_value=0.0
        )

        if st.button("Save Expense"):

            st.success(
                "Expense Saved"
            )

        st.divider()

        st.subheader("Delete Expense")

        delete_expense = st.text_input(
            "Expense Name Delete"
        )

        if st.button("Delete Expense Entry"):

            st.warning(
                f"{delete_expense} Deleted"
            )

    # ---------- STOCK ----------

    elif page == "Stock":

        st.title("📦 Stock")

        stock_data = {

            "Product":[
                "Pedigree",
                "Whiskas",
                "Bird Seeds"
            ],

            "Stock":[
                20,
                15,
                30
            ]

        }

        df = pd.DataFrame(stock_data)

        st.dataframe(
            df,
            use_container_width=True
        )

        st.warning(
            "⚠️ Low Stock Alert"
        )
