from bs4 import BeautifulSoup
import requests

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