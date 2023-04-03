from bs4 import BeautifulSoup
import requests
import plotly.graph_objs as go
import plotly
import plotly.io as pio
import json


def pie_chart(data):
    labels = list(data.keys())
    values = list(data.values())
    colors = ['#5cb85c', '#5bc0de', '#d9534f']
    font_color = 'white'
    hover_text = '%{percent}'
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker=dict(colors=colors), 
                                 textfont=dict(color=font_color),
                                 hovertemplate='%{label}: ' + hover_text)])
    fig.update_layout(title={
        'text': "Groww Recommendation",
        'font': {'size': 18}
    })
    
    chart_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return chart_json

def buy_sell_hold(stock_symbol):
    if stock_symbol == "Larsen and Toubro Ltd":
        stock_symbol = "Larsen Toubro Ltd"
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