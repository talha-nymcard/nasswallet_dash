import pandas as pd
import streamlit as st
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Function to load data from CSV files
def load_data():
    yesterday_df = pd.read_csv('transaction_yesterday.csv')
    inception_df = pd.read_csv('transaction_inception.csv')
    return yesterday_df, inception_df

# Function to calculate transaction statistics
def calculate_transaction_stats(df):
    # Amount and currency logic
    df['amount'] = df.apply(lambda row: row['bill_amt'] if pd.notnull(row['bill_amt']) else row['txn_amt'], axis=1)
    df['currency'] = df.apply(lambda row: row['bill_curr'] if pd.notnull(row['bill_curr']) else row['txn_curr'], axis=1)

    # Replace currency codes
    df['currency'] = df['currency'].replace({368: 'IQD', 840: 'USD'})

    total_count = df.shape[0]
    accepted_count = df[df['transaction_status'] == 'Approved'].shape[0]
    rejected_count = df[df['transaction_status'] == 'Declined'].shape[0]
    
    approval_percentage = (accepted_count / total_count * 100) if total_count > 0 else 0

    # Group by transaction_type, status, currency, and network_type
    grouped = df.groupby(['transaction_type', 'transaction_status', 'currency', 'networkname']).agg(
        total_amount=('amount', 'sum'),
        transaction_count=('transaction_type', 'count')
    ).reset_index()

    # Calculate currency-specific amounts
    accepted_iqd_amount = grouped[(grouped['transaction_status'] == 'Approved') & (grouped['currency'] == 'IQD')]['total_amount'].sum()
    accepted_usd_amount = grouped[(grouped['transaction_status'] == 'Approved') & (grouped['currency'] == 'USD')]['total_amount'].sum()
    rejected_iqd_amount = grouped[(grouped['transaction_status'] == 'Declined') & (grouped['currency'] == 'IQD')]['total_amount'].sum()
    rejected_usd_amount = grouped[(grouped['transaction_status'] == 'Declined') & (grouped['currency'] == 'USD')]['total_amount'].sum()

    return {
        'Total Transactions': total_count,
        'Accepted Transactions IQD': accepted_count,
        'Accepted Transactions USD': accepted_count,
        'Rejected Transactions IQD': rejected_count,
        'Rejected Transactions USD': rejected_count,
        'Approval Percentage': round(approval_percentage, 2),  # Round to 2 decimal points
        'Accepted Amount IQD': accepted_iqd_amount,
        'Accepted Amount USD': accepted_usd_amount,
        'Rejected Amount IQD': rejected_iqd_amount,
        'Rejected Amount USD': rejected_usd_amount,
        'Grouped Data': grouped  # Ensure this is returned
    }

# Function to create summary DataFrame for a single currency
def create_currency_summary_df(stats, currency):
    return pd.DataFrame({
        'Metrics': [
            'Total Transactions', 
            'Accepted Transactions',
            'Rejected Transactions',
            'Approval Percentage',
            'Accepted Amount', 
            'Rejected Amount'
        ],
        currency: [
            stats['Total Transactions'],
            stats[f'Accepted Transactions {currency}'],
            stats[f'Rejected Transactions {currency}'],
            f"{stats['Approval Percentage']:.2f}%",  # Format percentage with 2 decimal points
            stats[f'Accepted Amount {currency}'],
            stats[f'Rejected Amount {currency}'],
        ]
    })

# Function to display detailed transaction summaries
def display_transaction_summaries(title, grouped_data):
    st.write(grouped_data)  # Use st.write to remove serial numbers

# Function to display pie charts for transaction status
def display_pie_chart(stats, title, key_suffix):
    labels = ['Approved', 'Declined']
    values_iqd = [stats['Accepted Transactions IQD'], stats['Rejected Transactions IQD']]
    values_usd = [stats['Accepted Transactions USD'], stats['Rejected Transactions USD']]

    # Create pie subplots
    fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'pie'}, {'type': 'pie'}]], subplot_titles=(f"{title} - IQD Transactions", f"{title} - USD Transactions"))

    fig.add_trace(go.Pie(labels=labels, values=values_iqd, name='IQD'), row=1, col=1)
    fig.add_trace(go.Pie(labels=labels, values=values_usd, name='USD'), row=1, col=2)

    st.plotly_chart(fig, key=f"pie_chart_{key_suffix}")

# Function to display pie chart based on transaction types
def display_transaction_type_pie_chart(grouped_data, title, key_suffix):
    # Group by transaction type
    transaction_type_counts = grouped_data['transaction_type'].value_counts()

    fig = go.Figure(data=[go.Pie(labels=transaction_type_counts.index, values=transaction_type_counts.values)])
    fig.update_layout(title=f"{title} - Transaction Type Distribution")
    st.plotly_chart(fig, key=f"type_pie_chart_{key_suffix}")

# Function to display comparison bar chart between IQD and USD transactions
def display_comparison_bar_chart(yesterday_stats):
    labels = ['Accepted Transactions', 'Rejected Transactions', 'Total Transactions']
    iqd_values = [
        yesterday_stats['Accepted Transactions IQD'],
        yesterday_stats['Rejected Transactions IQD'],
        yesterday_stats['Total Transactions']
    ]
    usd_values = [
        yesterday_stats['Accepted Transactions USD'],
        yesterday_stats['Rejected Transactions USD'],
        yesterday_stats['Total Transactions']
    ]

    fig = go.Figure(data=[
        go.Bar(name='IQD', x=labels, y=iqd_values),
        go.Bar(name='USD', x=labels, y=usd_values)
    ])
    fig.update_layout(barmode='group', title='Transaction Comparison: IQD vs USD')
    
    st.plotly_chart(fig, key="comparison_bar_chart")

# Main function to display transaction metrics
def display_transaction_metrics():
    # Load the data
    yesterday_df, inception_df = load_data()

    # Calculate statistics
    yesterday_stats = calculate_transaction_stats(yesterday_df)
    inception_stats = calculate_transaction_stats(inception_df)

    # Create summary DataFrames for IQD and USD
    yesterday_iqd_summary = create_currency_summary_df(yesterday_stats, 'IQD')
    yesterday_usd_summary = create_currency_summary_df(yesterday_stats, 'USD')
    inception_iqd_summary = create_currency_summary_df(inception_stats, 'IQD')
    inception_usd_summary = create_currency_summary_df(inception_stats, 'USD')

    # Display summaries for Inception and Yesterday in a 4-column layout
    col1, col2, col3 = st.columns(3)
    
    # IQD and USD summaries (Inception)
    with col1:
        st.write("#### IQD Transactions (Inception)")
        st.dataframe(inception_iqd_summary, use_container_width=True)  # Use st.dataframe to avoid serial numbers
    
    with col2:
        display_pie_chart(inception_stats, "Inception", key_suffix="inception")
    
    with col3:
        st.write("#### USD Transactions (Inception)")
        st.dataframe(inception_usd_summary, use_container_width=True)  # Use st.dataframe to avoid serial numbers

    # Display summaries for Yesterday
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.write("#### IQD Transactions (Yesterday)")
        st.dataframe(yesterday_iqd_summary, use_container_width=True)  # Use st.dataframe to avoid serial numbers
    with col5:
        display_pie_chart(yesterday_stats, "Yesterday", key_suffix="yesterday")        

    with col6:
        st.write("#### USD Transactions (Yesterday)")
        st.dataframe(yesterday_usd_summary, use_container_width=True)  # Use st.dataframe to avoid serial numbers

    # Display transaction type distribution charts for Yesterday and Inception side by side
    st.write("### Transaction Type Distribution")
    col7, col8 = st.columns(2)
    
    with col7:
        st.write("#### Inception")
        display_transaction_type_pie_chart(inception_stats['Grouped Data'], "Inception", key_suffix="inception_type")
    
    with col8:
        st.write("#### Yesterday")
        display_transaction_type_pie_chart(yesterday_stats['Grouped Data'], "Yesterday", key_suffix="yesterday_type")

# Run the transaction metrics
if __name__ == "__main__":
    display_transaction_metrics()  # Call the function to display transaction metrics
