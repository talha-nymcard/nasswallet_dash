import streamlit as st
from metrics_display import display_metrics
from banking_metrics import display_transaction_metrics  # Import transaction metrics
# Set page configuration
st.set_page_config(page_title="Nasswallet Dashboard", layout="wide")
# Inject JavaScript to force dark theme
dark_theme_js = """
<script>
    const setDarkMode = () => {
        document.documentElement.setAttribute('data-theme', 'dark');
    };
    window.addEventListener('load', setDarkMode);
</script>
"""
# Inject the CSS and JavaScript into the Streamlit app

st.markdown(dark_theme_js, unsafe_allow_html=True)
# Set page configuration


# Title of the application
st.title("Nasswallet Dashboard")

# Create columns to display Cardholder and Card metrics side by side
#col1, col2 = st.columns(2)

#with col1:
 #   display_cardholder_metrics()  # Call the function to display cardholder metrics

#with col2:
 #   display_card_metrics()  # Call the function to display card metrics

# Call the display_metrics function to show the cardholder and card metrics
display_metrics()
# This one looks good on bigger screen but the text alignment isn't ok for smaller screensize.
#display_metrics1()
# Create a new row for Transaction Metrics
st.markdown("<br>", unsafe_allow_html=True)
st.subheader("Transaction Summary")
st.markdown("<hr>", unsafe_allow_html=True)
#display_transaction_metrics()  # Call the function to display transaction metrics
display_transaction_metrics()
