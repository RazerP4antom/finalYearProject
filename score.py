def final_output(a,b,c,d):

     if isinstance(a, str) or isinstance(b, str) or isinstance(c, str) or isinstance(d, str):
        return "Not enough articles were found to make a cumulative analysis",None
     
     else:
        if(-1.0 <= a <= -0.3): 
            output1 = "You are advised to remain extremely cautious and preferably avoid investing in this company temporarily, as its public image or future prospects seem questionable. If you are an existing shareholder, you may want to gather additional information on how to minimize losses in any adverse circumstance - whether it is through the reduction of your holdings or through hedging by buying put options. Another outlook could be to buy more shares if you have enough information to believe that this phase will be overcome by the company fairly soon. Exercise discretion and be aware of your options."

        elif(-0.3 < a <= 0.5): 
            if(-1.0 <= c <= -0.1):
                output1 ="The company is most likely recovering from a scandal or a bout of bad decisions and has suffered a major hit to its quarterly results.  Hence it is important to evaluate the steps it's taking to address the crisis and consider whether the long-term prospects are impacted or if this situation is temporary and can be countered soon. If the outlook is strong, holding onto the shares may be worthwhile, but if it's bleak, selling shares to minimize losses may be necessary. Exercise discretion and carefully evaluate the situation."
            elif(-0.1 < c <= 0.5) and (-1.0 <= b <= -0.3):
                output1 ="In this case the company’s recent financial results are neither very good nor very bad however, market sentiment about longer term is weak. Please evaluate the longer term prospects or the efforts of management to address the longer term issues. Prospective investors with high risk appetites may take advantage of lower share prices, while those with low-risk appetites may avoid investing."

            elif(-0.1 < c <= 0.5) and (-0.3 < b <= 0.5):
                output1 ="In this case, investor sentiment towards this company's share seems to be improving and perhaps the company is taking some solid measures to counteract losses or crises. It is worth looking into the company's next few steps and its financials to take advantage of a possible rise in the share price. You may want to look into buying a small quantity of shares with more research and expert opinions."

            elif(-0.1 < c <=0.5) and (0.5 < b <= 1.0):
                output1 ="The market sentiment for this stock is rapidly improving, but investors should exercise caution to avoid being caught up in a potential bubble. It is important to conduct thorough research into the company's financials and recent developments to take advantage of the positive signal for shareholders to increase their holdings or for new investors to enter the market. Determine whether this positive sentiment is sustainable or not, although analyst ratings for this stock are probably becoming more optimistic."

            elif(0.5 < c <= 1.0) and (-1.0 <= b <= -0.3):
                output1 ="Evaluate the company's financial position and prospects carefully, even if the market advice is negative despite the company's image and quarter results improving. If the company is taking solid measures to recover, and the negative market sentiment seems temporary, consider holding onto shares. If there are underlying issues, consider selling shares. Prospective investors with high risk appetites may take advantage of lower share prices, while those with low-risk appetites may avoid investing."

            elif(0.3 < c <= 1.0) and (-0.3 < b <= 0.5):
                output1 ="In this case, the company seems to be recovering financially and image-wise, and the market sentiment for investors is becoming slightly positive. Evaluate the company's financial position and recent developments to consider increasing your holdings or investing slightly more liberally if you are a new investor. However, exercise discretion and avoid making impulsive decisions based solely on the positive market sentiment."

            elif(0.3 < c <= 1.0) and (0.5 < b <= 1.0):
                output1 ="In this case, the company's financials and image are improving, and market sentiment for investors is strongly positive. Consider taking advantage of this opportunity by thoroughly researching the company's recent developments and financial position. If everything seems positive, you may want to increase your share holdings or consider investing more liberally if you are a new investor."

        elif(0.5 < a <= 1.0):   
            if(-1.0 < c <= -0.1):
                output1 ="In this case, the company's image is quite positive, but the quarter results are not good. As an investor, you should evaluate the reasons behind the poor quarter results and determine whether they are indicative of a temporary setback or a long-term problem. Look into the company's financials and recent developments to assess whether the losses were caused by some unusual expenses or major investment activity that will bring benefits in the future. Based on your findings you may want to withdraw your stake or increase it, respectively."

            elif(-0.1 < c <= 0.5) and (-1.0 <= b <= -0.3):
                output1 ="In this case, the company's image is positive, but quarter results are satisfactory despite market advice leaning towards negative. Evaluate the company's financial position and recent developments to determine if the negative market sentiment is warranted. Look into the company's future plans and assess whether they align with the current market trends. Consider holding onto shares if the negative advice seems flimsy, but if underlying issues are present, it may be wise to reduce stake. Prospective investors should assess their risk appetite before investing."

            elif(-0.1 < c <= 0.5) and (-0.3 < b <= 0.5):
                output1 ="Consider evaluating the company's financial position and recent developments to take advantage of the positive market sentiment, as the company's image is quite positive and the quarter results are satisfactory. Assess whether the company's future plans align with the current market trends and if so, consider increasing your stake. However, be mindful of any potential underlying issues and exercise discretion when making investment decisions. Prospective investors should assess their risk appetite before investing, although they may want to trade in small quantities."

            elif(-0.1 < c <= 0.5) and (0.5 < b <= 1.0):
                output1 ="In this scenario, the company's image is quite positive, and the quarter results are satisfactory, while the market sentiment is leaning towards strong positivity. This is an opportune time to evaluate the company's financial position, recent developments, and future plans to make an informed investment decision. Consider increasing your holdings, especially if the market is optimistic about the company's prospects, but exercise discretion and avoid making impulsive decisions. Prospective investors can also look into investing in the company with an eye towards growth potential."

            elif(0.5 < c <= 1.0) and (-1.0 <= b <= 0.5):
                output1 ="In this scenario, the company's image is very positive, the quarter results are amazing, but the market advice is leaning towards negative/neutral, possibly due to suspicions of a bubble or overvaluation of the stock. As an investor, you should thoroughly evaluate the company's financial position and recent developments to determine if the negative market sentiment is warranted. Look for any signs of inflated financials or window dressing that may be masking underlying issues. Consider reducing your stake or selling shares entirely if you find any red flags, and keep an eye on the market for any potential corrections."

            elif(0.5 < c <= 1.0) and (0.5 < b <= 1.0):
                output1 ="In this scenario, the company's image is very positive, the quarter results are excellent, and market advice is leaning towards positivity. As an investor, you will probably want to consider increasing your stake or investing more liberally if you are a new investor, but exercise discretion and make sure to thoroughly evaluate the company's financials and recent developments, keeping in mind your risk appetite. Overall, this looks like a very promising opportunity for investors."
        


        if(-1.0 <= d <= -0.4):
            tradingOutput = "May sell (short term - intraday or within the week)"
        elif(-0.4 < d <= 0.3):
            tradingOutput = "May not trade (short term - intraday or within the week)"
        elif(0.3 < d <= 0.7):
            tradingOutput = "May buy with precaution (short term - intraday or within the week)"
        elif(0.7 < d <= 1.0):
            tradingOutput = "May buy more liberally (short term - intraday or within the week)"

        return output1,tradingOutput