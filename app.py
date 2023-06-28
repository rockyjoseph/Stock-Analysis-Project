import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from nsepy import get_history
from nsepy import get_rbi_ref_history
from nsetools import Nse

from datetime import date

nse = Nse()

st.header('Stock Analysis Website')
st.sidebar.title('Explore')

menu_bar = st.sidebar.radio('Select an Option',
                            ('STOCKS', 'INDIA VIX',
                             'DERIVATIVES', 'FOREX'))

if menu_bar == 'STOCKS':
    home_stocks, search_stocks = st.tabs(["Stocks", "Search Stocks"])

    with home_stocks:
        st.title("Top Gainers")
        top_gainers = nse.get_top_gainers()
        gainers = pd.DataFrame(top_gainers)
        gainers.drop(columns=['ltp','series','turnoverInLakhs'], inplace = True)
        st.table(gainers)

        st.title("Top Losers")
        top_losers = nse.get_top_losers()
        losers = pd.DataFrame(top_losers)
        losers.drop(columns=['ltp','series','turnoverInLakhs'], inplace = True)
        st.table(losers)

    with search_stocks:
        st.title('SEARCH STOCKS')
        stock_name = st.text_input('Stock Name: ')
        start_date = st.date_input('From: ')
        end_date = st.date_input('To: ')

        st.title(stock_name)
        Line, Candle = st.tabs(["Line", "Candle"])
        fig = go.Figure()
        with Line:
            stocks = get_history(symbol=stock_name, start=start_date, end=end_date)
            line_chart = px.line(stocks, y='Close')
            line_chart.update_layout(height=500, width=800, plot_bgcolor="black", xaxis=dict(showgrid=False),
                                    yaxis=dict(showgrid=False, title='Price')
                                    )
            st.plotly_chart(line_chart)
        with Candle:
            stocks = get_history(symbol=stock_name, start=start_date, end=end_date)
            candle_stick = fig.add_trace(go.Candlestick(
                open=stocks['Open'], high=stocks['High'],
                low=stocks['Low'], close=stocks['Close']))
            fig.update_layout(height=500, width=800, plot_bgcolor='black', xaxis=dict(showgrid=False),
                            yaxis=dict(showgrid=False,  title='Price'))
            st.plotly_chart(candle_stick)

        st.title('Daily Price Statement')
        stocks['%Change'] = stocks['Close'] / stocks['Close'].shift(1) - 1
        stocks_annual_return = stocks['%Change'].mean()*252*100
        stocks_std = np.std(stocks['%Change']) * np.sqrt(252)
        stocks_risk = stocks_annual_return / (stocks_std*100)
        st.write('Annual return: ', stocks_annual_return)
        st.write('Risk: ', stocks_risk)
        stocks.dropna(inplace=True)
        st.table(stocks)

if menu_bar == 'INDIA VIX':
    st.write('''What is the Vix and why is it important?
    
The India VIX value has a direct relation with the volatility,which means that higher the value of India VIX, higher is the volatility.
Whereas, lower the value of the India VIX,lower will be the volatility in the market.
                The VIX is also a helpful indicator for options traders. Volatility is typically used to determine whether to purchase or sell an option.
                When volatility is expected to grow, options become more attractive, and buyers tend to profit more. When the VIX falls,
                there will be more squandering of time value, and option sellers will gain more.''')
    st.write('''Is India Vix a directional move?

But be aware of the fact, India VIX does not give any indication of the directional move in the market,
it simply indicates the volatility in the market.So, anyone with a huge investment in Equities should keep a close eye on the movement of India VIX
coz a similar movement in the shares of his portfolio cannot be ruled out.''')

    start_date = st.sidebar.date_input('From: ')
    end_date = st.sidebar.date_input('To: ')

    st.title('INDIA VIX')
    vix = get_history(symbol="INDIAVIX", start=start_date,
                    end=end_date, index=True)
    vix_chart = px.line(vix, y='Change')
    vix_chart.update_layout(height=500, width=800, plot_bgcolor="black", xaxis=dict(showgrid=False),
                        yaxis=dict(showgrid=False, title='Price')
                    )
    st.plotly_chart(vix_chart)
    st.title('VIX Daily Price Statement')
    vix_annual_return = vix['%Change'].mean() * 252 * 100
    vix_std = np.std(vix['%Change']) * np.sqrt(252)
    vix_risk = vix_annual_return / (vix_std * 100)
    st.write('Annual return: ', vix_annual_return)
    st.write('Risk: ', vix_risk)
    vix.dropna(inplace=True)
    st.table(vix)

if menu_bar == 'DERIVATIVES':
    f_no, lot_sizes = st.tabs(["F&O", "F&O Lot Sizes"])

    with f_no:
        fno_gainers = nse.get_top_fno_gainers()
        fno_losers = nse.get_top_fno_losers()
        st.title('Futures & Options Gainers')
        st.table(fno_gainers)
        st.title('Futures & Options Losers')
        st.table(fno_losers)

    with lot_sizes:
        st.title('Futures & Options Lot Sizes')
        options_lot_size = nse.get_fno_lot_sizes()
        st.write(options_lot_size)

if menu_bar == 'FOREX':
        st.title('Forex')
        st.title('RBI REF RATE')
        rbi_start_date = st.date_input('From: ')
        rbi_end_date = st.date_input('To: ')
        rbi_ref = get_rbi_ref_history(rbi_start_date, rbi_end_date)
        st.write(rbi_ref)
