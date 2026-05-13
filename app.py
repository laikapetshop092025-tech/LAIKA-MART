import streamlit as st
import pandas as pd
from datetime import datetime
import calendar

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

/* SIDEBAR */

[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#1e3a8a,#4f46e5);
}

[data-testid="stSidebar"] *{
    color:white;
}

/* BUTTON */

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

/* CARDS */

.card{
    padding:25px;
    border-radius:20px;
    color:white;
    text-align:center;
    height:150px;
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

if "login" not in st.session_state:
    st.session_state.login = False

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

            st.error("Wrong Username or Password")

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

            st.error("Username Not Found")

# ---------------- ERP ----------------

else:

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
            "📦 Stock"
        ]
    )

    today = datetime.now()

    today_date = today.strftime("%d-%m-%Y")

    today_day = calendar.day_name[
        today.weekday()
    ]

    # ---------------- DASHBOARD ----------------

    if page == "📊 Dashboard":

        st.title("📊 LAIKA ERP DASHBOARD")

        st.subheader(
            f"📅 {today_date} | {today_day}"
        )

        c1,c2,c3,c4 = st.columns(4)

        with c1:

            st.markdown("""

            <div class="card blue">
            <h3>Today's Sales</h3>
            <h1>₹ 0</h1>
            </div>

            """, unsafe_allow_html=True)

        with c2:

            st.markdown("""

            <div class="card green">
            <h3>Today's Purchase</h3>
            <h1>₹ 0</h1>
            </div>

            """, unsafe_allow_html=True)

        with c3:

            st.markdown("""

            <div class="card red">
            <h3>Today's Expense</h3>
            <h1>₹ 0</h1>
            </div>

            """, unsafe_allow_html=True)

        with c4:

            st.markdown("""

            <div class="card purple">
            <h3>Today's Profit</h3>
            <h1>₹ 0</h1>
            </div>

            """, unsafe_allow_html=True)

        st.divider()

        st.subheader("📈 Monthly Report")

        m1,m2,m3,m4 = st.columns(4)

        with m1:

            st.markdown("""

            <div class="card orange">
            <h3>Monthly Sales</h3>
            <h1>₹ 0</h1>
            </div>

            """, unsafe_allow_html=True)

        with m2:

            st.markdown("""

            <div class="card blue">
            <h3>Monthly Purchase</h3>
            <h1>₹ 0</h1>
            </div>

            """, unsafe_allow_html=True)

        with m3:

            st.markdown("""

            <div class="card green">
            <h3>Monthly Expense</h3>
            <h1>₹ 0</h1>
            </div>

            """, unsafe_allow_html=True)

        with m4:

            st.markdown("""

            <div class="card purple">
            <h3>Monthly Profit</h3>
            <h1>₹ 0</h1>
            </div>

            """, unsafe_allow_html=True)

    # ---------------- PURCHASE ----------------

    elif page == "🛒 Purchase":

        st.title("🛒 Purchase Entry")

        col1,col2 = st.columns(2)

        with col1:

            bill_no = st.text_input(
                "Bill Number"
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

        with col2:

            rate = st.number_input(
                "Rate",
                min_value=0.0
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
                f"Balance: ₹ {balance}"
            )

        if st.button("Save Purchase"):

            st.success(
                "Purchase Saved Successfully"
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
                f"Pending Amount: ₹ {balance}"
            )

        if st.button("Save Sales"):

            st.success(
                "Sales Saved Successfully"
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

            st.success(
                "Expense Saved Successfully"
            )

    # ---------------- STOCK ----------------

    elif page == "📦 Stock":

        st.title("📦 Stock Management")

        stock_data = {

            "Product":[
                "Pedigree",
                "Whiskas",
                "Bird Seeds"
            ],

            "Stock":[
                25,
                10,
                30
            ],

            "Unit":[
                "PCS",
                "PCS",
                "KG"
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
