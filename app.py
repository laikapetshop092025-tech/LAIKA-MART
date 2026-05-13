import streamlit as st
import pandas as pd
from datetime import datetime
import calendar

# ================= PAGE =================

st.set_page_config(
    page_title="LAIKA ERP PRO MAX",
    layout="wide"
)

# ================= SESSION =================

defaults = {

    "login": False,
    "purchase_data": [],
    "sales_data": [],
    "expense_data": [],
    "pets": [],
    "reward_points": {},
    "purchase_bill": 1001,
    "sales_bill": 5001

}

for key, value in defaults.items():

    if key not in st.session_state:

        st.session_state[key] = value

# ================= CSS =================

st.markdown("""

<style>

.main{
    background:#fdf4ff;
}

/* SIDEBAR */

[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#d8b4fe,#f9a8d4);
    padding-top:20px;
}

[data-testid="stSidebar"] *{
    color:white;
}

/* BUTTON */

.stButton>button{
    width:100%;
    border:none;
    border-radius:14px;
    padding:12px;
    font-size:16px;
    font-weight:bold;
    background:linear-gradient(90deg,#d946ef,#9333ea);
    color:white;
    transition:0.3s;
}

.stButton>button:hover{
    transform:scale(1.03);
    background:linear-gradient(90deg,#c026d3,#7e22ce);
}

/* CARDS */

.card{
    padding:20px;
    border-radius:20px;
    color:white;
    text-align:center;
    height:150px;
    display:flex;
    flex-direction:column;
    justify-content:center;
    margin-bottom:15px;
}

.pink{
    background:linear-gradient(135deg,#f9a8d4,#ec4899);
}

.purple{
    background:linear-gradient(135deg,#c084fc,#9333ea);
}

.blue{
    background:linear-gradient(135deg,#93c5fd,#2563eb);
}

.green{
    background:linear-gradient(135deg,#86efac,#16a34a);
}

.orange{
    background:linear-gradient(135deg,#fdba74,#ea580c);
}

</style>

""", unsafe_allow_html=True)

# ================= LOGIN =================

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

            st.info("Password: admin123")

        else:

            st.error("Username Not Found")

# ================= ERP =================

else:

    # ================= PRODUCTS =================

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
            "Purchase":500,
            "Sale":700,
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

    # ================= STOCK UPDATE =================

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

    # ================= SIDEBAR =================

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

    # ================= DATE =================

    today = datetime.now()

    today_date = today.strftime(
        "%d-%m-%Y"
    )

    today_day = calendar.day_name[
        today.weekday()
    ]

    # ================= TOTALS =================

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

    # ================= CASH / ONLINE =================

    total_cash = 0
    total_online = 0

    for s in st.session_state.sales_data:

        payment = s.get("Payment", "")
        paid = s.get("Paid", 0)

        if payment == "Cash":

            total_cash += paid

        elif payment == "Online":

            total_online += paid

    total_collection = (
        total_cash
        + total_online
    )

    # ================= DASHBOARD =================

    if page == "📊 Dashboard":

        st.title("📊 LAIKA ERP DASHBOARD")

        st.subheader(
            f"📅 {today_date} | {today_day}"
        )

        c1,c2,c3,c4 = st.columns(4)

        with c1:

            st.markdown(f"""

            <div class="card pink">
            <h3>Total Sales</h3>
            <h1>₹ {total_sales}</h1>
            </div>

            """, unsafe_allow_html=True)

        with c2:

            st.markdown(f"""

            <div class="card purple">
            <h3>Total Purchase</h3>
            <h1>₹ {total_purchase}</h1>
            </div>

            """, unsafe_allow_html=True)

        with c3:

            st.markdown(f"""

            <div class="card blue">
            <h3>Total Expense</h3>
            <h1>₹ {total_expense}</h1>
            </div>

            """, unsafe_allow_html=True)

        with c4:

            st.markdown(f"""

            <div class="card green">
            <h3>Total Profit</h3>
            <h1>₹ {total_profit}</h1>
            </div>

            """, unsafe_allow_html=True)

        st.divider()

        d1,d2,d3 = st.columns(3)

        with d1:

            st.markdown(f"""

            <div class="card orange">
            <h3>Cash Collection</h3>
            <h1>₹ {total_cash}</h1>
            </div>

            """, unsafe_allow_html=True)

        with d2:

            st.markdown(f"""

            <div class="card pink">
            <h3>Online Collection</h3>
            <h1>₹ {total_online}</h1>
            </div>

            """, unsafe_allow_html=True)

        with d3:

            st.markdown(f"""

            <div class="card purple">
            <h3>Total Collection</h3>
            <h1>₹ {total_collection}</h1>
            </div>

            """, unsafe_allow_html=True)

    # ================= PURCHASE =================

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

            st.info(f"Total: ₹ {total}")

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
                "Purchase Saved"
            )

        if len(
            st.session_state.purchase_data
        ) > 0:

            st.subheader("Purchase Entries")

            purchase_df = pd.DataFrame(
                st.session_state.purchase_data
            )

            st.dataframe(
                purchase_df,
                use_container_width=True
            )

            delete_purchase = st.selectbox(

                "Delete Purchase Bill",

                range(
                    len(
                        st.session_state.purchase_data
                    )
                ),

                format_func=lambda x:
                st.session_state.purchase_data[x]["Bill"]

            )

            if st.button("Delete Purchase"):

                st.session_state.purchase_data.pop(
                    delete_purchase
                )

                st.success(
                    "Purchase Deleted"
                )

                st.rerun()

    # ================= SALES =================

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
                "Sales Saved"
            )

        if len(
            st.session_state.sales_data
        ) > 0:

            st.subheader("Sales Entries")

            sales_df = pd.DataFrame(
                st.session_state.sales_data
            )

            st.dataframe(
                sales_df,
                use_container_width=True
            )

            delete_sales = st.selectbox(

                "Delete Sales Bill",

                range(
                    len(
                        st.session_state.sales_data
                    )
                ),

                format_func=lambda x:
                st.session_state.sales_data[x]["Bill"]

            )

            if st.button("Delete Sales"):

                st.session_state.sales_data.pop(
                    delete_sales
                )

                st.success(
                    "Sales Deleted"
                )

                st.rerun()

    # ================= EXPENSE =================

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

            delete_expense = st.selectbox(

                "Delete Expense",

                range(
                    len(
                        st.session_state.expense_data
                    )
                ),

                format_func=lambda x:
                st.session_state.expense_data[x]["Expense"]

            )

            if st.button("Delete Expense Entry"):

                st.session_state.expense_data.pop(
                    delete_expense
                )

                st.success(
                    "Expense Deleted"
                )

                st.rerun()

    # ================= STOCK =================

    elif page == "📦 Stock":

        st.title("📦 Stock Management")

        st.dataframe(
            product_df,
            use_container_width=True
        )

    # ================= CUSTOMER LEDGER =================

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

    # ================= SUPPLIER LEDGER =================

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

    # ================= PET REGISTER =================

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
                "Pet Registered"
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

    # ================= ANALYTICS =================

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

    # ================= DAILY CLOSING =================

    elif page == "🧾 Daily Closing":

        st.title("🧾 Daily Closing")

        closing_df = pd.DataFrame({

            "Sales":[total_sales],
            "Purchase":[total_purchase],
            "Expense":[total_expense],
            "Profit":[total_profit],
            "Cash":[total_cash],
            "Online":[total_online],
            "Collection":[total_collection]

        })

        st.dataframe(
            closing_df,
            use_container_width=True
        )

        st.success(
            "Daily Closing Generated"
        )
