import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
import json
import plotly

def historical_closing_price(ticker):
    complete_ticker = ticker + ".NS"
    data = yf.download(complete_ticker)
    df = pd.DataFrame(data)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines'))
    fig.update_layout(title={
        'text': "Historical Stock Price",
        'font': {'size': 18}
    })
    chart_json = json.dumps(fig, cls = plotly.utils.PlotlyJSONEncoder)
    return chart_json
