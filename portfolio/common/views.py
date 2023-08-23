from django.db.models import Q
from django.shortcuts import render

from portfolio.common.forms import SearchTickerForm
from portfolio.common.models import Ticker

# https://pypi.org/project/yfinance/
import yfinance as yf

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

    context = {
        'tickers_count': all_tickers.count(),
        'search_result': search_result,
        'form': form,
    }
    return render(request, 'index.html', context)


def ticker_details(request, symbol):
    ticker = Ticker.objects.filter(symbol__exact=symbol).get()

    current_ticker = yf.Ticker(ticker.symbol)

    ticker.name = current_ticker.info['shortName']
    ticker.website = current_ticker.info['website']
    ticker.live_price = current_ticker.info['currentPrice']
    ticker.currency = current_ticker.info['financialCurrency']
    ticker.industry = current_ticker.info['industry']
    ticker.sector = current_ticker.info['sector']
    ticker.summary = current_ticker.info['longBusinessSummary']
    ticker.employees = current_ticker.info['fullTimeEmployees']
    ticker.market_cap = current_ticker.info['marketCap']
    ticker.short_ratio = current_ticker.info['shortRatio']

    context = {
        'ticker': ticker,
    }
    return render(request, 'ticker-details.html', context)


def error_page(request):
    return render(request, 'common/error.html')
