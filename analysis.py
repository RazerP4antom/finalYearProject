from serpapi import GoogleSearch
from datetime import datetime, timedelta 
import pandas as pd
import time
import nltk
from nltk.stem import WordNetLemmatizer
from newspaper import Article, ArticleException
from sentiment import *

lemmatizer = WordNetLemmatizer()
analyzer = SentimentIntensityAnalyzer()

def sentiment_score_A(urlA):
  if len(urlA) == 0:
      return("Not enough articles found")
  else:
    total_score_A = 0.0
    total_weight_A = 0.0
    for item in urlA:
      try:
        article = Article(item)
        article.download()
        article.parse()
        sentences = nltk.sent_tokenize(article.text)
        if len(sentences) > 2:
          words = article.title.lower().split()
          words = [lemmatizer.lemmatize(word) for word in words]
          headline_lemat = ' '.join(words)
          text = headline_lemat + article.text.lower()
        else:
          words = article.title.lower().split()
          words = [lemmatizer.lemmatize(word) for word in words]
          headline_lemat = ' '.join(words)
          text = headline_lemat
        if any(keyword in text for keyword in ['fraud','evasion','insider', 'scandal', 'audit', 'practices', 'ethical', 'stir', 'row', 'charge', 'settle', 'probe', 'controversy', 'petition', 'fine', 'compensation', 'protest', 'accuse', 'misappropriation', 'scam']):
          sentiment = (analyzer.polarity_scores(text)['compound'])
          weight = 5
        elif any(keyword in text for keyword in ['divestment', 'liquidation', 'bankrupt','bankruptcy', 'handover', 'stake', 'asset', 'raid', 'seize', 'insolvent', 'insolvency']):
          sentiment = (analyzer.polarity_scores(text)['compound'])
          weight = 4
        elif any(keyword in text for keyword in ['award', 'recognition', 'defect', 'lawsuit', 'merger', 'acquisition', 'consolidation', 'joint venture', 'buyout', 'takeover', 'synergy', 'due diligence', 'bid', 'acquire', 'sell-off', 'partnership', 'partner', 'expansion', 'suspension']):
          sentiment = (analyzer.polarity_scores(text)['compound'])
          weight = 3
        elif any(keyword in text for keyword in ['contract', 'project', 'discovery', 'launch', 'unveil', 'investment', 'invest']):
          sentiment = (analyzer.polarity_scores(text)['compound'])
          weight = 2
        else:
          sentiment = (analyzer.polarity_scores(text)['compound'])
          weight = 1
        total_score_A += (sentiment * weight)
        total_weight_A += weight
      except ArticleException as e:
        continue
    return float(("{:.4f}".format(total_score_A/total_weight_A)))

def sentiment_score_B(urlB):
  if len(urlB) == 0:
      return("Not enough articles found")
  else:
    total_score_B = 0.0
    total_weight_B = 0.0
    for item in urlB:
      try:
        article = Article(item)
        article.download()
        article.parse()
        sentences = nltk.sent_tokenize(article.text)
        if len(sentences) > 2:
          words = article.title.lower().split()
          words = [lemmatizer.lemmatize(word) for word in words]
          headline_lemat = ' '.join(words)
          text = headline_lemat + article.text.lower()
        else:
          words = article.title.lower().split()
          words = [lemmatizer.lemmatize(word) for word in words]
          headline_lemat = ' '.join(words)
          text = headline_lemat
        if any(keyword in text for keyword in ['FII','institutional', 'foreign','investment', 'IPO', 'dividend', 'ex-dividend', 'PE', 'hedge fund', 'angel', 'venture', 'raise', 'fund']):
          sentiment = (analyzer.polarity_scores(text)['compound'])
          weight = 4
        elif any(keyword in text for keyword in ['GST', 'windfall', 'taxation','relaxation', 'subsidy', 'duties', 'customs']):
          sentiment = (analyzer.polarity_scores(text)['compound'])
          weight = 3
        elif any(keyword in text for keyword in ['NCD', 'bonds', 'debentures', 'bonus', 'rights']):
          sentiment = (analyzer.polarity_scores(text)['compound'])
          weight = 2
        else:
          sentiment = (analyzer.polarity_scores(text)['compound'])
          weight = 1
        total_score_B+= (sentiment * weight)
        total_weight_B += weight
      except ArticleException as e:
        continue
    return float(("{:.4f}".format(total_score_B/total_weight_B)))
  
def sentiment_score_C(urlC):
  if len(urlC) == 0:
      return("Not enough articles found")
  else:
    total_score_C = 0.0
    for item in urlC:
      try:
        article = Article(item)
        article.download()
        article.parse()
        text = article.text
        sentiment = analyzer.polarity_scores(text)['compound']
        total_score_C += sentiment
      except ArticleException as e:
        continue
    return float("{:.4f}".format(total_score_C/len(urlC)))
  
def sentiment_score_D(urlD):
  if len(urlD) == 0:
      return("Not enough articles found")
  else:
    total_score_D = 0.0
    for item in urlD:
      try:
        article = Article(item)
        article.download()
        article.parse()
        text = article.text
        sentiment = analyzer.polarity_scores(text)['compound']
        total_score_D += sentiment
      except ArticleException as e:
        continue
    return float("{:.4f}".format(total_score_D/len(urlD)))
  
def get_headlines(company):

    search_params = {
        "q": company,
        "tbm": "nws",
        "location": "India",
        "api_key": "562c5937810dfdce1353fdaf0ab2668339295eccbc09aa88d6007990cb74581f" }

    # Define the date ranges
    today = datetime.now()
    last_month = today - timedelta(days=30)
    two_months_ago = today - timedelta(days=60)
    three_months_ago = today - timedelta(days=90)
    one_week_ago = today - timedelta(days=7)

    # Define the number of articles to fetch from each date range
    oldest_count = 7
    intermediate_count = 12
    recent_count = 11
    recent_week_count = 10

    # Define a function to fetch news articles for a given date range
    def fetch_articles(start_date, end_date, count):
        # Set the search parameters for the given date range
        params = search_params.copy()
        params.update({
            "tbs": f"cdr:1,cd_min:{start_date.strftime('%m/%d/%Y')},cd_max:{end_date.strftime('%m/%d/%Y')}",
            "num": count
        })
        
        # Fetch the search results
        search = GoogleSearch(params)
        results = search.get_dict()
        
        # Extract the news articles from the search results
        articles = []
        if 'news_results' in results:
            news_results = results["news_results"]
            for news_result in news_results:
                link = news_result.get("link", "")
                headline = news_result.get("title", "")
                articles.append({"headline": headline, "link": link})
        
        return articles

    # Fetch the news articles for each date range and merge them into a single list
    all_articles = []
    all_articles += fetch_articles(three_months_ago, two_months_ago, oldest_count)
    all_articles += fetch_articles(two_months_ago, last_month, intermediate_count)
    all_articles += fetch_articles(last_month, today - timedelta(days=7), recent_count)
    all_articles += fetch_articles(one_week_ago, today, recent_week_count)

    urls_a = []
    urls_b = []
    urls_c = []
    urls_d = []

    for article in all_articles:
      # Lemmatize the words in the headline
      headline1 = article['headline']
      words = headline1.lower().split()
      words = [lemmatizer.lemmatize(word) for word in words]
      headline_lemmatized = ' '.join(words)
      if any(keyword in headline_lemmatized for keyword in ['sale', 'cut', 'production', 'vehicle', 'unveil', 'supply chain', 'launch', 'project', 'merger', 'acquisition', 'fraud', 'innovation', 'product', 'technology', 'business', 'strategy', 'strategic', 'expansion', 'partnership', 'joint venture', 'divestment', 'liquidation', 'insider', 'bankruptcy', 'scandal', 'audit', 'ethical', 'issue', 'EV', 'manufacturing', 'stir', 'row', 'acquire', 'raise', 'growth', 'grow', 'partner', 'round', 'sanction', 'add', 'customer', 'charge', 'settle', 'cap', 'probe', 'controversy', 'capacity', 'institution', 'collaboration', 'handover', 'stake', 'rake in', 'receive', 'convene', 'layoff', 'data center', 'subscriber', 'petition', 'fine', 'sack', 'agreement', 'bid', 'bidder', 'asset', 'compensation', 'plant', 'talk', 'output', 'protest']):
       if article['link'] not in urls_a:
         urls_a.append(article['link'])
      elif any(keyword in headline_lemmatized for keyword in ['retail', 'you', 'shareholder', 'debt', 'return', 'expect', 'trade', 'investor', 'bonus', 'dividend', 'stock market', 'investment', 'investor relation', 'equity market', 'capital market', 'fund manager', 'hedge fund', 'institutional investor', 'high net worth individual', 'HNI', 'security', 'exchange', 'public', 'offering', 'IPO', 'index', 'bond', 'debenture', 'issue', 'dollar', 'sell-off', 'purchase', 'offer', 'FMCG', 'demand', 'consumer', 'recovery', 'pharma', 'profitable', 'portfolio', 'buyback', 'ex-dividend', 'FII', 'player', 'telecom', 'bullish', 'bearish', 'metal', 'windfall', 'realty', 'NCD']):
       if article['link'] not in urls_b:
         urls_b.append(article['link'])
      elif any(keyword in headline_lemmatized for keyword in ['Q1', 'Q2', 'Q3', 'Q4', 'q1', 'q2', 'q3', 'q4', 'profit', 'loss', 'performance', 'grow', 'earnings', 'quarter', 'quarterly', 'annual', 'yearly', 'underperform', 'tumble', 'cost', 'drop', 'record', 'surge', 'tax', 'outperform']): 
       if article['link'] not in urls_c:
         urls_c.append(article['link'])
      elif any(keyword in headline_lemmatized for keyword in ['price', 'rise', 'jump', 'fall', 'volatile', 'spurt', 'bearish', 'bullish', 'value', 'target', 'chart', 'rally', '52 week', 'high', 'low', 'trading', 'buy', 'sell', 'hold', 'all-time high', 'slips']):
       if article['link'] not in urls_d:
         urls_d.append(article['link'])
    return urls_a, urls_b, urls_c, urls_d

