from django.shortcuts import render, redirect

from portfolio.position.models import Position
from portfolio.stocks_portfolio.forms import AddPortfolioForm
from portfolio.stocks_portfolio.models import Portfolio


def create_portfolio(request):
    if request.method == 'GET':
        form = AddPortfolioForm()
    else:
        form = AddPortfolioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    context = {
        'form': form,
    }
    return render(request, 'create-portfolio.html', context)


def details_portfolio(request, pk):
    portfolio = Portfolio.objects.filter(pk=pk).get()
    positions = Position.objects.filter(to_portfolio_id=portfolio.pk)
    print(positions)
    context = {
        'portfolio': portfolio,
        'positions': positions,
    }
    return render(request, 'portfolio-details.html', context)
