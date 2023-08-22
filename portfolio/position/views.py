from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from portfolio.common.models import Ticker
from portfolio.position.forms import CreatePositionForm, AddToPositionForm, SellPositionForm
from portfolio.position.models import Position, PositionHistory
from portfolio.stocks_portfolio.models import Portfolio


@login_required
def create_position(request, pk):
    ticker = get_object_or_404(Ticker, pk=pk)

    if request.method == 'POST':
        form = CreatePositionForm(request.POST)
        if form.is_valid():
            count = form.cleaned_data['count']
            price = form.cleaned_data['price']
            portfolio_id = form.cleaned_data['to_portfolio'].id
            portfolio = Portfolio.objects.get(pk=portfolio_id)
            if count * price > portfolio.cash:
                messages.error(request, f'Insufficient funds')
                return redirect(request.META['HTTP_REFERER'])

            # Check if a position with the same ticker already exists in the portfolio
            existing_position = Position.objects.filter(ticker=ticker, to_portfolio_id=portfolio_id).first()

            if existing_position:
                # Update the existing position's count and price
                existing_position.count += count
                existing_position.price += price * count
                existing_position.avg_price = existing_position.price / existing_position.count
                existing_position.save()
                position_history = PositionHistory(to_position=existing_position, date_added=existing_position.date_added, count=count, price=price)
                position_history.save()
            else:
                # Create a new position
                position = Position(
                    ticker=ticker,
                    count=count,
                    price=price * count,
                    to_portfolio_id=portfolio_id,
                    avg_price=price,
                )
                position.save()
                position_history = PositionHistory(to_position=position, date_added=position.date_added, count=position.count, price=price)
                position_history.save()
            portfolio.cash -= count * price
            portfolio.save()
            return redirect('details_portfolio', pk=portfolio.pk)

    else:
        form = CreatePositionForm(initial={'ticker': ticker})

    context = {
        'form': form,
        'ticker': ticker,
    }

    return render(request, 'positions/create-position.html', context)


def add_to_position(request, pk):
    position = Position.objects.get(pk=pk)
    portfolio = Portfolio.objects.get(pk=position.to_portfolio_id)

    if request.method == 'GET':
        form = AddToPositionForm()
    else:
        form = AddToPositionForm(request.POST)
        if form.is_valid():
            count = form.cleaned_data['count']
            price = form.cleaned_data['price']
            if count * price > portfolio.cash:
                messages.error(request, 'Not enough cash to complete the operation')
                return redirect(request.META['HTTP_REFERER'])

            position.count += count
            position.price += count * price
            position.avg_price = position.price / position.count
            position.save()

            portfolio.cash -= count * price
            portfolio.save()
            position_history = PositionHistory(to_position=position, date_added=position.date_added, count=count, price=price)
            position_history.save()
            return redirect('details_portfolio', pk=portfolio.pk)

    context = {
        'form': form,
        'position': position,
        'portfolio': portfolio,
    }

    return render(request, 'positions/add-to-position.html', context)


def sell_position(request, pk):
    position = Position.objects.get(pk=pk)
    portfolio = Portfolio.objects.get(pk=position.to_portfolio.id)
    if request.method == 'GET':
        form = SellPositionForm()
    else:
        form = SellPositionForm(request.POST)
        if form.is_valid():
            count = form.cleaned_data['count']
            price = form.cleaned_data['price']
            if count > position.count:
                messages.error(request, f'You cannot sell more than {position.count} shares')
                return redirect(request.META['HTTP_REFERER'])
            elif count == position.count:
                position.delete()
            else:
                position.count -= count
                position.price -= count * position.avg_price
                position.save()
                position_history = PositionHistory(to_position=position, date_added=position.date_added, count=-count, price=price)
                position_history.save()

            # position.price -= price * count
            portfolio.cash += count * price
            portfolio.save()
            #position.save()
            return redirect('details_portfolio', pk=portfolio.pk)

    context = {
        'form': form,
        'position': position,
    }

    return render(request, 'positions/sell-position.html', context)
