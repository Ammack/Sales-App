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
import plotly.express as px


st.title("Visualization")

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

    df['day'] = df.date.dt.day.astype(int)

    df['month'] = df.date.dt.month.astype(int)

    df['year'] = df.date.dt.year.astype(int)

    df['day_of_week'] = df.date.dt.dayofweek.astype(int)  # Mon:0, Sun: 6

    df['week_of_month'] = (df.date.dt.isocalendar().week.astype(int) - 1) % 4 # 0 to 4

    df['quarter'] = df.date.dt.quarter.astype(int) # 1 to 4



    df_avg_sales = df.groupby(['year', 'month'])['sales'].sum().reset_index()

    fig = px.line(df_avg_sales, x='month', y='sales', color='year', title='Monthly Sales Over the Years')

    fig.update_layout(
        xaxis=dict(title='Month'),
        yaxis=dict(title='Total Sales'),
        legend=dict(title='Year'),
        width=1000,
        height=600
    )

    st.plotly_chart(fig)
    st.subheader("",divider=True)

    # Getting mean sales for each day of the week
    mean_sales_by_day = df.groupby('day_of_week')['sales'].mean()
    
    day_names = {6: "Sunday", 5: "Saturday", 4: "Friday",3: "Thursday", 2: "Wednesday", 1: "Tuesday", 0: "Monday"}

    mean_sales_by_day.index = mean_sales_by_day.index.map(day_names)

    #Top 3 day_of_week with the highest mean sales
    top_3_days = mean_sales_by_day.nlargest(3)


    st.header("Most Selling Days")
    st.markdown(f"#### - {top_3_days.index[0]}")
    st.markdown(f"#### - {top_3_days.index[1]}")
    st.markdown(f"#### - {top_3_days.index[2]}")

    fig = px.bar(x=mean_sales_by_day.index, y=mean_sales_by_day.values)

    fig.update_layout(
        title='Mean Sales by Day of Week',
        xaxis=dict(title='Day of Week'),
        yaxis=dict(title='Mean Sales'),
        width=800,
        height=500
    )

    st.plotly_chart(fig)

    item_sales_mean = df.groupby('item')['sales'].mean()


    st.subheader("",divider=True)


    
    top_5_items = item_sales_mean.nlargest(5)
    rest_items = item_sales_mean.nsmallest(len(item_sales_mean) - 5)

    sum_top_5_items = top_5_items.sum()
    sum_rest_items = rest_items.sum()

    pie_data = pd.DataFrame({
        'Category': ['Top 5 items', 'Rest items'],
        'Sales': [sum_top_5_items, sum_rest_items]
    })

    fig = px.pie(pie_data, names='Category', values='Sales', title='Sales percentage of top 5 SKUs and rest of the items')

    fig.update_layout(
        width=600,
        height=600
    )

    st.plotly_chart(fig)


    st.subheader("",divider=True)

    
    sales_by_item_date = df.pivot_table(index='date', columns='item', values='sales', aggfunc='sum')
    sales_by_item_date = pd.DataFrame(sales_by_item_date)

    correlation_matrix = sales_by_item_date.corr()

    np.fill_diagonal(correlation_matrix.values, np.nan)

    # Top 5 correlated items
    top_correlated_items = correlation_matrix.unstack().sort_values(ascending=False)[::2][:5]


    st.header("Items that almost always sell together!")
    st.text(f"Item Numbers ({top_correlated_items.index[0][0]},{top_correlated_items.index[0][1]})")
    st.text(f"Item Numbers ({top_correlated_items.index[1][0]},{top_correlated_items.index[1][1]})")
    st.text(f"Item Numbers ({top_correlated_items.index[2][0]},{top_correlated_items.index[2][1]})")
    st.text(f"Item Numbers ({top_correlated_items.index[3][0]},{top_correlated_items.index[3][1]})")
    st.text(f"Item Numbers ({top_correlated_items.index[4][0]},{top_correlated_items.index[4][1]})")
