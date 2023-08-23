from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from yahoo_fin.stock_info import get_live_price

from portfolio.account.models import AppUserHistory
from portfolio.position.models import Position
from portfolio.stocks_portfolio.forms import AddPortfolioForm, DeletePortfolioForm, CashTransactionForm
from portfolio.stocks_portfolio.models import Portfolio


@login_required
def create_portfolio(request):
    user = request.user
    if request.method == 'GET':
        form = AddPortfolioForm()
    else:
        form = AddPortfolioForm(request.POST)
        if form.is_valid():
            portfolio = form.save(commit=False)
            #cash = form.cleaned_data['cash']
            portfolio.user = user
            portfolio.save()

            user_history = AppUserHistory(
                to_user=request.user,
                operation_type='deposit',
                ticker=None,
                date_added=portfolio.date_added,
                count=None,
                price=portfolio.cash)
            user_history.save()

            return redirect('index')
    context = {
        'form': form,
    }
    return render(request, 'portfolios/create-portfolio.html', context)


def details_portfolio(request, pk):
    portfolio = Portfolio.objects.filter(pk=pk, user_id=request.user.id).get()
    positions = Position.objects.filter(to_portfolio_id=portfolio.pk)
    for position in positions:
        position.current_price = get_live_price(position.ticker.symbol)
        position.change = (position.current_price - position.avg_price) / position.avg_price * 100

    context = {
        'portfolio': portfolio,
        'positions': positions,
    }
    return render(request, 'portfolios/portfolio-details.html', context)


def delete_portfolio(request, pk):
    portfolio = Portfolio.objects.get(pk=pk)

    if request.method == "GET":
        form = DeletePortfolioForm(instance=portfolio)
    else:
        form = DeletePortfolioForm(request.POST, instance=portfolio)
        if form.is_valid():
            form.save()
            return redirect('index')

    context = {
        'form': form,
        'portfolio': portfolio,
    }
    return render(request, 'portfolios/delete-portfolio.html', context)


def add_withdraw_cash(request, pk):
    portfolio = Portfolio.objects.get(pk=pk)

    if request.method == 'GET':
        form = CashTransactionForm()
    else:
        form = CashTransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.portfolio = portfolio
            operation_type = None
            if transaction.operation == 'withdraw':
                if transaction.amount <= portfolio.cash:
                    portfolio.cash -= transaction.amount
                    operation_type = 'withdraw'
                else:
                    messages.error(request, f'You cannot withdraw more than {portfolio.cash:.2f}')
                    return redirect(request.META['HTTP_REFERER'])
            else:
                portfolio.cash += transaction.amount
                operation_type = 'deposit'

            transaction.save()

            user_history = AppUserHistory(
                to_user=request.user,
                operation_type=operation_type,
                ticker=None,
                date_added=transaction.date_added,
                count=None,
                price=transaction.amount)
            user_history.save()

            portfolio.save()
            return redirect('details_portfolio', pk=portfolio.pk)
    context = {
        'portfolio': portfolio,
        'form': form,
    }
    return render(request, 'portfolios/add-withdraw.html', context)
