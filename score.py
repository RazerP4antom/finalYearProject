def final_output(a,b,c,d):

    if isinstance(a, str):
        output1 = "Not enough articles found"
    if isinstance(b, str):
        output1 = "Not enough articles found"
    if isinstance(c, str):
        output1 = "Not enough articles found"
    if isinstance(d, str):
        tradingOutput = "Not enough articles found"
    
    if(-1.0 <= a <= -0.3):
        output1 ="Stay away from the company"

    elif(-0.3 < a <= 0.3):
        if(-1.0 <= c <= -0.4):
            output1 ="Hold for old investors, Don't buy for new investors"
        elif(-0.4 < c <= 0.3) and (-1.0 <= b <= -0.4):
            output1 ="Selling off"
        elif(-0.4 < c <= 0.3) and (-0.3 < b <= 0.7):
            output1 ="Trade in small quantities"
        elif(-0.4 < c <=0.3) and (0.7 < b <= 1.0):
            output1 ="Can buy in large quantities"
        elif(0.3 < c <= 1.0) and (-1.0 <= b <= -0.4):
            output1 ="Hold or trade in small quantities"
        elif(0.3 < c <= 1.0) and (-0.4 < b <= 0.6):
            output1 ="Analyst recommendation to change"
        elif(0.3 < c <= 1.0) and (0.6 < b <= 1.0):
            output1 ="Can buy in large quantities"

    elif(0.3 < a <= 1.0):
        if(-1.0 < c <= -0.4):
            output1 ="Analyst rating may change"
        elif(-0.4 < c <= 0.7) and (-1.0 <= b <= -0.4):
            output1 ="Hold or sell off some part of total holdings"
        elif(-0.4 < c <= 0.7) and (-0.4 < b <= 0.6):
            output1 ="Analyst rating may become positive, can buy"
        elif(-0.4 < c <= 0.7) and (0.6 < b <= 1.0):
            output1 ="Can buy in good quantity"
        elif(0.7 < c <= 1.0) and (-1.0 <= b <= 0.6):
            output1 ="Analyst recommendation can change, can buy"
        elif(0.7 < c <= 1.0) and (0.6 < b <= 1.0):
            output1 ="Strong buy"
    


    if(-1.0 <= d <= -0.4):
        tradingOutput = "Sell"
    elif(-0.4 < d <= 0.3):
        tradingOutput = "No Trade"
    elif(0.3 < d <= 0.7):
        tradingOutput = "Buy"
    elif(0.7 < d <= 1.0):
        tradingOutput = "Strong Buy"



    return output1,tradingOutput