from django.urls import path

from portfolio.tickers_list.views import index, ticker_info

urlpatterns = [
    path('', index, name='index'),
    path('ticker/<str:symbol>/', ticker_info, name='info'),
]
