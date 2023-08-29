from django.urls import path

from portfolio.stocks_portfolio.views import create_portfolio, delete_portfolio, \
    PortfolioDetailsView, PortfolioDetailsApiView, deposit_withdraw_view

urlpatterns = [
    path('<int:pk>/', PortfolioDetailsView.as_view(), name='details_portfolio'),
    path('<int:pk>/api/', PortfolioDetailsApiView.as_view(), name='details_portfolio_api'),
    path('<int:pk>/delete/', delete_portfolio, name='delete_portfolio'),
    path('<int:pk>/cash/', deposit_withdraw_view, name='deposit_withdraw'),
    path('create/', create_portfolio, name='create_portfolio'),
]
