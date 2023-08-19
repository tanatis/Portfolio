from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from portfolio.position.forms import AddPositionForm
from portfolio.position.models import Position
from portfolio.stocks_portfolio.models import Portfolio
from portfolio.tickers_list.models import Ticker


@login_required
def add_position(request, pk):
    ticker = get_object_or_404(Ticker, pk=pk)

    if request.method == 'POST':
        form = AddPositionForm(request.POST)
        if form.is_valid():
            count = form.cleaned_data['count']
            price = form.cleaned_data['price']
            portfolio_id = form.cleaned_data['to_portfolio'].id
            portfolio = Portfolio.objects.get(pk=portfolio_id)
            if count * price > portfolio.cash:
                return redirect('index')

            # Check if a position with the same ticker already exists in the portfolio
            existing_position = Position.objects.filter(ticker=ticker, to_portfolio_id=portfolio_id).first()

            if existing_position:
                # Update the existing position's count and price
                existing_position.count += count
                existing_position.price += price * count
                existing_position.save()
            else:
                # Create a new position
                position = Position(
                    ticker=ticker,
                    count=count,
                    price=price * count,
                    to_portfolio_id=portfolio_id
                )
                position.save()

            return redirect('index')

    else:
        form = AddPositionForm(initial={'ticker': ticker})

    context = {
        'form': form,
        'ticker': ticker,
    }

    return render(request, 'positions/add-position.html', context)
