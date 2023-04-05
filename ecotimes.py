from bs4 import BeautifulSoup
import requests
import re

def research_report_ecotimes(stock_symbol):
    if (stock_symbol == "Cipla Ltd"):
        full_url = "https://economictimes.indiatimes.com/cipla-ltd/stocks/companyid-13917.cms"
    else:
        stock_symbol = re.sub(r'\b\s*and\s*\b', ' ', stock_symbol)
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
