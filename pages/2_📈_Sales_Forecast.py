import streamlit as st

st.set_page_config(
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
import numpy as np
from io import BytesIO
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from statsmodels.tsa.seasonal import seasonal_decompose


from statsmodels.tsa.statespace.sarimax import SARIMAX
import plotly.express as px


st.title("Sales Forecast")

st.sidebar.header("Upload Data")

if 'uploaded_file' not in st.session_state:
    st.session_state['uploaded_file'] = None

if st.session_state['uploaded_file'] is None:

    uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")
    st.session_state['uploaded_file'] = uploaded_file

else:
    uploaded_file = st.session_state['uploaded_file']

if uploaded_file is None:
    st.write("Upload a CSV file to get started.")
    if st.checkbox("See Sample CSV files"):
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



if uploaded_file is not None:
    st.sidebar.success("Uploaded")
    df = pd.read_csv(BytesIO(uploaded_file.getvalue()))
    if st.checkbox("Display uploaded data"):
        st.dataframe(df)


    df['date'] = pd.to_datetime(df.date, format="%Y-%m-%d")
    df = df.set_index('date',drop=True)


    sales_by_item_date = df.pivot_table(index='date', columns='item', values='sales', aggfunc='sum')
    sales_by_item_date = pd.DataFrame(sales_by_item_date)

    forecast_frequency = st.selectbox('Select forecast frequency', ['Monthly', 'Weekly'])

    if forecast_frequency == 'Monthly':
        
        net_monthly_sales = sales_by_item_date.resample('M').sum()

        last_year = net_monthly_sales.index[-1].year
        train_data_monthly = net_monthly_sales[:str(last_year - 1)]
        test_data_monthly = net_monthly_sales[str(last_year):]

        
        i = st.number_input("Select item number", min_value=1, step=1, format="%i")
        i-=1


        model_monthly = SARIMAX(train_data_monthly.iloc[:,i],order = (1, 0, 0),seasonal_order =(0, 1, 0, 12))

        result_monthly = model_monthly.fit()

        start = len(train_data_monthly)
        end = len(train_data_monthly) + len(test_data_monthly) - 1

        # Predictions for one-year against the test set
        predictions = result_monthly.predict(start, end,
                                    typ = 'levels').rename("Predictions")

        trace1 = go.Scatter(
            x=predictions.index.strftime('%b'),
            y=predictions,
            mode='lines',
            name='Predictions'
        )

        trace2 = go.Scatter(
            x=test_data_monthly.iloc[:,i].index.strftime('%b'),
            y=test_data_monthly.iloc[:,i],
            mode='lines',
            name='Actual Sales'
        )

        layout = go.Layout(
            title='Prediction for Year '+str(last_year),
            height=600,
            width=1000
        )

        # Combining traces and layout into a figure
        fig = go.Figure(data=[trace1, trace2], layout=layout)
        st.plotly_chart(fig)

        mape = np.mean((np.abs(test_data_monthly.iloc[:,i] - predictions)) / test_data_monthly.iloc[:,i]) * 100
        # print("MAPE:",mape)
        st.text("Mean Absolute Percentage Error: "+str(np.round(mape,2))+"%")
    
    elif forecast_frequency == 'Weekly':
        net_weekly_sales = sales_by_item_date.resample('W').sum()
        
        last_year = net_weekly_sales.index[-1].year

        train_data_weekly = net_weekly_sales[:str(last_year - 1)]
        test_data_weekly = net_weekly_sales[str(last_year):]

        i = st.number_input("Select item number", min_value=1, step=1, format="%i")
        i-=1

        model_weekly = SARIMAX(train_data_weekly.iloc[:,i],
                order = (3, 1, 0),
                seasonal_order =(1, 0, 1, 52))
        
        result_weekly = model_weekly.fit()

        start = len(train_data_weekly)
        end = len(train_data_weekly) + len(test_data_weekly) - 1

        # Predictions for one-year against the test set
        predictions = result_weekly.predict(start, end,
                                    typ = 'levels').rename("Predictions")
        
        #line for predictions
        trace1 = go.Scatter(
            x=predictions.index,
            y=predictions,
            mode='lines',
            name='Predictions'
        )

        #line for actual sales
        trace2 = go.Scatter(
            x=test_data_weekly.iloc[:,i].index,
            y=test_data_weekly.iloc[:,i],
            mode='lines',
            name='Actual Sales'
        )

        layout = go.Layout(
            title='Prediction for Year '+str(last_year),
            height=600,
            width=1000
        )

        fig = go.Figure(data=[trace1, trace2], layout=layout)
        st.plotly_chart(fig)

        mape = np.mean((np.abs(test_data_weekly.iloc[:,i] - predictions)) / test_data_weekly.iloc[:,i]) * 100
        # print("MAPE:",mape)
        st.text("Mean Absolute Percentage Error: "+str(np.round(mape,2))+"%")
    
    st.subheader("",divider=True)

    net_monthly_sales = sales_by_item_date[1].resample('M').sum()

    decomposition = seasonal_decompose(net_monthly_sales, model='additive')


    # Extracting the trend, seasonality, and irregularity components
    trend = decomposition.trend
    seasonality = decomposition.seasonal
    residuals = decomposition.resid


    fig = make_subplots(rows=3, cols=1)

    # Original Sales
    fig.add_trace(go.Scatter(x=net_monthly_sales.index, y=net_monthly_sales, mode='lines', name='Original Sales'),row=1,col=1)

    # Trend
    fig.add_trace(go.Scatter(x=trend.index, y=trend, mode='lines', name='Trend'),row=2,col=1)

    # Seasonality
    fig.add_trace(go.Scatter(x=seasonality.index, y=seasonality, mode='lines', name='Seasonality'),row=3,col=1)

    # Layout
    fig.update_layout(title='Decomposition of Monthly Sales',
                    xaxis_title='Date',
                    yaxis_title='Sales',
                    height=1000,
                    width=1000)

    st.plotly_chart(fig)