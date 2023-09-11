from django.urls import path
from portfolio.common.views import error_page, ticker_details, IndexAPIView, index

urlpatterns = [
    path('', index, name='index'),
    path('ticker/<str:symbol>/', ticker_details, name='ticker_details'),
    path('error/', error_page, name='error'),
    path('api/index/', IndexAPIView.as_view(), name='index_api'),
]
