from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import pandas as pd
import plotly
import json
import io
import base64
import requests
import nsepy as nse
from datetime import date
import plotly.express as px
import datetime
import csv

app = Flask(__name__)

def pie_chart(data):
    # plt.pie(data.values(), labels=data.keys(), autopct='%1.1f%%')
    # plt.title('Buy, Hold, Sell')

    # # Save the chart to a BytesIO object
    # img = io.BytesIO()
    # plt.savefig(img, format='png')
    # img.seek(0)
    
    # # Encode the chart as base64 and insert into HTML
    # chart = base64.b64encode(img.getvalue()).decode()

    labels = list(data.keys())
    values = list(data.values())
    colors = ['#5cb85c', '#5bc0de', '#d9534f']
    font_color = 'white'
    hover_text = '%{percent}'
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker=dict(colors=colors), 
                                 textfont=dict(color=font_color),
                                 hovertemplate='%{label}: ' + hover_text)])
    
    chart_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return chart_json

def buy_sell_hold(stock_symbol):
    company_name = stock_symbol.lower().replace(" ", "-")
    URL = f'https://groww.in/stocks/{company_name}'
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html.parser')
    
    buy_sell_hold = []
    buy_div = soup.find('div', attrs={'class':'width100'})

    for i in buy_div.findAll('div', attrs={'class':'row valign-wrapper clrSubText'}):
        buy_sell_hold_percent = i.text
        buy_sell_hold_percent = buy_sell_hold_percent[:-3] + ' ' + buy_sell_hold_percent[-3:]
        buy_sell_hold.append(buy_sell_hold_percent)
    
    # data_dict = {item.split()[0]: float(item.split()[1].strip('%')) for item in buy_sell_hold}

    data_dict = {}
    for item in buy_sell_hold:
        split_items = item.split()
        if len(split_items) == 2:
            key = split_items[0]
            value = split_items[1].strip('%').replace('l', '')
            if key == 'Sel':
                key = 'Sell'
            try:
                data_dict[key] = float(value)
            except ValueError:
                print(f"Unable to convert {value} to float for key {key}")

    pie = pie_chart(data_dict)
        
    return pie

def research_report_icic(stock_symbol):
    # base URL
    base_url = "https://www.icicidirect.com/stocks/"
    company_extension = stock_symbol.lower().replace(" ", "-") + "-share-price" 
    full_url = base_url + company_extension
    response = requests.get(full_url)
    html_content = response.text

    soup = BeautifulSoup(html_content, "html.parser")

    div = soup.find("div", id="ResearchReportTab")
    if div:
        a_tag = div.find("a", text="Click here for full recommendation")
        full_recommendation_link = a_tag.get("href")
        # print(full_recommendation_link)
        response1 = requests.get(full_recommendation_link)
        html_content1 = response1.text

        soup = BeautifulSoup(html_content1, "html.parser")

        recommendation = None
        for div in soup.find_all("div", class_="box bg_grey mb-3"):
            for strong in div.find_all("strong"):
                if "What should Investors do?" in strong.text:
                    recommendation = div.text
        
        if recommendation:
            return(recommendation)
        else:
            return"Recommendation not found"
        
    else:
        return"Not fully researched by ICICI direct"
    
def research_report_ecotimes(stock_symbol):
    first_letter = stock_symbol[0]
    company_extension = stock_symbol.lower().replace(" ", "-")
    url = "https://economictimes.indiatimes.com/markets/stocks/stock-quotes/" + first_letter
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    company_link = None
    for ul in soup.find_all('ul', class_='companyList'):
        for li in ul.find_all('li'):
            a_tag = li.find('a')
            if a_tag is not None:
                url_term = a_tag.get('href').split('/')[-3]
                if company_extension in url_term:
                    company_link = a_tag.get('href')
                    break
        if company_link is not None:
            full_url = "https://economictimes.indiatimes.com" + company_link
            break

    if full_url is None:
        return"Company not Found"
    else:
        response = requests.get(full_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        recommendation = soup.find('div', {'class': 'meanTxt'}).span.text
        if recommendation is None:
            return"No recommendation found"
        else:
            return"Recommendation as per analysts: {}".format(recommendation) 

def historical_closing_price(ticker):
    today = datetime.date.today()
    stock_price = nse.get_history(symbol = ticker, start=date(2022,1,1), end=today)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=stock_price.index, y=stock_price['Close'], mode='lines'))
    chart_json = json.dumps(fig, cls = plotly.utils.PlotlyJSONEncoder)
    # print(chart_json)
    return chart_json

def ratios(ticker):

    url = 'https://www.screener.in/company/'
    full_url = url + ticker + '/'
    response = requests.get(full_url)

    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find('div', {'class': 'company-ratios'})
    ratios = []
    for li in div.find_all('li'):
        name = li.find('span', {'class': 'name'}).text.strip()
        # Exclude 'High / Low' ratio
        if name == 'High / Low':
            continue
        value = li.find('span', {'class': 'number'})
        if value is not None:
            # For ratios with currency values, add the rupee symbol and 'Cr.' suffix
            if 'Market Cap' in name or 'Book Value' in name:
                value = '₹' + value.text.strip() + ' Cr.'
            # For ratios with percentage values, add the percentage sign
            elif 'Dividend Yield' in name or 'ROCE' in name or 'ROE' in name:
                value = value.text.strip() + '%'
            else:
                value = value.text.strip()
        else:
            value = li.find('span', {'class': 'value'}).text.strip()
        ratios.append(f'{name}: {value}')

    return ratios

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
    table_final = table.to_html()

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

    table_final = df.to_html()

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

    table_final = df.to_html()

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

    table_final = df.to_html()

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



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_stock_data', methods=['POST'])
def get_stock_data_route():
    stock_symbol = request.form['stock_symbol']
    pie_chart = buy_sell_hold(stock_symbol)
    research_data_icic = research_report_icic(stock_symbol)
    research_data_ecotimes = research_report_ecotimes(stock_symbol)
    with open('Tickers.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
    
    for row in rows:
        if row['Company Name'] == stock_symbol:
            ticker = row['Ticker']
    closing_chart = historical_closing_price(ticker)
    company_ratios = ratios(ticker)
    quaterly_results = quaterly_table(ticker)
    profit_loss = profit_loss_table(ticker)
    balance_sheet = balance_sheet_table(ticker)
    cash_flow = cash_flow_table(ticker)
    shareholding = share_holding_pie_chart(ticker)

    return render_template('stock_data.html', pie_chart=pie_chart,research_data_icic=research_data_icic,
                           research_data_ecotimes = research_data_ecotimes,
                           closing_chart = closing_chart, company_ratios = company_ratios,
                           quaterly_results = quaterly_results,
                           profit_loss = profit_loss,
                           balance_sheet = balance_sheet,
                           cash_flow = cash_flow,
                           shareholding = shareholding)

if __name__ == '__main__':
    app.run(debug=True)
