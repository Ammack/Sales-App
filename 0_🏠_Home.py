import streamlit as st

st.set_page_config(
    page_title="Sales Analysis",
    page_icon="📈",
    layout="wide"
)

hide_streamlit_style = """
            <style>
            .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob,
            .styles_viewerBadge_1yB5, .viewerBadge_link__1S137,
            .viewerBadge_text__1JaDK {display: none;}
            MainMenu {visibility: hidden;}
            header { visibility: hidden; }
            footer {visibility: hidden;}
            #GithubIcon {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

import pandas as pd
from io import BytesIO
from streamlit import session_state
from PIL import Image
import requests


st.write("# Sales Analysis App")

# URL of the image
image_url = "https://www.lystloc.com/blog/wp-content/uploads/2023/05/What-Is-Sales-Data-Importance-And-Types-Of-Sales-Data-Reports-.webp"

response = requests.get(image_url)
image = Image.open(BytesIO(response.content))



para = """
Welcome to the Sales Analysis App your go-to tool for gaining valuable insights into your sales data! Whether you're a business owner, sales manager, or analyst, this app empowers you to make informed decisions, optimize strategies, and drive business growth.
"""
st.write(para)
st.write("")

st.image(image,width=500)

para = """
Key Features:
1. Data Upload:
Effortlessly upload your sales data in CSV format using the sidebar.

2. Data Insights:
Explore the fundamental aspects of your sales data and a sneak peek of the uploaded information. This app is designed to give you a snapshot of your data, setting the stage for deeper analysis.

3. Sales Visualization:
Visualize your sales data dynamically with interactive plots. The app utilizes Plotly Express to create engaging visualizations, allowing you to compare predictions and actual sales over time. Dive into trends, patterns, and performance metrics effortlessly.

4. Sales Forecast:
Beyond the provided features, this app also allows you to forecast sales for the upcoming months. The app utilizes the SARIMAX model to predict future sales based on historical data. The model is trained on the uploaded data and can be used to forecast sales for the next 12 months."""

st.write(para)
st.subheader("",divider=True)

st.write("Suggested formats of the CSV file:")

sample_df = {
    'date': ['2013-01-01', '2014-05-12', '2016-12-23', '2013-09-04', '2015-07-20', '2016-11-16'],
    'item': [1, 2, 4, 25, 49, 15],
    'store': [1, 5, 10, 4, 8, 6],
    'sales': [13, 11, 14, 13, 10, 12]
}

sample_df2 = {
    'date': ['2013-01-01', '2014-05-12', '2016-12-23', '2013-09-04', '2015-07-20', '2016-11-16'],
    'item': [1, 2, 4, 25, 49, 15],
    'sales': [13, 11, 14, 13, 10, 12]
}

sample_df = pd.DataFrame(sample_df)
sample_df2 = pd.DataFrame(sample_df2)

col1, col2 = st.columns(2)

col1.dataframe(sample_df)
col2.dataframe(sample_df2)


st.sidebar.header("Upload Data")


if 'uploaded_file' not in session_state:
    session_state['uploaded_file'] = None


if session_state['uploaded_file'] is None:
    file = st.sidebar.file_uploader("Choose a CSV file", type="csv")
    session_state['uploaded_file'] = file
 
else:
    file = session_state['uploaded_file']

if file is not None:
    st.sidebar.success("Uploaded")
    df = pd.read_csv(BytesIO(file.getvalue()))
    if st.checkbox("Display uploaded data"):
        st.dataframe(df)
    

