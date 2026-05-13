import streamlit as st
import pandas as pd
from datetime import datetime
import calendar

# ---------------- PAGE ----------------

st.set_page_config(
    page_title="LAIKA ERP PRO MAX",
    layout="wide"
)

# ---------------- SESSION ----------------

default_keys = {

    "login": False,
    "purchase_data": [],
    "sales_data": [],
    "expense_data": [],
    "customer_payments": [],
    "supplier_payments": [],
    "pets": [],
    "reward_points": {},
    "purchase_bill": 1001,
    "sales_bill": 5001

}

for key, value in default_keys.items():

    if key not in st.session_state:

        st.session_state[key] = value

# ---------------- CSS ----------------

st.markdown("""

<style>

.main{
    background:#eef4ff;
}

[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#1e3a8a,#4f46e5);
    padding-top:20px;
}

[data-testid="stSidebar"] *{
    color:white;
}

.stButton>button{
    width:100%;
    border:none;
    border-radius:14px;
    padding:12px;
    font-size:16px;
    font-weight:bold;
    background:linear-gradient(90deg,#2563eb,#7c3aed);
    color:white;
    transition:0.3s;
}

.stButton>button:hover{
    transform:scale(1.03);
    background:linear-gradient(90deg,#1d4ed8,#6d28d9);
    box-shadow:0 0 15px rgba(0,0,0,0.3);
}

.card{
    padding:20px;
    border-radius:18px;
    color:white;
    text-align:center;
    height:145px;
    display:flex;
    flex-direction:column;
    justify-content:center;
    margin-bottom:15px;
    transition:0.3s;
}

.card:hover{
    transform:translateY(-5px);
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

    # ---------------- PRODUCTS ----------------

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

    # ---------------- STOCK UPDATE ----------------

    for p in st.session_state.purchase_data:

        for item in products:

            if item["Product"] == p.get("Product"):

                item["Stock"] += p.get("Qty", 0)

    for s in st.session_state.sales_data:

        for item in products:

            if item["Product"] == s.get("Product"):

                item["Stock"] -= s.get("Qty", 0)

    product_df = pd.DataFrame(products)

    product_names = list(
        product_df["Product"]
    )

    # ---------------- SIDEBAR ----------------

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
            "🐾 Pet Register",
            "📈 Analytics",
            "🧾 Daily Closing"

        ]
    )

    # ---------------- DATE ----------------

    today = datetime.now()

    today_date = today.strftime(
        "%d-%m-%Y"
    )

    today_day = calendar.day_name[
        today.weekday()
    ]

    # ---------------- TOTALS ----------------

    total_sales = sum(
        item.get("Total", 0)
        for item in st.session_state.sales_data
    )

    total_purchase = sum(
        item.get("Total", 0)
        for item in st.session_state.purchase_data
    )

    total_expense = sum(
        item.get("Amount", 0)
        for item in st.session_state.expense_data
    )

    total_profit = (
        total_sales
        - total_purchase
        - total_expense
    )

    # ---------------- CASH / ONLINE ----------------

    total_cash = 0
    total_online = 0

    for s in st.session_state.sales_data:

        payment_mode = s.get(
            "Payment",
            ""
        )

        paid_amount = s.get(
            "Paid",
            0
        )

        if payment_mode == "Cash":

            total_cash += paid_amount

        elif payment_mode == "Online":

            total_online += paid_amount

    # ---------------- DASHBOARD ----------------

    if page == "📊 Dashboard":

        st.title("📊 LAIKA ERP DASHBOARD")

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

        m1,m2,m3,m4 = st.columns(4)

        with m1:

            st.markdown(f"""

            <div class="card orange">
            <h3>Cash</h3>
            <h1>₹ {total_cash}</h1>
            </div>

            """, unsafe_allow_html=True)

        with m2:

            st.markdown(f"""

            <div class="card blue">
            <h3>Online</h3>
            <h1>₹ {total_online}</h1>
            </div>

            """, unsafe_allow_html=True)

        with m3:

            st.markdown("""

            <div class="card green">
            <h3>ERP Status</h3>
            <h1>ACTIVE</h1>
            </div>

            """, unsafe_allow_html=True)

        with m4:

            st.markdown("""

            <div class="card red">
            <h3>Version</h3>
            <h1>PRO MAX</h1>
            </div>

            """, unsafe_allow_html=True)

    # ---------------- PURCHASE ----------------

    elif page == "🛒 Purchase":

        st.title("🛒 Purchase Entry")

        col1,col2 = st.columns(2)

        with col1:

            bill_no = st.text_input(
                "Purchase Bill Number",
                value=str(
                    st.session_state.purchase_bill
                )
            )

            supplier = st.text_input(
                "Supplier Name"
            )

            product = st.selectbox(
                "Product",
                product_names
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
                f"Pending: ₹ {balance}"
            )

        if st.button("Save Purchase"):

            st.session_state.purchase_data.append({

                "Bill":bill_no,
                "Supplier":supplier,
                "Product":product,
                "Unit":unit,
                "Qty":qty,
                "Rate":rate,
                "Total":total,
                "Payment":payment,
                "Paid":paid,
                "Balance":balance

            })

            st.session_state.purchase_bill += 1

            st.success(
                "Purchase Saved Successfully"
            )

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

    # ---------------- SALES ----------------

    elif page == "💰 Sales":

        st.title("💰 Sales Entry")

        col1,col2 = st.columns(2)

        with col1:

            bill_no = st.text_input(
                "Sales Bill Number",
                value=str(
                    st.session_state.sales_bill
                )
            )

            customer = st.text_input(
                "Customer Name"
            )

            product = st.selectbox(
                "Product",
                product_names,
                key="sales_product"
            )

            unit = st.selectbox(

                "Unit",

                [
                    "KG",
                    "PCS",
                    "DOZEN",
                    "BAG"
                ],

                key="sales_unit"
            )

            row = product_df[
                product_df["Product"] == product
            ]

            stock = row.iloc[0]["Stock"]

            st.info(
                f"Current Stock: {stock}"
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

            reward = int(total / 100) * 50

            current_points = st.session_state.reward_points.get(
                customer,
                0
            )

            st.success(
                f"Earn Points: {reward}"
            )

            st.info(
                f"Current Points: {current_points}"
            )

            redeem = st.number_input(
                "Redeem Points",
                min_value=0
            )

            discount = (redeem / 50) * 2

            final_total = total - discount

            st.warning(
                f"Final Amount: ₹ {final_total}"
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
                "Received Amount",
                min_value=0.0
            )

            balance = final_total - paid

            st.error(
                f"Pending: ₹ {balance}"
            )

        if st.button("Save Sales"):

            st.session_state.reward_points[customer] = (

                current_points
                + reward
                - redeem

            )

            st.session_state.sales_data.append({

                "Bill":bill_no,
                "Customer":customer,
                "Product":product,
                "Unit":unit,
                "Qty":qty,
                "Rate":rate,
                "Total":final_total,
                "Payment":payment,
                "Paid":paid,
                "Balance":balance

            })

            st.session_state.sales_bill += 1

            st.success(
                "Sales Saved Successfully"
            )

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

    # ---------------- EXPENSE ----------------

    elif page == "💸 Expense":

        st.title("💸 Expense Entry")

        expense = st.text_input(
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

                "Expense":expense,
                "Amount":amount,
                "Payment":payment

            })

            st.success(
                "Expense Saved"
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

    # ---------------- PET REGISTER ----------------

    elif page == "🐾 Pet Register":

        st.title("🐾 Pet Register")

        pet_id = st.text_input(
            "Pet ID"
        )

        pet_name = st.text_input(
            "Pet Name"
        )

        owner = st.text_input(
            "Owner Name"
        )

        mobile = st.text_input(
            "Mobile Number"
        )

        pet_type = st.selectbox(

            "Pet Type",

            [
                "Dog",
                "Cat",
                "Bird",
                "Fish",
                "Other"
            ]
        )

        breed = st.text_input(
            "Breed"
        )

        age = st.text_input(
            "Age"
        )

        vaccine = st.text_input(
            "Vaccine"
        )

        notes = st.text_area(
            "Notes"
        )

        if st.button("Register Pet"):

            st.session_state.pets.append({

                "Pet ID":pet_id,
                "Pet Name":pet_name,
                "Owner":owner,
                "Mobile":mobile,
                "Type":pet_type,
                "Breed":breed,
                "Age":age,
                "Vaccine":vaccine,
                "Notes":notes

            })

            st.success(
                "Pet Registered Successfully"
            )

        if len(
            st.session_state.pets
        ) > 0:

            pet_df = pd.DataFrame(
                st.session_state.pets
            )

            st.dataframe(
                pet_df,
                use_container_width=True
            )

    # ---------------- ANALYTICS ----------------

    elif page == "📈 Analytics":

        st.title("📈 Analytics")

        chart_df = pd.DataFrame({

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

        st.bar_chart(
            chart_df.set_index(
                "Category"
            )
        )

    # ---------------- DAILY CLOSING ----------------

    elif page == "🧾 Daily Closing":

        st.title("🧾 Daily Closing")

        closing_df = pd.DataFrame({

            "Sales":[total_sales],
            "Purchase":[total_purchase],
            "Expense":[total_expense],
            "Profit":[total_profit],
            "Cash":[total_cash],
            "Online":[total_online]

        })

        st.dataframe(
            closing_df,
            use_container_width=True
        )

        st.success(
            "Daily Closing Generated"
        )
