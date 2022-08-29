import streamlit as st
import pandas as pd
from PIL import Image
import datetime as dt
from datetime import datetime, timedelta
from src import extract_data
import plotly.graph_objects as go
import plotly.express as px

# image = Image.open('logo.png')
st.set_page_config(page_title='dashboard',layout="wide",initial_sidebar_state="expanded")

st.title('Sale Dashboard')

def get_time_week():
    now = datetime.now()
    temp_5week_before = now - timedelta(weeks = 2)
    temp_1week_before = now - timedelta(weeks = 1)
    
    from_week = int(temp_5week_before.strftime("%V"))
    from_year = int(temp_5week_before.year)
    to_week = int(temp_1week_before.strftime("%V"))
    to_year = int(temp_1week_before.year)
    return from_week, from_year, to_week, to_year

st.sidebar.subheader("Set frequency: ")
frequency = st.sidebar.selectbox('',("Overview","Daily","Weekly", "Monthly","Quarterly"))
now = dt.datetime.now()

if frequency == "Overview":
    try:
        # st.subheader(f"Report Daily on {datetime.strftime(d, '%Y-%m-%d')}")

        tl = extract_data.extract_transaction_log()

        revenue = tl['sales_amount'].sum()
        sale = tl['sales_qty'].sum()
        order = len(tl.index)

        metric1, metric2, metric3 = st.columns(3)

        metric1.metric(label='Total Revenue',
                        value=revenue)
        metric2.metric(label='Sale Quantity',
                        value=sale)
        metric3.metric(label='Total Order',
                        value=order)

        customgroup = tl.groupby('markets_name').agg({'sales_amount':'sum','sales_qty':'sum'}).reset_index()

        fig1, fig2 = st.columns(2)
        fig1.subheader('Revenue By Market')
        chart1 = go.Figure(data = go.Bar(x = customgroup['sales_amount'],y= customgroup['markets_name'],orientation='h'))
        chart1.layout.margin.update({'t':0,'b':20,'r':50, 'l':50})
        chart1.update_layout({'height':300}, yaxis={'categoryorder':'total ascending'}, xaxis_title = 'Revenue')
        fig1.plotly_chart(chart1 , use_container_width=True)

        fig2.subheader('Sale Quantity By Market')
        chart2 = go.Figure(data = go.Bar(x = customgroup['sales_qty'],y= customgroup['markets_name'],orientation='h'))
        chart2.layout.margin.update({'t':0,'b':20,'r':50, 'l':50})
        chart2.update_layout({'height':300}, yaxis={'categoryorder':'total ascending'}, xaxis_title = 'Sale Quantity')
        fig2.plotly_chart(chart2 , use_container_width=True)

        st.subheader('Revenue by Year')
        tl['year'] = pd.to_datetime(tl['order_date']).dt.year
        revenue_by_year = tl.groupby('year').agg({'sales_amount':'sum'}).reset_index()
        chart3 = go.Figure(data = go.Scatter(x = revenue_by_year['year'],y= revenue_by_year['sales_amount'],orientation='h'))
        chart3.layout.margin.update({'t':0,'b':20,'r':50, 'l':50})
        chart3.update_layout({'height':300}, yaxis={'categoryorder':'total ascending'}, xaxis_title = 'Sale Quantity')
        st.plotly_chart(chart3 , use_container_width=True)

        fig3, fig4 = st.columns(2)

        top5_revenue = (customgroup.sort_values(by=['sales_amount'], ascending=False)).head(5)
        fig3.subheader('Top 5 Customers by Revenue')
        chart3 = go.Figure(data = go.Bar(x = top5_revenue['sales_amount'],y= top5_revenue['markets_name'],orientation='h'))
        chart3.layout.margin.update({'t':0,'b':20,'r':50, 'l':50})
        chart3.update_layout({'height':300}, yaxis={'categoryorder':'total ascending'}, xaxis_title = 'Revenue')
        fig3.plotly_chart(chart3 , use_container_width=True)

        top5_sale = (customgroup.sort_values(by=['sales_qty'], ascending=False)).head(5)
        fig4.subheader('Top 5 Products by Revenue')
        chart4 = go.Figure(data = go.Bar(x = top5_sale['sales_qty'],y= top5_sale['markets_name'],orientation='h'))
        chart4.layout.margin.update({'t':0,'b':20,'r':50, 'l':50})
        chart4.update_layout({'height':300}, yaxis={'categoryorder':'total ascending'}, xaxis_title = 'Sale Quantity')
        fig4.plotly_chart(chart4 , use_container_width=True)

    except:
        st.text("Data is not available!")
if frequency == "Daily":
    try:
        d = st.sidebar.date_input("Date",now)
        st.subheader(f"Report Daily on {datetime.strftime(d, '%Y-%m-%d')}")

        tl = extract_data.extract_transaction_log_with_date(f"{d.strftime('%Y-%m-%d')} 00:00:00", f"{d.strftime('%Y-%m-%d')} 23:59:59")

        revenue = tl['sales_amount'].sum()
        sale = tl['sales_qty'].sum()
        order = len(tl.index)

        metric1, metric2, metric3 = st.columns(3)

        metric1.metric(label='Total Revenue',
                        value=revenue)
        metric2.metric(label='Sale Quantity',
                        value=sale)
        metric3.metric(label='Total Order',
                        value=order)

        customgroup = tl.groupby('markets_name').agg({'sales_amount':'sum','sales_qty':'sum'}).reset_index()

        fig1, fig2 = st.columns(2)
        fig1.subheader('Revenue By Market')
        chart1 = go.Figure(data = go.Bar(x = customgroup['sales_amount'],y= customgroup['markets_name'],orientation='h'))
        chart1.layout.margin.update({'t':0,'b':20,'r':50, 'l':50})
        chart1.update_layout({'height':300}, yaxis={'categoryorder':'total ascending'}, xaxis_title = 'Revenue')
        fig1.plotly_chart(chart1 , use_container_width=True)

        fig2.subheader('Sale Quantity By Market')
        chart2 = go.Figure(data = go.Bar(x = customgroup['sales_qty'],y= customgroup['markets_name'],orientation='h'))
        chart2.layout.margin.update({'t':0,'b':20,'r':50, 'l':50})
        chart2.update_layout({'height':300}, yaxis={'categoryorder':'total ascending'}, xaxis_title = 'Sale Quantity')
        fig2.plotly_chart(chart2 , use_container_width=True)

    except:
        st.text("Data is not available!")
