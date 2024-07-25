from django.shortcuts import render
import yfinance as yf
import datetime as dt
import matplotlib.pyplot as plt
import json
import os
import base64
from io import BytesIO
import datetime as dt





def search_stocks(request):
    json_path = os.path.join(os.path.dirname(__file__), 'companies.json')

    with open(json_path) as f:
        stocks_data = json.load(f)


    stocks = [
        {"ticker": stock["ticker"], "title": stock["title"]}
        for stock in stocks_data.values()
    ]

    context = {
        'stocks': stocks,
    }

    return render(request, 'search.html', context)



def results_stocks(request):
    if request.method == 'GET' and 'ticker' in request.GET:
        ticker = request.GET['ticker']
        years = int(request.GET.get('years', 1))

        start_date = dt.datetime(2000,1,1)
        end_date = dt.datetime.now()
        

        stock = yf.Ticker(ticker)
        history = stock.history(start=start_date, end=end_date)
        history.reset_index(inplace=True)
        
        plt.figure()
        plt.plot(history['Date'], history['Close'])
        plt.title(f'Fechamento do preço de {ticker}')
        plt.xlabel('Data')
        plt.ylabel('Preço de Fechamento')
        plt.grid(True)

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        graphic = base64.b64encode(image_png).decode('utf-8')

        context = {
            'ticker': ticker,
            'graphic': graphic,
        }
        return render(request, 'results.html', context)

    return render(request, 'results.html')
