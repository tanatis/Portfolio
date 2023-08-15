from django.urls import path

from portfolio.stock_picker.views import index

urlpatterns = [
    path('', index, name='index'),
]
