from django.shortcuts import render, redirect, get_object_or_404

from portfolio.position.forms import AddPositionForm
from portfolio.tickers_list.models import Ticker


def add_position(request, pk):
    ticker = get_object_or_404(Ticker, pk=pk)

    if request.method == 'POST':
        form = AddPositionForm(request.POST)
        if form.is_valid():
            position = form.save(commit=False)
            position.ticker = ticker
            position.save()
            return redirect('index')
    else:
        form = AddPositionForm(initial={'ticker': ticker})

    context = {
        'form': form,
        'ticker': ticker,
    }

    return render(request, 'add-position.html', context)

# def add_position(request):
#
#     if request.method == 'GET':
#         form = AddPositionForm()
#     else:
#         form = AddPositionForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('index')
#
#     context = {
#         'form': form,
#     }
#     return render(request, 'add-position.html', context)
