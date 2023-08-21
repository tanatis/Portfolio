from django.urls import path

from portfolio.stocks_portfolio.views import create_portfolio, details_portfolio, delete_portfolio, add_withdraw_cash

urlpatterns = [
    path('<int:pk>/', details_portfolio, name='details_portfolio'),
    path('<int:pk>/delete/', delete_portfolio, name='delete_portfolio'),
    path('<int:pk>/cash/', add_withdraw_cash, name='add_withdraw_cash'),
    path('create/', create_portfolio, name='create_portfolio'),
]