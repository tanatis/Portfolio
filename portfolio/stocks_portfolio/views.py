from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from portfolio.position.models import Position
from portfolio.stocks_portfolio.forms import AddPortfolioForm
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
    #print(positions)
    context = {
        'portfolio': portfolio,
        'positions': positions,
    }
    return render(request, 'portfolios/portfolio-details.html', context)

