from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from portfolio.common.models import Ticker
from portfolio.watchlist.models import Watchlist
import yfinance as yf


@login_required
def watchlist_details(request):
    user = request.user

    try:
        watchlist = Watchlist.objects.get(user=user)
    except Watchlist.DoesNotExist:
        watchlist = None

    watchlist_data = {}
    for ticker in watchlist.tickers.all():
        current_ticker = yf.Ticker(ticker.symbol)
        watchlist_data[ticker.symbol] = current_ticker.info['shortName']

    context = {
        'watchlist': watchlist_data,
    }
    return render(request, 'watchlist/watchlist.html', context)


def add_to_watchlist(request, ticker):
    user = request.user
    tkr = Ticker.objects.get(symbol=ticker)
    user_watchlist, created = Watchlist.objects.get_or_create(user=user)
    user_watchlist.tickers.add(tkr)

    return redirect('watchlist')


def remove_from_watchlist(request, ticker):
    user = request.user
    tkr = Ticker.objects.get(symbol=ticker)
    user_watchlist = Watchlist.objects.get(user=user)
    user_watchlist.tickers.remove(tkr)

    return redirect('watchlist')
