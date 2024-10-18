import pandas as pd
import streamlit as st

# Function to read CSV files
def read_csv_file(file_path):
    return pd.read_csv(file_path)

# Function to display metrics for cardholders and cards
def display_metrics():
    # Reading data from the files
    df_cardholder = read_csv_file('./cardholder_inception.csv')
    df_yesterday_cardholder = read_csv_file('./cardholder_yesterday.csv')
    df_card = read_csv_file('./card_inception.csv')
    df_yesterday_card = read_csv_file('./card_yesterday.csv')

    ### Cardholder Metrics ###
    # Status counts for cardholder inception
    status_counts_cardholder = df_cardholder.set_index('status')['count'].to_dict()
    total_cardholder_count = sum(status_counts_cardholder.values())

    # Color class mapping for current cardholder stats
    color_class_map_cardholder = {
        'ACTIVE': '#99CC99',
        'INACTIVE': '#808080',
        'PENDINGIDVERIFICATION': '#A7C7E7',
        'SUSPENDED': '#ffcc66',
        'TERMINATED': '#c0392b',
        'PENDINGKYC': '#4169E1',
        'total': '#001F3F'
    }

    # Define color class mapping for yesterday's cardholder stats
    yesterday_color_class_map_cardholder = {
        0: '#28a745',
        1: '#4682B4',
        2: '#007bff',
        3: '#ff7f50',
        4: '#dc3545',
        5: '#6f42c1',
    }

    # Extract yesterday's data for cardholders
    yesterday_cardholder_counts = [
        {
            "operation_newstate": row["newstate"].capitalize() if pd.notna(row["newstate"]) else row["operation"].capitalize(),
            "count": row["count"]
        }
        for index, row in df_yesterday_cardholder.iterrows()
    ]

    # Streamlit layout for cardholder metrics
    st.subheader("Cardholder Onboarding Summary")

    # Current Cardholder Status
    st.write("### Current Cardholder Status")
    cols_cardholder = st.columns(len(status_counts_cardholder) + 1)  # +1 for total

    for i, (status, count) in enumerate(status_counts_cardholder.items()):
        with cols_cardholder[i]:
            st.markdown(f"<div style='height: 120px; padding: 20px; background-color: {color_class_map_cardholder[status]}; border-radius: 8px; text-align: center; color: #fff; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);'>"
                        f"<p style='margin: 0; font-weight: bold;'>{status.capitalize()}</p><h3 style='margin: 0;'>{count}</h3></div>", unsafe_allow_html=True)

    with cols_cardholder[-1]:  # Total
        st.markdown(f"<div style='height: 120px; padding: 20px; background-color: {color_class_map_cardholder['total']}; border-radius: 8px; text-align: center; color: #fff; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);'>"
                    f"<p style='margin: 0; font-weight: bold;'>Total Cardholders</p><h3 style='margin: 0;'>{total_cardholder_count}</h3></div>", unsafe_allow_html=True)

    # Counts for Yesterday
    st.write("### Counts for Yesterday")
    cols_yesterday_cardholder = st.columns(len(yesterday_cardholder_counts) + 1)  # +1 for total
    yesterday_total_cardholder = df_yesterday_cardholder['count'].sum()

    for i, item in enumerate(yesterday_cardholder_counts):
        with cols_yesterday_cardholder[i]:
            st.markdown(f"<div style='height: 120px; padding: 20px; background-color: {yesterday_color_class_map_cardholder[i % len(yesterday_color_class_map_cardholder)]}; border-radius: 8px; text-align: center; color: #fff; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);'>"
                        f"<p style='margin: 0; font-weight: bold;'>{item['operation_newstate']}</p><h3 style='margin: 0;'>{item['count']}</h3></div>", unsafe_allow_html=True)

    with cols_yesterday_cardholder[-1]:  # Total
        st.markdown(f"<div style='height: 120px; padding: 20px; background-color: {color_class_map_cardholder['total']}; border-radius: 8px; text-align: center; color: #fff; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);'>"
                    f"<p style='margin: 0; font-weight: bold;'>Total Cardholders Yesterday</p><h3 style='margin: 0;'>{yesterday_total_cardholder}</h3></div>", unsafe_allow_html=True)

    ### Card Metrics ###
    # Status counts for card inception
    status_counts_card = df_card.set_index('status')['count'].to_dict()
    total_card_count = sum(status_counts_card.values())

    # Color class mapping for current card stats
    color_class_map_card = {
        'ACTIVE': '#99CC99',
        'SUSPENDED': '#ffcc66',
        'TERMINATED': '#c0392b',
        'PENDINGIDVERIFICATION': '#FFD009',
        'total': '#001F3F'
    }

    # Define color class mapping for yesterday's stats
    yesterday_color_class_map_card = {
        0: '#28a745',  # Green
        1: '#FFD700',  # Gold
        2: '#007bff',  # Blue
        3: '#ff7f50',  # Orange
        4: '#dc3545',  # Red
        5: '#6f42c1',  # Purple
    }

    # Extract yesterday's data for cards
    yesterday_card_counts = [
        {
            "operation_newstate": row['operation'].capitalize(),
            "count": row["count"]
        }
        for index, row in df_yesterday_card.iterrows()
    ]

    # Streamlit layout for card metrics
    st.subheader("Card Summary")
    
    # Current Card Status
    st.write("### Current Card Status")
    cols_card = st.columns(len(status_counts_card) + 1)  # +1 for total

    for i, (status, count) in enumerate(status_counts_card.items()):
        with cols_card[i]:
            st.markdown(f"<div style='height: 120px; padding: 20px; background-color: {color_class_map_card.get(status, '#99CC99')}; border-radius: 8px; text-align: center; color: #fff; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);'>"
                        f"<p style='margin: 0; font-weight: bold;'>{status.capitalize()}</p><h3 style='margin: 0;'>{count}</h3></div>", unsafe_allow_html=True)

    with cols_card[-1]:  # Total
        st.markdown(f"<div style='height: 120px; padding: 20px; background-color: {color_class_map_card['total']}; border-radius: 8px; text-align: center; color: #fff; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);'>"
                    f"<p style='margin: 0; font-weight: bold;'>Total Cards</p><h3 style='margin: 0;'>{total_card_count}</h3></div>", unsafe_allow_html=True)

    # Counts for Yesterday
    st.write("### Counts for Yesterday")
    cols_yesterday_card = st.columns(len(yesterday_card_counts) + 1)  # +1 for total

    for i, item in enumerate(yesterday_card_counts):
        with cols_yesterday_card[i]:
            st.markdown(f"<div style='height: 120px; padding: 20px; background-color: {yesterday_color_class_map_card[i % len(yesterday_color_class_map_card)]}; border-radius: 8px; text-align: center; color: #fff; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);'>"
                        f"<p style='margin: 0; font-weight: bold;'>{item['operation_newstate']}</p><h3 style='margin: 0;'>{item['count']}</h3></div>", unsafe_allow_html=True)

    with cols_yesterday_card[-1]:  # Total
        st.markdown(f"<div style='height: 120px; padding: 20px; background-color: {color_class_map_card['total']}; border-radius: 8px; text-align: center; color: #fff; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);'>"
                    f"<p style='margin: 0; font-weight: bold;'>Total Cards Yesterday</p><h3 style='margin: 0;'>{df_yesterday_card['count'].sum()}</h3></div>", unsafe_allow_html=True)

# Run the display function
display_metrics()
