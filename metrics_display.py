import pandas as pd
import streamlit as st

# Function to read CSV files
def read_csv_file(file_path):
    return pd.read_csv(file_path)

# Function to log messages to the browser console
def display_to_browser_console(message):
    js_code = f"""
    <script>
        console.log("{message}");
    </script>
    """
    st.components.v1.html(js_code, height=0)


# Function to display metrics for cardholders and cards
def display_metrics():
    # Reading data from the files
    df_cardholder = read_csv_file('./cardholder_inception.csv')
    df_yesterday_cardholder = read_csv_file('./cardholder_yesterday.csv')
    df_card = read_csv_file('./card_inception.csv')
    df_yesterday_card = read_csv_file('./card_yesterday.csv')

    ### Cardholder Metrics ###
    status_counts_cardholder = {
        row["status"]: row["count"]
        for index, row in df_cardholder.iterrows()
    }

    total_cardholder_count = sum(status_counts_cardholder.values())



    # Color class mapping for current cardholder stats
    color_class_map_cardholder = {
        'ACTIVE': '#669966',             
        'INACTIVE': 'rgb(199 65 56)',           
        'PENDINGID VERIFICATION': '#6699cc',  
        'Suspended': '#cc9933',          
        'TERMINATED': 'rgb(67 178 173)',         
        'PENDING KYC': '#27408b',         
        'Total': 'rgb(53 141 114)',               
        'Activated': '#669966',
        'Inactive': 'rgb(199 65 56)',
        'Pending IDV/Created': '#6699cc',
        'Pending KYC': '#4692A4',
        'Terminated': 'rgb(67 178 173)',
        'Created': '#2199D4',
    }

    # Define the desired order of statuses
    ordered_statuses = ['Pending KYC', 'Pending IDV/Created', 'Inactive', 'Activated', 'Suspended', 'Terminated']

    # Yesterday's data initialization
    count_dict = {
        "Pending KYC": 0,
        "Pending IDV/Created": 0,
        "Active": 0,
        "Inactive": 0,
        "Suspended": 0,
        "Terminated": 0,
        
    }

    # Iterate through yesterday's data
    for index, row in df_yesterday_cardholder.iterrows():
        operation_newstate = row["newstate"] if pd.notna(row["newstate"]) else row["operation"]
        if operation_newstate in count_dict:
            count_dict[operation_newstate] += row["count"]
        else:
            count_dict[operation_newstate] = row["count"]

    # Log yesterday's counts in the console
    display_to_browser_console(f"'Yesterday Cardholder Counts: {count_dict}'")

    # Streamlit layout for cardholder metrics
    st.subheader("Cardholder Onboarding Summary")
    st.markdown("<hr>", unsafe_allow_html=True)

    # Display Overall Status
    st.write("### Overall Status")
    cols_cardholder = st.columns(len(ordered_statuses) + 1)  # +1 for total

    # Display cardholder stats
    for i, status in enumerate(ordered_statuses):
        count = status_counts_cardholder.get(status, 0)
        with cols_cardholder[i]:
            st.markdown(f"<div style='height: 120px; padding: 20px; background-color: {color_class_map_cardholder.get(status, '#4d4d4d')}; border-radius: 8px; text-align: center; color: #fff; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);'>"
                        f"<h6>{status}</h6><h3>{count}</h3></div>", unsafe_allow_html=True)

    # Display total cardholders
    with cols_cardholder[-1]:
        st.markdown(f"<div style='height: 120px; padding: 20px; background-color: {color_class_map_cardholder['Total']}; border-radius: 8px; text-align: center; color: #fff; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);'>"
                    f"<h5>Total</h6><h3>{total_cardholder_count}</h6></div>", unsafe_allow_html=True)

    # Display yesterday's status
    st.write("### Yesterday's Status")
    cols_yesterday_cardholder = st.columns(len(ordered_statuses) + 1)

    for i, status in enumerate(ordered_statuses):
        count = count_dict.get(status, 0)
        with cols_yesterday_cardholder[i]:
            st.markdown(f"<div style='height: 120px; padding: 20px; background-color: {color_class_map_cardholder.get(status, '#4d4d4d')}; border-radius: 8px; text-align: center; color: #fff; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);'>"
                        f"<h6>{status}</h6><h3>{count}</h3></div>", unsafe_allow_html=True)

    total_yesterday_cardholder_count = sum(count_dict.values())
    with cols_yesterday_cardholder[-1]:
        st.markdown(f"<div style='height: 120px; padding: 20px; background-color: {color_class_map_cardholder['Total']}; border-radius: 8px; text-align: center; color: #fff; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);'>"
                    f"<h6>Total</h6><h3>{total_yesterday_cardholder_count}</h3></div>", unsafe_allow_html=True)

 ### Card Metrics ###

    # Define the desired order of card statuses
    card_ordered_statuses = ['Created', 'Inactive', 'Activated', 'Suspended', 'Terminated']

    # Read card data and create a dictionary of status counts for overall metrics
    status_counts_card = {
        row["status"]: row["count"]
        for index, row in df_card.iterrows()
    }
    total_card_count = sum(status_counts_card.values())

    # Log card metrics in the console
    display_to_browser_console(f"'Status Counts Card: {status_counts_card}'")
    display_to_browser_console(f"'Total Card Count: {total_card_count}'")

    # Streamlit layout for card metrics
    st.subheader("Card Summary")
    st.write("### Overall Status")
    cols_card = st.columns(len(card_ordered_statuses) + 1)  # +1 for total

    # Display card stats in the specified order
    for i, status in enumerate(card_ordered_statuses):
        count = status_counts_card.get(status, 0)
        with cols_card[i]:
            st.markdown(
                f"<div style='height: 120px; padding: 20px; background-color: {color_class_map_cardholder.get(status, '#99CC99')}; border-radius: 8px; text-align: center; color: #fff; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);'>"
                f"<h5>{status.capitalize()}</h5><h3>{count}</h3></div>",
                unsafe_allow_html=True,
            )

    # Display total cards
    with cols_card[-1]:
        st.markdown(
            f"<div style='height: 120px; padding: 20px; background-color: {color_class_map_cardholder['Total']}; border-radius: 8px; text-align: center; color: #fff; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);'>"
            f"<h5>Total Cards</h5><h3>{total_card_count}</h3></div>",
            unsafe_allow_html=True,
        )

    # Yesterday's card metrics initialization
    count_dict_yesterday_card = {status: 0 for status in card_ordered_statuses}

    # Iterate through yesterday's data for cards
    for index, row in df_yesterday_card.iterrows():
        operation_newstate = row["newstate"] if pd.notna(row["newstate"]) else row["operation"]
        if operation_newstate in count_dict_yesterday_card:
            count_dict_yesterday_card[operation_newstate] += row["count"]
        else:
            count_dict_yesterday_card[operation_newstate] = row["count"]

    # Log yesterday's card counts in the console
    display_to_browser_console(f"'Yesterday Card Counts: {count_dict_yesterday_card}'")

    # Display yesterday's card status
    st.write("### Yesterday's Status")
    cols_yesterday_card = st.columns(len(card_ordered_statuses) + 1)

    for i, status in enumerate(card_ordered_statuses):
        count = count_dict_yesterday_card.get(status, 0)
        with cols_yesterday_card[i]:
            st.markdown(
                f"<div style='height: 120px; padding: 20px; background-color: {color_class_map_cardholder.get(status, '#99CC99')}; border-radius: 8px; text-align: center; color: #fff; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);'>"
                f"<h5>{status.capitalize()}</h5><h3>{count}</h3></div>",
                unsafe_allow_html=True,
            )

    # Display total cards for yesterday
    total_yesterday_card_count = sum(count_dict_yesterday_card.values())
    with cols_yesterday_card[-1]:
        st.markdown(
            f"<div style='height: 120px; padding: 20px; background-color: {color_class_map_cardholder['Total']}; border-radius: 8px; text-align: center; color: #fff; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);'>"
            f"<h5>Total Cards</h5><h3>{total_yesterday_card_count}</h3></div>",
            unsafe_allow_html=True,
        )    # Display message in browser console
    display_to_browser_console(f"'Status Counts Cardholder: {status_counts_cardholder}'")
    display_to_browser_console(f"'Total Cardholder Count: {total_cardholder_count}'")
# Call the function to display metrics
display_metrics()
