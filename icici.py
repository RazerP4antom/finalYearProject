from bs4 import BeautifulSoup
import requests


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