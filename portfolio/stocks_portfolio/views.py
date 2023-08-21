from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

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
            portfolio.user = user
            portfolio.save()
            return redirect('index')
    context = {
        'form': form,
    }
    return render(request, 'portfolios/create-portfolio.html', context)


def details_portfolio(request, pk):
    portfolio = Portfolio.objects.filter(pk=pk, user_id=request.user.id).get()
    positions = Position.objects.filter(to_portfolio_id=portfolio.pk)

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
            if transaction.operation == 'withdraw':
                if transaction.amount <= portfolio.cash:
                    portfolio.cash -= transaction.amount
                else:
                    messages.error(request, f'You cannot withdraw more than {portfolio.cash:.2f}')
                    return redirect(request.META['HTTP_REFERER'])
            else:
                portfolio.cash += transaction.amount
            transaction.save()
            portfolio.save()
            return redirect('details_portfolio', pk=portfolio.pk)
    context = {
        'portfolio': portfolio,
        'form': form,
    }
    return render(request, 'portfolios/add-withdraw.html', context)
