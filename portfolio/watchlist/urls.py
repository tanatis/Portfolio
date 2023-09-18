from django.urls import path

from portfolio.watchlist.views import watchlist_details, add_to_watchlist, remove_from_watchlist

urlpatterns = [
    path('', watchlist_details, name='watchlist'),
    path('add/<str:ticker>/', add_to_watchlist, name='add_to_watchlist'),
    path('remove/<str:ticker>/', remove_from_watchlist, name='remove_from_watchlist'),
]
