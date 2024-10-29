import pandas as pd
import streamlit as st
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Function to load data from CSV files
def load_data():
    yesterday_df = pd.read_csv('transaction_yesterday.csv')
    inception_df = pd.read_csv('transaction_inception.csv')
    return yesterday_df, inception_df

# Function to calculate transaction statistics for each currency
def calculate_transaction_stats(df):
    # Amount and currency logic
    df['amount'] = df.apply(lambda row: row['bill_amt'] if pd.notnull(row['bill_amt']) else row['txn_amt'], axis=1)
    df['currency'] = df.apply(lambda row: row['bill_curr'] if pd.notnull(row['bill_curr']) else row['txn_curr'], axis=1)

    # Replace currency codes
    df['currency'] = df['currency'].replace({368: 'IQD', 840: 'USD'})

    # Calculate stats for IQD and USD separately
    stats = {}
    for currency in ['IQD', 'USD']:
        currency_df = df[df['currency'] == currency]
        total_count = currency_df.shape[0]
        accepted_count = currency_df[currency_df['transaction_status'] == 'Approved'].shape[0]
        rejected_count = currency_df[currency_df['transaction_status'] != 'Approved'].shape[0]
        approval_percentage = (accepted_count / total_count * 100) if total_count > 0 else 0

        accepted_amount = currency_df[currency_df['transaction_status'] == 'Approved']['amount'].sum()
        rejected_amount = currency_df[currency_df['transaction_status'] != 'Approved']['amount'].sum()

        stats[currency] = {
            'Total Transactions': total_count,
            'Accepted Transactions': accepted_count,
            'Rejected Transactions': rejected_count,
            'Approval Percentage': round(approval_percentage, 2),
            'Accepted Amount': accepted_amount,
            'Rejected Amount': rejected_amount
        }

    return stats

# Function to create HTML table with Streamlit-like styling
def create_html_table(stats, currency):
    table_html = f"""
    <style>
        .dataframe {{
            width: 100%;
            border: 1px solid #e0e0e0;
            border-collapse: collapse;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            font-size: 14px;
            line-height: 1.5;
        }}
        .dataframe th {{
            background-color: grey;
            border: 1px solid #e0e0e0;
            padding: 8px;
            text-align: left;
        }}
        .dataframe td {{
            border: 1px solid #e0e0e0;
            padding: 8px;
        }}
    </style>
    <table class="dataframe">
        <tr>
            <th>Metrics</th>
            <th>{currency}</th>
        </tr>
        <tr>
            <td>Total Transactions</td>
            <td>{stats['Total Transactions']}</td>
        </tr>
        <tr>
            <td>Accepted Transactions</td>
            <td>{stats['Accepted Transactions']}</td>
        </tr>
        <tr>
            <td>Rejected Transactions</td>
            <td>{stats['Rejected Transactions']}</td>
        </tr>
        <tr>
            <td>Approval Percentage</td>
            <td>{stats['Approval Percentage']}%</td>
        </tr>
        <tr>
            <td>Accepted Amount</td>
            <td>{stats['Accepted Amount']}</td>
        </tr>
        <tr>
            <td>Rejected Amount</td>
            <td>{stats['Rejected Amount']}</td>
        </tr>
    </table>
    """
    return table_html

# Function to create grouped data
def group_transaction_data(df):
    grouped_data = df.groupby(
        ['transaction_type','pos_entry_mode', 'CARD_PRESENT/CARD_NOT_PRESENT', 'transaction_status', 'eci', 'currency', 'networkname']
    ).size().reset_index(name='counts')
    return grouped_data

# Function to display pie charts for transaction status
def display_pie_chart(stats, title, key_suffix):
    labels = ['Approved', 'Declined']
    values_iqd = [stats['IQD']['Accepted Transactions'], stats['IQD']['Rejected Transactions']]
    values_usd = [stats['USD']['Accepted Transactions'], stats['USD']['Rejected Transactions']]

    # Create pie subplots
    fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'pie'}, {'type': 'pie'}]], subplot_titles=(f"{title} - IQD Transactions", f"{title} - USD Transactions"))

    fig.add_trace(go.Pie(labels=labels, values=values_iqd, name='IQD'), row=1, col=1)
    fig.add_trace(go.Pie(labels=labels, values=values_usd, name='USD'), row=1, col=2)

    st.plotly_chart(fig, key=f"pie_chart_{key_suffix}")

# Function to display transaction type pie chart
def display_transaction_type_pie_chart(grouped_data, title, key_suffix):
    # Group by transaction type
    transaction_type_counts = grouped_data['transaction_type'].value_counts()

    fig = go.Figure(data=[go.Pie(labels=transaction_type_counts.index, values=transaction_type_counts.values)])
    fig.update_layout(title=f"{title} - Transaction Type Distribution")
    st.plotly_chart(fig, key=f"type_pie_chart_{key_suffix}")

# Main function to display transaction metrics
def display_transaction_metrics():
    # Load the data
    yesterday_df, inception_df = load_data()

    # Calculate statistics for Yesterday and Inception
    yesterday_stats = calculate_transaction_stats(yesterday_df)
    inception_stats = calculate_transaction_stats(inception_df)

    # Create grouped data
    inception_grouped_data = group_transaction_data(inception_df)
    yesterday_grouped_data = group_transaction_data(yesterday_df)

    # Display transaction summaries for Inception
    st.write("### Transaction Summary (Inception)")
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.write("#### IQD Transactions (Inception)")
        st.markdown(create_html_table(inception_stats['IQD'], 'IQD'), unsafe_allow_html=True)
    
    with col2:
        display_pie_chart(inception_stats, "Inception", key_suffix="inception")

    with col3:
        st.write("#### USD Transactions (Inception)")
        st.markdown(create_html_table(inception_stats['USD'], 'USD'), unsafe_allow_html=True)

    # Display transaction summaries for Yesterday
    st.write("### Transaction Summary (Yesterday)")
    col4, col5, col6 = st.columns([1, 1, 1])

    with col4:
        st.write("#### IQD Transactions (Yesterday)")
        st.markdown(create_html_table(yesterday_stats['IQD'], 'IQD'), unsafe_allow_html=True)
    
    with col5:
        display_pie_chart(yesterday_stats, "Yesterday", key_suffix="yesterday")
    
    with col6:
        st.write("#### USD Transactions (Yesterday)")
        st.markdown(create_html_table(yesterday_stats['USD'], 'USD'), unsafe_allow_html=True)
        
    # Display transaction type distribution summaries for Yesterday and Inception
    st.write("### Transaction Details")
    
    col7, col8 = st.columns(2)

    with col7:
        st.write("#### Inception Transaction Type Summary")
        st.dataframe(inception_grouped_data)  # Use st.table to display Inception data
    
    with col8:
        st.write("#### Yesterday Transaction Type Summary")
        st.dataframe(yesterday_grouped_data)  # Use st.table to display Yesterday data
        
            # Display transaction type distribution charts
    st.write("### Transaction Type Distribution")
    col9, col10 = st.columns(2)

    with col9:
        st.write("#### Inception")
        display_transaction_type_pie_chart(inception_df, "Inception", key_suffix="inception_type")

    with col10:
        st.write("#### Yesterday")
        display_transaction_type_pie_chart(yesterday_df, "Yesterday", key_suffix="yesterday_type")

# Run the transaction metrics
if __name__ == "__main__":
    display_transaction_metrics()
