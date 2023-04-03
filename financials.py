from bs4 import BeautifulSoup
import pandas as pd
import requests
import json
import plotly
import plotly.graph_objs as go


def quaterly_table(ticker):
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
    table_final = table.to_html(classes="data-table")

    return table_final
    
def profit_loss_table(ticker):
    url = 'https://www.screener.in/company/'
    full_url = url + ticker + '/#profit-loss'
    r = requests.get(full_url)
    soup = BeautifulSoup(r.content, 'html.parser')

    section = soup.find('section', {'id': 'profit-loss'})
    table = section.find('table', {'class': 'data-table'})
    df = pd.read_html(str(table))[0]
    df['Unnamed: 0'] = df['Unnamed: 0'].str.replace('+', '')
    df = df.rename(columns={'Unnamed: 0': ''})

    table_final = df.to_html(classes="data-table")

    return table_final
    
def balance_sheet_table(ticker):
    url = 'https://www.screener.in/company/'
    full_url = url + ticker + '/#balance-sheet'
    r = requests.get(full_url)
    soup = BeautifulSoup(r.content, 'html.parser')

    section = soup.find('section', {'id': 'balance-sheet'})
    table = section.find('table', {'class': 'data-table'})
    df = pd.read_html(str(table))[0]
    df['Unnamed: 0'] = df['Unnamed: 0'].str.replace('+', '')
    df = df.rename(columns={'Unnamed: 0': ''})

    table_final = df.to_html(classes="data-table")

    return table_final

def cash_flow_table(ticker):
    url = 'https://www.screener.in/company/'
    full_url = url + ticker + '/#cash-flow'
    r = requests.get(full_url)
    soup = BeautifulSoup(r.content, 'html.parser')

    section = soup.find('section', {'id': 'cash-flow'})
    table = section.find('table', {'class': 'data-table'})
    df = pd.read_html(str(table))[0]
    df['Unnamed: 0'] = df['Unnamed: 0'].str.replace('+', '')
    df = df.rename(columns={'Unnamed: 0': ''})

    table_final = df.to_html(classes="data-table")

    return table_final

def share_holding_pie_chart(ticker):
    url = 'https://www.screener.in/company/'
    full_url = url + ticker + '/#shareholding'
    r = requests.get(full_url)
    soup = BeautifulSoup(r.content, 'html.parser')

    section = soup.find('section', {'id': 'shareholding'})
    table = section.find('table', {'class': 'data-table'})
    df = pd.read_html(str(table))[0]
    df['Unnamed: 0'] = df['Unnamed: 0'].str.replace('+', '')
    df = df.rename(columns={'Unnamed: 0': ''})
    df.set_index(df.columns[0], inplace=True)

    # hover_text = '%{percent}'
    trace = go.Pie(labels=df.index, values=df[df.columns[-1]], 
               hovertemplate='%{label}: %{percent}')
    layout = go.Layout(title=f'Shareholding in {df.columns[-1]}')
    fig = go.Figure(data=[trace], layout=layout)
    chart_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return chart_json