import streamlit as st
import pandas as pd
import re

# Initialize the transactions dataframe
@st.cache
def load_data(file=None):
    if file is not None:
        try:
            transactions = pd.read_csv(file)
        except FileNotFoundError:
            st.error("File not found. Please upload the correct CSV file.")
            return pd.DataFrame(columns=['amount', 'type', 'date'])
    else:
        # If no file is provided, try loading the local transactions.csv
        try:
            transactions = pd.read_csv('transactions.csv')
        except FileNotFoundError:
            transactions = pd.DataFrame(columns=['amount', 'type', 'date'])
    return transactions

# Function to classify input transactions based on message content
def classify_transaction(message):
    if 'spent' in message.lower() or 'buy' in message.lower():
        return 'debt'  # Classify as expense
    elif 'received' in message.lower() or 'income' in message.lower():
        return 'credit'  # Classify as income
    else:
        return 'unknown'  # Could not classify

# Streamlit UI
st.title("Expense Tracker")

# File uploader to input CSV data
uploaded_file = st.file_uploader("Upload a CSV file with transaction data", type=["csv"])

if uploaded_file:
    transactions = load_data(uploaded_file)
else:
    transactions = load_data()  # Load the saved transactions from 'transactions.csv'

# Display uploaded data or input form
if uploaded_file:
    st.write("Uploaded Transactions Data:")
    st.dataframe(transactions)

# Streamlit section for inputting transactions manually
st.write("Enter your transaction message (e.g., 'I spent 50 on groceries' or 'Received 1000 as salary'):")
message = st.text_input("Transaction message")

if st.button("Submit"):
    try:
        # Extract the amount from the message
        amount = float(re.search(r'\d+', message).group())
        transaction_type = classify_transaction(message)
        date = pd.Timestamp.now()  # Use the current date for the transaction

        if transaction_type != 'unknown':
            # Append the new transaction to the dataframe
            new_transaction = pd.DataFrame({'amount': [amount], 'type': [transaction_type], 'date': [date]})
            transactions = pd.concat([transactions, new_transaction], ignore_index=True)

            # Save the updated transactions to the CSV file
            transactions.to_csv('transactions.csv', index=False)

            st.success(f"Transaction added: {transaction_type} of ${amount}")
        else:
            st.error("Unable to classify the transaction. Please try again.")
    except AttributeError:
        st.error("Invalid message format. Please include a valid amount in your message.")

# Display the transaction log
st.write("Transactions Log:")
st.dataframe(transactions)
