from django.urls import path

from portfolio.tickers_list.views import index, ticker_details

urlpatterns = [
    path('', index, name='index'),
    path('ticker/<str:symbol>/', ticker_details, name='ticker_details'),
]
