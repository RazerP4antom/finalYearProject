from flask import Flask, render_template, request
from threading import Thread

import csv
from groww import *
from icici import *
from ecotimes import *
from historical import *
from ratios import *
from financials import *
from analysis import *
from score import *

app = Flask(__name__)


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

    
    URLS_a, URLS_b, URLS_c, URLS_d = get_headlines(stock_symbol)
    score_a = sentiment_score_A(URLS_a)
    score_b = sentiment_score_B(URLS_b)
    score_c = sentiment_score_C(URLS_c)
    score_d = sentiment_score_D(URLS_d)

    sentiment_output, trading_output = final_output(score_a,score_b,score_c,score_d)




    return render_template('stock_data.html',
                           stock_symbol = stock_symbol,
                           pie_chart=pie_chart,
                           research_data_icic=research_data_icic,
                           research_data_ecotimes = research_data_ecotimes,
                           closing_chart = closing_chart,
                           company_ratios = company_ratios,
                           quaterly_results = quaterly_results,
                           profit_loss = profit_loss,
                           balance_sheet = balance_sheet,
                           cash_flow = cash_flow,
                           shareholding = shareholding,
                           company = stock_symbol,
                           score_a = score_a,
                           score_b = score_b,
                           score_c = score_c,
                           score_d = score_d,
                           sentiment_output = sentiment_output,
                           trading_output = trading_output)


if __name__ == '__main__':
    app.run(debug=True,threaded = True)
