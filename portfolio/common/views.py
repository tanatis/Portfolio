from django.db.models import Q
from django.shortcuts import render
from yahoo_fin.stock_info import get_day_gainers

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

    gainers_data = {}
    gainers = get_day_gainers()
    for i in gainers.head(5).index:
        symbol = gainers['Symbol'][i]
        change = gainers['% Change'][i]
        gainers_data[symbol] = change

    context = {
        'tickers_count': all_tickers.count(),
        'search_result': search_result,
        'form': form,
        'gainers': gainers_data,
    }
    return render(request, 'index.html', context)


'''
 'address1': '1200 17th Street',
 'address2': 'Floor 15',
 'city': 'Denver',
 'state': 'CO',
 'zip': '80202',
 'country': 'United States',
 'phone': '720 358 3679',
 'website': 'https://www.palantir.com',
 'industry': 'Software—Infrastructure',
 'industryDisp': 'Software—Infrastructure',
 'sector': 'Technology',
 'sectorDisp': 'Technology',
 'fullTimeEmployees': 3734,
 'bookValue': 1.375,
 'priceToBook': 11.036364,
 'lastFiscalYearEnd': 1672444800,
 'nextFiscalYearEnd': 1703980800,
 'mostRecentQuarter': 1688083200,
 'netIncomeToCommon': -48068000,
 'trailingEps': -0.02,
 'forwardEps': 0.27,
 'pegRatio': 0.8,
 'enterpriseToRevenue': 14.615,
 'enterpriseToEbitda': -834.975,
 '52WeekChange': 1.0851648,
 'SandP52WeekChange': 0.15546322,
 'exchange': 'NYQ',
 'quoteType': 'EQUITY',
 'symbol': 'PLTR',
 'underlyingSymbol': 'PLTR',
 'shortName': 'Palantir Technologies Inc.',
 'longName': 'Palantir Technologies Inc.',
 'firstTradeDateEpochUtc': 1601472600,
 'currentPrice': 15.175,
 'targetHighPrice': 25.0,
 'targetLowPrice': 5.0,
 'targetMeanPrice': 14.11,
 'targetMedianPrice': 14.5,
 'recommendationMean': 3.4,
 'recommendationKey': 'hold',
 'numberOfAnalystOpinions': 14,
 'totalCash': 3103251968,
 'totalCashPerShare': 1.442,
 'ebitda': -35794000,
 'totalDebt': 245988992,
 'quickRatio': 5.076,
 'currentRatio': 5.219,
 'totalRevenue': 2045006976,
 'debtToEquity': 8.105,
 'revenuePerShare': 0.973,
 'returnOnAssets': -0.01133,
 'returnOnEquity': -0.01611,
 'grossProfits': 1497322000,
 'freeCashflow': 435973248,
 'operatingCashflow': 403396992,
 'revenueGrowth': 0.127,
 'grossMargins': 0.79146004,
 'ebitdaMargins': -0.0175,
 'operatingMargins': -0.032190003,
 'financialCurrency': 'USD',
 'trailingPegRatio': 0.9712
'''


def ticker_details(request, symbol):
    ticker = Ticker.objects.filter(symbol__exact=symbol).get()

    current_ticker = yf.Ticker(ticker.symbol)
    # print(current_ticker.info)
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
