from bs4 import BeautifulSoup
import requests
import re

def about_company(ticker):
    url = 'https://www.screener.in/company/'
    full_url = url + ticker
    r = requests.get(full_url)
    soup = BeautifulSoup(r.content, 'html.parser')

    about = soup.find('div',{'class':'about'})
    p_tags = about.find_all('p')

    text_contents = []
    for p_tag in p_tags:
        text_contents.append(p_tag.text)

    text_string = ' '.join(text_contents)
    text_string = re.sub(r'\[\d+\]', '', text_string)

    return text_string