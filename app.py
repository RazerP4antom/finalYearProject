from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import io
import base64
import requests

app = Flask(__name__)

def pie_chart(data):
    plt.pie(data.values(), labels=data.keys(), autopct='%1.1f%%')
    plt.title('Buy, Hold, Sell')

    # Save the chart to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    
    # Encode the chart as base64 and insert into HTML
    chart = base64.b64encode(img.getvalue()).decode()

    return chart

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
    
    data_dict = {item.split()[0]: float(item.split()[1].strip('%')) for item in buy_sell_hold}
    pie = pie_chart(data_dict)
    
        
    return pie


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
    


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_stock_data', methods=['POST'])
def get_stock_data_route():
    stock_symbol = request.form['stock_symbol']
    stock_data = buy_sell_hold(stock_symbol)
    research_data_icic = research_report_icic(stock_symbol)
    research_data_ecotimes = research_report_ecotimes(stock_symbol)

    return render_template('stock_data.html', stock_data=stock_data,research_data_icic=research_data_icic,
                           research_data_ecotimes = research_data_ecotimes)

if __name__ == '__main__':
    app.run(debug=True)