from django.db.models import Q
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from yahoo_fin.stock_info import get_day_gainers, get_day_losers, get_day_most_active

from portfolio.common.forms import SearchTickerForm
from portfolio.common.models import Ticker

from portfolio.common.serializers import DailyStockMovementSerializer

# https://pypi.org/project/yfinance/
import yfinance as yf

# TODO: https://stockanalysis.com/list/nasdaq-stocks/


class IndexAPIView(APIView):
    @staticmethod
    def get(request):

        losers = {}
        losers_data = get_day_losers(count=10)
        for i in losers_data.index:
            symbol = losers_data['Symbol'][i]
            change = losers_data['% Change'][i]
            name = losers_data['Name'][i]
            losers[i] = [symbol, name, change]

        gainers = {}
        gainers_data = get_day_gainers(count=10)
        for i in gainers_data.index:
            symbol = gainers_data['Symbol'][i]
            change = gainers_data['% Change'][i]
            name = gainers_data['Name'][i]
            gainers[i] = [symbol, name, change]

        active = {}
        active_data = get_day_most_active(count=10)
        for i in active_data.index:
            symbol = active_data['Symbol'][i]
            name = active_data['Name'][i]
            change = active_data['% Change'][i]
            active[i] = [symbol, name, change]

        context = {
            'gainers': gainers,
            'losers': losers,
            'active': active,
        }

        serializer = DailyStockMovementSerializer(context)
        return Response(serializer.data, status=status.HTTP_200_OK)


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

    # losers = {}
    # losers_data = get_day_losers(count=10)
    # for i in losers_data.index:
    #     symbol = losers_data['Symbol'][i]
    #     change = losers_data['% Change'][i]
    #     losers[symbol] = change
    #
    # gainers = {}
    # gainers_data = get_day_gainers(count=10)
    # for i in gainers_data.index:
    #     symbol = gainers_data['Symbol'][i]
    #     change = gainers_data['% Change'][i]
    #     gainers[symbol] = change
    #
    # active = {}
    # active_data = get_day_most_active(count=10)
    # for i in active_data.index:
    #     symbol = active_data['Symbol'][i]
    #     name = active_data['Name'][i]
    #     change = active_data['% Change'][i]
    #     active[symbol] = [name, change]

    context = {
        'tickers_count': all_tickers.count(),
        'search_result': search_result,
        'form': form,
        # 'gainers': gainers,
        # 'losers': losers,
        # 'active': active,
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
