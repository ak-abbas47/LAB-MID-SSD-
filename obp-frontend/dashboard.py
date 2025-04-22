import streamlit as st
import requests

API_URL = "http://localhost:8000"  # Change if deployed elsewhere

st.title("💳 Online Banking Platform")

# -------------------------------
# Accounts Management
# -------------------------------
st.header("🏦 Accounts Management")

# Get All Accounts
if st.button("📄 Get All Accounts"):
    response = requests.get(f"{API_URL}/accounts/")
    if response.status_code == 200:
        st.json(response.json())
    else:
        st.error("Failed to fetch accounts!")

# Add New Account
st.subheader("➕ Add New Account")
account_number = st.text_input("Account Number")
owner_name = st.text_input("Owner Name")
account_type = st.selectbox("Account Type", ["savings", "checking"])
balance = st.number_input("Initial Balance", min_value=0.0, step=0.01)

if st.button("✅ Create Account"):
    data = {
        "account_number": account_number,
        "owner_name": owner_name,
        "account_type": account_type,
        "balance": balance
    }
    response = requests.post(f"{API_URL}/accounts/", data=data)
    if response.status_code in [200, 201]:
        st.success("Account created successfully!")
    else:
        st.error("Failed to create account!")

# Update Account
st.subheader("✏️ Update Account")
account_id = st.number_input("Account ID", min_value=1, step=1)
new_balance = st.number_input("Updated Balance", min_value=0.0, step=0.01)
new_type = st.selectbox("Updated Account Type", ["savings", "checking"])

if st.button("🔁 Update Account"):
    data = {
        "account_type": new_type,
        "balance": new_balance
    }
    response = requests.put(f"{API_URL}/accounts/{account_id}", data=data)
    if response.status_code == 200:
        st.success("Account updated successfully!")
    else:
        st.error("Failed to update account!")

# Delete Account
st.subheader("🗑️ Delete Account")
delete_id = st.number_input("Account ID to Delete", min_value=1, step=1)

if st.button("❌ Delete Account"):
    response = requests.delete(f"{API_URL}/accounts/{delete_id}")
    if response.status_code == 200:
        st.success("Account deleted successfully!")
    else:
        st.error("Failed to delete account!")

# -------------------------------
# Transactions Management
# -------------------------------
st.header("💰 Transactions Management")

# View All Transactions
if st.button("📄 Get All Transactions"):
    response = requests.get(f"{API_URL}/transactions/")
    if response.status_code == 200:
        st.json(response.json())
    else:
        st.error("Failed to fetch transactions!")

# View Transactions by Account
account_filter_id = st.number_input("Account ID (Filter Transactions)", min_value=1, step=1)
if st.button("🔎 Get Transactions for Account"):
    response = requests.get(f"{API_URL}/transactions/account/{account_filter_id}")
    if response.status_code == 200:
        st.json(response.json())
    else:
        st.error("Failed to fetch transactions!")

# Add New Transaction
st.subheader("➕ Add New Transaction")
# txn_account_id = st.number_input("Account ID", min_value=1, step=1)
txn_account_id = st.number_input("Account ID", min_value=1, step=1, key="txn_account_id_input")
txn_type = st.selectbox("Transaction Type", ["deposit", "withdrawal"])
txn_amount = st.number_input("Amount", min_value=0.0, step=0.01)

if st.button("✅ Submit Transaction"):
    data = {
        "account_id": txn_account_id,
        "type": txn_type,
        "amount": txn_amount
    }
    response = requests.post(f"{API_URL}/transactions/", data=data)
    if response.status_code == 200:
        st.success("Transaction successful!")
    else:
        try:
            error_msg = response.json().get("detail", "Error occurred")
            st.error(error_msg)
        except:
            st.error("Failed to create transaction!")

# Delete Transaction
st.subheader("🗑️ Delete Transaction")
txn_delete_id = st.number_input("Transaction ID to Delete", min_value=1, step=1)

if st.button("❌ Delete Transaction"):
    response = requests.delete(f"{API_URL}/transactions/{txn_delete_id}")
    if response.status_code == 200:
        st.success("Transaction deleted successfully!")
    else:
        st.error("Failed to delete transaction!")
