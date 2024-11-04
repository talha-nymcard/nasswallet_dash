import pandas as pd
import streamlit as st

# Function to load data from CSV files
def load_data():
    yesterday_df = pd.read_csv('transaction_yesterday.csv')
    inception_df = pd.read_csv('transaction_inception.csv')
    inception_df['date'] = pd.to_datetime(inception_df['date'], errors='coerce')  # Convert to datetime
    return yesterday_df, inception_df

# Function to calculate separated stats for IQD and USD
def calculate_separated_stats(df):
    df['amount'] = df.apply(lambda row: row.get('bill_amt') if pd.notnull(row.get('bill_amt')) else row.get('txn_amt'), axis=1)
    df['currency'] = df.apply(lambda row: row.get('bill_curr') if pd.notnull(row.get('bill_curr')) else row.get('txn_curr'), axis=1)
    df['currency'] = df['currency'].replace({368: 'IQD', 840: 'USD'})

    stats = {
        "Total Transactions": len(df),
        "Total Approved": len(df[df['transaction_status'] == 'Approved']),
        "Total Rejected": len(df[df['transaction_status'] != 'Approved'])
    }

    separated_stats = {}
    for currency in ['IQD', 'USD']:
        currency_df = df[df['currency'] == currency]
        separated_stats[currency] = {
            "Total Transactions": len(currency_df),
            "Total Approved": len(currency_df[currency_df['transaction_status'] == 'Approved']),
            "Total Rejected": len(currency_df[currency_df['transaction_status'] != 'Approved']),
            "Approved Amount": currency_df[currency_df['transaction_status'] == 'Approved']['amount'].sum(),
            "Rejected Amount": currency_df[currency_df['transaction_status'] != 'Approved']['amount'].sum()
        }
    return stats, separated_stats

# Function to apply filters to inception data
def apply_filters(df, transaction_type, transaction_status, currency, start_date, end_date):
    if transaction_type:
        df = df[df['transaction_type'] == transaction_type]
    if transaction_status:
        df = df[df['transaction_status'] == transaction_status]
    if currency:
        df = df[df['currency'] == currency]
    if start_date:
        df = df[df['date'] >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df['date'] <= pd.to_datetime(end_date)]
    return df

# Function to display summary stats as metrics with color indicators
def display_summary_tiles(stats, label=""):
    st.write(f"### {label} Summary Metrics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<h6 style='color: grey;'>Total Transactions</h6>", unsafe_allow_html=True)
        col1.metric("", stats["Total Transactions"], delta_color="off")
        
    with col2:
        st.markdown("<h6 style='color: green;'>Total Approved</h6>", unsafe_allow_html=True)
        col2.metric("", stats["Total Approved"], delta_color="normal")  # Green indicator
        
    with col3:
        st.markdown("<h6 style='color: red;'>Total Rejected</h6>", unsafe_allow_html=True)
        col3.metric("", stats["Total Rejected"], delta_color="inverse")  # Red indicator

# Function to display detailed separated stats for IQD and USD in tiles with color indicators
def display_separated_stats_tiles(separated_stats, label=""):
    st.write(f"#### {label} Metrics (IQD and USD)")
    for currency, data in separated_stats.items():
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.markdown(f"<h6 style='color: grey;'>{currency} Total Transactions</h6>", unsafe_allow_html=True)
            col1.metric("", data["Total Transactions"], delta_color="off")
        
        with col2:
            st.markdown(f"<h6 style='color: green;'>{currency} Total Approved</h6>", unsafe_allow_html=True)
            col2.metric("", data["Total Approved"], delta_color="normal")  # Green
        
        with col3:
            st.markdown(f"<h6 style='color: red;'>{currency} Total Rejected</h6>", unsafe_allow_html=True)
            col3.metric("", data["Total Rejected"], delta_color="inverse")  # Red
        
        with col4:
            st.markdown(f"<h6 style='color: green;'>{currency} Approved Amount</h6>", unsafe_allow_html=True)
            col4.metric("", f"{data['Approved Amount']:.2f}", delta_color="normal")  # Green
        
        with col5:
            st.markdown(f"<h6 style='color: red;'>{currency} Rejected Amount</h6>", unsafe_allow_html=True)
            col5.metric("", f"{data['Rejected Amount']:.2f}", delta_color="inverse")  # Red

# Main function to display transaction metrics with filtering options
def display_transaction_metrics():
    # Load the data
    yesterday_df, inception_df = load_data()

    # Display summary tiles for Yesterday and Inception stats
    inception_stats, inception_separated_stats = calculate_separated_stats(inception_df)
    display_summary_tiles(inception_stats, label="Inception")
    display_separated_stats_tiles(inception_separated_stats, label="Inception")

    yesterday_stats, yesterday_separated_stats = calculate_separated_stats(yesterday_df)
    display_summary_tiles(yesterday_stats, label="Yesterday")
    display_separated_stats_tiles(yesterday_separated_stats, label="Yesterday")

    # Filter Section
    st.write("### Apply Filters to Transaction Inception Data")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        transaction_type = st.selectbox("Transaction Type", options=[None] + list(inception_df['transaction_type'].unique()), index=0)
    with col2:
        transaction_status = st.selectbox("Transaction Status", options=[None] + list(inception_df['transaction_status'].unique()), index=0)
    with col3:
        currency = st.selectbox("Currency", options=[None] + list(inception_df['currency'].unique()), index=0)
    with col4:
        start_date = st.date_input("From Date", min_value=inception_df['date'].min().date())
    with col5:
        end_date = st.date_input("To Date", max_value=inception_df['date'].max().date())

    # Check if filters are applied
    if st.button("Apply Filters"):
        filtered_df = apply_filters(inception_df, transaction_type, transaction_status, currency, start_date, end_date)
        filtered_stats, filtered_separated_stats = calculate_separated_stats(filtered_df)

        # Display filtered summary and separated stats as tiles
        st.write("### Filtered Transaction Metrics")
        display_summary_tiles(filtered_stats, label="Filtered")
        display_separated_stats_tiles(filtered_separated_stats, label="Filtered")

        # Add download button for filtered data
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Filtered Data as CSV",
            data=csv,
            file_name='filtered_transactions.csv',
            mime='text/csv',
            key='download-csv'
        )

# Run the transaction metrics
if __name__ == "__main__":
    display_transaction_metrics()
