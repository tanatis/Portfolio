from django.urls import path

from portfolio.common.views import error_page, index, ticker_details

urlpatterns = [
    path('', index, name='index'),
    path('ticker/<str:symbol>/', ticker_details, name='ticker_details'),
    path('error/', error_page, name='error'),
]
