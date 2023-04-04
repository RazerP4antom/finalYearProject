from bs4 import BeautifulSoup
import pandas as pd
import requests
import yfinance as yf
import json
import plotly
import plotly.graph_objs as go

def quaterly_graph(ticker):
    url = 'https://www.screener.in/company/'
    full_url = url + ticker + '/#quaters'
    r = requests.get(full_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find('table', {'class': 'data-table'})
    df = pd.read_html(str(table))[0]
    # df.drop('Raw PDF', axis=0, inplace=True)
    df['Unnamed: 0'] = df['Unnamed: 0'].str.replace('+', '')
    df = df.rename(columns={'Unnamed: 0': ''})
    table = df.head(11)

    complete_ticker = ticker + ".NS"
    data = yf.download(complete_ticker)
    df2 = pd.DataFrame(data)

    


    
