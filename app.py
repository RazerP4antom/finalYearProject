from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import plotly.graph_objs as go
import pandas as pd
import plotly
import plotly.io as pio
import json
import requests
import nsepy as nse
from datetime import date
import datetime
import csv
from datetime import date, timedelta
from GoogleNews import GoogleNews
import datetime
import pandas as pd
from nltk.stem import WordNetLemmatizer
from sentiment import *
from newspaper import Article, ArticleException
import nltk

lemmatizer = WordNetLemmatizer()
analyzer = SentimentIntensityAnalyzer()

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

# def get_headlines(company, start_date, end_date):
#     googlenews = GoogleNews()
#     googlenews.set_time_range(start_date.strftime('%m/%d/%Y'), end_date.strftime('%m/%d/%Y'))
#     googlenews.search(company)

#     first_letter_company = company.split()[0]
#     urls_a = []
#     urls_b = []
#     urls_c = []
#     urls_d = []

#     for i in range(3):
#         googlenews.get_page(i+1)
#         result = googlenews.result()
#         for item in result:
#             headline = item['title']
#             link = item['link']
            
#             # Lemmatize the words in the headline
#             words = headline.lower().split()
#             words = [lemmatizer.lemmatize(word) for word in words]
#             headline_lemmatized = ' '.join(words)

#             if first_letter_company in headline_lemmatized:
#               if any(keyword in headline_lemmatized for keyword in ['sale', 'cut', 'production', 'vehicle', 'unveil', 'supply chain', 'launch', 'project', 'merger', 'acquisition', 'fraud', 'innovation', 'product', 'technology', 'business', 'strategy', 'strategic', 'expansion', 'partnership', 'joint venture', 'divestment', 'liquidation', 'insider', 'bankruptcy', 'scandal', 'audit', 'ethical', 'issue', 'EV', 'manufacturing', 'stir', 'row', 'acquire', 'raise', 'growth', 'grow', 'partner', 'round', 'sanction', 'add', 'customer', 'charge', 'settle', 'cap', 'probe', 'controversy', 'capacity', 'institution', 'collaboration', 'handover', 'stake', 'rake in', 'receive', 'convene', 'layoff', 'data center', 'subscriber', 'petition', 'fine', 'sack', 'agreement', 'bid', 'bidder', 'asset', 'compensation', 'plant', 'talk', 'output', 'protest']):
#                   if link not in urls_a:
#                       urls_a.append(link)
#               elif any(keyword in headline_lemmatized for keyword in ['retail', 'you', 'shareholder', 'debt', 'return', 'expect', 'trade', 'investor', 'bonus', 'dividend', 'stock market', 'investment', 'investor relation', 'equity market', 'capital market', 'fund manager', 'hedge fund', 'institutional investor', 'high net worth individual', 'HNI', 'security', 'exchange', 'public', 'offering', 'IPO', 'index', 'bond', 'debenture', 'issue', 'dollar', 'sell-off', 'purchase', 'offer', 'FMCG', 'demand', 'consumer', 'recovery', 'pharma', 'profitable', 'portfolio', 'buyback', 'ex-dividend', 'FII', 'player', 'telecom', 'bullish', 'bearish', 'metal', 'windfall', 'realty', 'NCD']):
#                   if link not in urls_b:
#                       urls_b.append(link)
#               elif any(keyword in headline_lemmatized for keyword in ['Q1', 'Q2', 'Q3', 'Q4', 'q1', 'q2', 'q3', 'q4', 'profit', 'loss', 'performance', 'grow', 'earnings', 'quarter', 'quarterly', 'annual', 'yearly', 'underperform', 'tumble', 'cost', 'drop', 'record', 'surge', 'tax', 'outperform']): 
#                   if link not in urls_c:
#                       urls_c.append(link)
#               elif any(keyword in headline_lemmatized for keyword in ['price', 'rise', 'jump', 'fall', 'volatile', 'spurt', 'bearish', 'bullish', 'value', 'target', 'chart', 'rally', '52 week', 'high', 'low', 'trading', 'buy', 'sell', 'hold', 'all-time high']):
#                   if link not in urls_d:
#                       urls_d.append(link)
        
#     return urls_a, urls_b, urls_c, urls_d

# def sentiment_score_A(urlA):
#   if len(urlA) == 0:
#       return("Not enough articles found")
#   else:
#     total_score_A = 0.0
#     total_weight_A = 0.0
#     for item in urlA:
#       try:
#         article = Article(item)
#         article.download()
#         article.parse()
#         sentences = nltk.sent_tokenize(article.text)
#         if len(sentences) > 2:
#           words = article.title.lower().split()
#           words = [lemmatizer.lemmatize(word) for word in words]
#           headline_lemat = ' '.join(words)
#           text = headline_lemat + article.text.lower()
#         else:
#           words = article.title.lower().split()
#           words = [lemmatizer.lemmatize(word) for word in words]
#           headline_lemat = ' '.join(words)
#           text = headline_lemat
#         if any(keyword in text for keyword in ['fraud','evasion','insider', 'scandal', 'audit', 'practices', 'ethical', 'stir', 'row', 'charge', 'settle', 'probe', 'controversy', 'petition', 'fine', 'compensation', 'protest', 'accuse', 'misappropriation', 'scam']):
#           sentiment = (analyzer.polarity_scores(text)['compound'])
#           weight = 5
#         elif any(keyword in text for keyword in ['divestment', 'liquidation', 'bankrupt','bankruptcy', 'handover', 'stake', 'asset', 'raid', 'seize', 'insolvent', 'insolvency']):
#           sentiment = (analyzer.polarity_scores(text)['compound'])
#           weight = 4
#         elif any(keyword in text for keyword in ['award', 'recognition', 'defect', 'lawsuit', 'merger', 'acquisition', 'consolidation', 'joint venture', 'buyout', 'takeover', 'synergy', 'due diligence', 'bid', 'acquire', 'sell-off', 'partnership', 'partner', 'expansion', 'suspension']):
#           sentiment = (analyzer.polarity_scores(text)['compound'])
#           weight = 3
#         elif any(keyword in text for keyword in ['contract', 'project', 'discovery', 'launch', 'unveil', 'investment', 'invest']):
#           sentiment = (analyzer.polarity_scores(text)['compound'])
#           weight = 2
#         else:
#           sentiment = (analyzer.polarity_scores(text)['compound'])
#           weight = 1
#         total_score_A += (sentiment * weight)
#         total_weight_A += weight
#       except ArticleException as e:
#         continue
#     return("{:.4f}".format(total_score_A/total_weight_A))

# def sentiment_score_B(urlB):
#   if len(urlB) == 0:
#       return("Not enough articles found")
#   else:
#     total_score_B = 0.0
#     total_weight_B = 0.0
#     for item in urlB:
#       try:
#         article = Article(item)
#         article.download()
#         article.parse()
#         sentences = nltk.sent_tokenize(article.text)
#         if len(sentences) > 2:
#           words = article.title.lower().split()
#           words = [lemmatizer.lemmatize(word) for word in words]
#           headline_lemat = ' '.join(words)
#           text = headline_lemat + article.text.lower()
#         else:
#           words = article.title.lower().split()
#           words = [lemmatizer.lemmatize(word) for word in words]
#           headline_lemat = ' '.join(words)
#           text = headline_lemat
#         if any(keyword in text for keyword in ['FII','institutional', 'foreign','investment', 'IPO', 'dividend', 'ex-dividend', 'PE', 'hedge fund', 'angel', 'venture', 'raise', 'fund']):
#           sentiment = (analyzer.polarity_scores(text)['compound'])
#           weight = 4
#         elif any(keyword in text for keyword in ['GST', 'windfall', 'taxation','relaxation', 'subsidy', 'duties', 'customs']):
#           sentiment = (analyzer.polarity_scores(text)['compound'])
#           weight = 3
#         elif any(keyword in text for keyword in ['NCD', 'bonds', 'debentures', 'bonus', 'rights']):
#           sentiment = (analyzer.polarity_scores(text)['compound'])
#           weight = 2
#         else:
#           sentiment = (analyzer.polarity_scores(text)['compound'])
#           weight = 1
#         total_score_B+= (sentiment * weight)
#         total_weight_B += weight
#       except ArticleException as e:
#         continue
#     return("{:.4f}".format(total_score_B/total_weight_B))

# def sentiment_score_C(urlC):
#   if len(urlC) == 0:
#       return("Not enough articles found")
#   else:
#     total_score_C = 0.0
#     for item in urlC:
#       try:
#         article = Article(item)
#         article.download()
#         article.parse()
#         text = article.text
#         sentiment = analyzer.polarity_scores(text)['compound']
#         total_score_C += sentiment
#       except ArticleException as e:
#         continue
#     return("{:.4f}".format(total_score_C/len(urlC)))

# def sentiment_score_D(urlD):
#   if len(urlD) == 0:
#       return("Not enough articles found")
#   else:
#     total_score_D = 0.0
#     for item in urlD:
#       try:
#         article = Article(item)
#         article.download()
#         article.parse()
#         text = article.text
#         sentiment = analyzer.polarity_scores(text)['compound']
#         total_score_D += sentiment
#       except ArticleException as e:
#         continue
#     return("{:.4f}".format(total_score_D/len(urlD)))

def sentiment(urls):
    sentiment = []
    try:
      for item in urls:
        article = Article(item)
        article.download()
        article.parse()
        text = article.text
        score = analyzer.polarity_scores(text)['compound']
        sentiment.append(score)
    except ArticleException as e:
        print()

    return sentiment

def headline(company):
    query = company.split()[0]
    googlenews = GoogleNews(lang='en') 
    end_date = date.today()
    start_date = end_date - timedelta(days=30)
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    googlenews.search(query)
    googlenews.set_time_range(start_date_str, end_date_str)

    results = googlenews.result() 

    titles = [] 
    urls = []  

    for i in range(len(results)): 
      titles.append(results[i]['title'])  
      urls.append(results[i]['link']) 

    y_values = sentiment(urls)
    x_values = [f"Headline {i+1}" for i in range(len(y_values))]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='lines'))
    chart_json = json.dumps(fig, cls = plotly.utils.PlotlyJSONEncoder)

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

    # start_date = datetime.date.today() - datetime.timedelta(days=40)
    # end_date = datetime.date.today()
    # URLS_a, URLS_b, URLS_c, URLS_d = get_headlines(stock_symbol,start_date,end_date)
    # score_a = sentiment_score_A(URLS_a)
    # score_b = sentiment_score_B(URLS_b)
    # score_c = sentiment_score_C(URLS_c)
    # score_d = sentiment_score_D(URLS_d)

    news_line = headline(stock_symbol)
    chart_html = pio.to_html(json.loads(news_line), full_html=False)


    return render_template('stock_data.html', pie_chart=pie_chart,research_data_icic=research_data_icic,
                           research_data_ecotimes = research_data_ecotimes,
                           closing_chart = closing_chart, company_ratios = company_ratios,
                           quaterly_results = quaterly_results,
                           profit_loss = profit_loss,
                           balance_sheet = balance_sheet,
                           cash_flow = cash_flow,
                           shareholding = shareholding,
                           company = stock_symbol,
                           chart_html = chart_html)

if __name__ == '__main__':
    app.run(debug=True)
