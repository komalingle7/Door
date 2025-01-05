import streamlit as st
from datetime import datetime
import pandas as pd

# Custom CSS for a fancy design
st.markdown(
    """
    <style>
    /* Set a gradient background */
    .reportview-container {
        background: url('images/work2.jpg') no-repeat center center fixed;  /* Use relative path to image */
        background-size: cover;
        padding: 20px;
        font-family: 'Arial', sans-serif;
        height: 100vh;
    }

    /* Style the title */
    .css-1d391kg {
        color: white;
        font-size: 40px;
        font-weight: bold;
    }

    /* Style the sidebar */
    .sidebar .sidebar-content {
        background-color: #1e2a47;
        color: white;
        font-size: 18px;
    }

    /* Customize the buttons */
    .stButton>button {
        background-color: #ff6f61;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 10px 20px;
    }

    /* Style the input fields */
    .stTextInput>label {
        color: #333;
    }
    .stTextInput>div>input {
        background-color: #f0f4f8;
        border: 1px solid #ccc;
        border-radius: 5px;
        padding: 10px;
    }

    /* Table Style */
    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 30px;
    }
    th, td {
        padding: 12px;
        text-align: left;
    }
    th {
        background-color: #4CAF50;
        color: white;
    }
    tr:nth-child(even) {
        background-color: #f2f2f2;
    }
    </style>
    """, unsafe_allow_html=True
)

# Title of the App
st.title("Kunal Fiber Tech Industries")

# Sidebar Content for navigation
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", ["Add Customer", "View Customer List"])

# Store customer data in a list (in place of a database for simplicity)
if 'customers' not in st.session_state:
    st.session_state.customers = []

# Add Customer Page
if menu == "Add Customer":
    st.header("🔧 Add Customer Details")

    # Customer information form
    with st.form(key='customer_form'):
        customer_name = st.text_input("Customer Name")
        date = st.date_input("Date of Purchase", min_value=datetime.today())
        size = st.text_input("Size")
        design = st.text_input("Design")
        colour = st.text_input("Colour")
        rate = st.number_input("Rate (₹)", min_value=0.0, step=0.1, format="%.2f")
        bill_amount = st.number_input("Bill Amount (₹)", min_value=0.0, step=0.1, format="%.2f")
        balance_amount = st.number_input("Balance Amount (₹)", min_value=0.0, step=0.1, format="%.2f")

        # Submit button
        submit_button = st.form_submit_button(label='Add Customer')

    # Save customer data to session state
    if submit_button:
        if not customer_name or not size or not design or not colour:
            st.warning("Please fill all the details before submitting.")
        else:
            customer = {
                "Customer Name": customer_name,
                "Date": str(date),
                "Size": size,
                "Design": design,
                "Colour": colour,
                "Rate": rate,
                "Bill Amount": bill_amount,
                "Balance Amount": balance_amount
            }
            st.session_state.customers.append(customer)
            st.success(f"Customer {customer_name} added successfully!")

# View Customer List Page
if menu == "View Customer List":
    st.header("📋 Customer List")

    # Display customer list as a table
    if len(st.session_state.customers) > 0:
        customer_df = pd.DataFrame(st.session_state.customers)

        # Display the data frame
        customer_df['Rate'] = customer_df['Rate'].apply(lambda x: f"₹ {x:.2f}")
        customer_df['Bill Amount'] = customer_df['Bill Amount'].apply(lambda x: f"₹ {x:.2f}")
        customer_df['Balance Amount'] = customer_df['Balance Amount'].apply(lambda x: f"₹ {x:.2f}")

        st.table(customer_df)

        # Select a customer to view/edit
        selected_customer_name = st.selectbox("Select a customer to view/edit", customer_df["Customer Name"])

        # Show selected customer details
        selected_customer = customer_df[customer_df["Customer Name"] == selected_customer_name].iloc[0]

        # Display customer details
        st.subheader(f"Customer Details: {selected_customer_name}")
        st.write(f"**Date of Purchase:** {selected_customer['Date']}")
        st.write(f"**Size:** {selected_customer['Size']}")
        st.write(f"**Design:** {selected_customer['Design']}")
        st.write(f"**Colour:** {selected_customer['Colour']}")
        st.write(f"**Rate:** {selected_customer['Rate']}")
        st.write(f"**Bill Amount:** {selected_customer['Bill Amount']}")
        st.write(f"**Balance Amount:** {selected_customer['Balance Amount']}")

        # Ensure `selected_customer['Balance Amount']` is treated as a float for editing
        try:
            new_balance = float(
                selected_customer['Balance Amount'].replace('₹', '').strip())  # Convert the string to float
        except ValueError:
            new_balance = 0.0  # Default if conversion fails

        # Option to edit the balance amount
        new_balance = st.number_input("Edit Balance Amount (₹)", min_value=0.0, step=0.1, value=new_balance)
        if st.button("Update Balance"):
            # Update balance amount in session state
            for customer in st.session_state.customers:
                if customer["Customer Name"] == selected_customer_name:
                    customer["Balance Amount"] = f"₹ {new_balance:.2f}"
            st.success(f"Balance amount for {selected_customer_name} updated to ₹{new_balance:.2f}")
    else:
        st.write("No customers added yet.")
