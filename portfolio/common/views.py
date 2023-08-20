from django.db.models import Q
from django.shortcuts import render
from yahoo_fin.stock_info import get_live_price

from portfolio.common.forms import SearchTickerForm
from portfolio.common.models import Ticker


# TODO: https://stockanalysis.com/list/nasdaq-stocks/


def index(request):
    all_tickers = Ticker.objects.all()

    search_result = None
    form = SearchTickerForm(request.GET)
    search_pattern = None
    if form.is_valid():
        search_pattern = form.cleaned_data['query']

    if search_pattern:
        search_result = all_tickers.filter(
            Q(symbol__icontains=search_pattern) | Q(company_name__icontains=search_pattern)
        )

    # Getting the current price
    # for ticker in search_result:
    #     ticker.price = get_live_price(ticker.symbol)

    #print(search_result)
    context = {
        'tickers_count': all_tickers.count(),
        'search_result': search_result,
        'form': form,
    }
    return render(request, 'index.html', context)


def ticker_details(request, symbol):
    ticker = Ticker.objects.filter(symbol__exact=symbol).get()
    price = get_live_price(ticker.symbol)

    context = {
        'ticker': ticker,
        'price': price,
    }
    return render(request, 'ticker-details.html', context)


def error_page(request):
    return render(request, 'common/error.html')
