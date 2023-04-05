from bs4 import BeautifulSoup
import requests
import re

def about_company(ticker):
    if (ticker == "CIPLA"):
        text_string = 'Cipla Limited is an Indian multinational pharmaceutical company, headquartered in Mumbai. Cipla primarily develops medicines to treat respiratory disease, cardiovascular disease, arthritis, diabetes, depression, and many other medical conditions.'

    else: 
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