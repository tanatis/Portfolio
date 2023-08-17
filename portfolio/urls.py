from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('portfolio.tickers_list.urls')),
    path('portfolio/', include('portfolio.stocks_portfolio.urls')),
    path('position/', include('portfolio.position.urls')),
]
