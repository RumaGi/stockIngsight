import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
alphavantage_api_key =  "PUT YOUR ALPHAVANTAGE KEY" # alphavantage API key
news_api_key =  "INSERT YOUR NEWS API KEY"    # news API key
account_sid =  " INSERT YOUR TWILIO ACCOUNT SSID"  # account ID for twilio
auth_token =   "INSERT YOUR TWITLIO AUTH TOKEN"   # auth token for twilio

parameters = {
    'function': "TIME_SERIES_DAILY",
    'symbol': STOCK,
    'apikey': alphavantage_api_key

}

response = requests.get(url="https://www.alphavantage.co/query", params=parameters)
response.raise_for_status()
stock_data = response.json()

items = list(stock_data["Time Series (Daily)"].keys())

yesterday_date = items[0]
day_before_yesterday = items[1]

yesterday_close = float(stock_data["Time Series (Daily)"][items[0]]['4. close'])
day_before_close = float(stock_data["Time Series (Daily)"][items[1]]['4. close'])

print(day_before_close)
print(yesterday_close)

percentage = ((yesterday_close - day_before_close) / day_before_close) * 100
rounded_percentage = round(percentage, 2)

print(rounded_percentage)

if rounded_percentage >= 3 or rounded_percentage <= -3:
    news_params = {
        'qInTitle': 'Tesla',
        'from': yesterday_date,
        'sort': 'popularity',
        'apiKey': news_api_key
    }

    response_2 = requests.get(url="https://newsapi.org/v2/everything", params=news_params)
    response_2.raise_for_status()
    news_data = response_2.json()["articles"]
    print(news_data)
    change_symbol = "?"
    if rounded_percentage > 0:
        change_symbol = "🔺"
    elif rounded_percentage < 0:
        change_symbol = "🔻"

    client = Client(account_sid, auth_token)
    for i in range(3):
        message = client.messages.create(
            from_="YOUR NUMBER GENERATED FROM TWILIO",  # from_ because from is a keyword
            body=f"""
            TSLA: {change_symbol}{rounded_percentage}
            Headline: {news_data[i]["title"]}
            Brief: {news_data[i]["description"]}
            """,
            to='YOUR NUMBER WITH COUNRTY CODE'
        )


else:
    print("CHANGE NOT GREATER THAN 5%\n")